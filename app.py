# app.py
from flask import Flask, request
import os
from dotenv import load_dotenv

import whatsapp_service as wa
import crm_service as crm
import flow_manager as flow
import nlp_service as nlp

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "seu_token_de_verificacao")

# ... (código do webhook permanece o mesmo) ...

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge'), 200
        else:
            return 'Forbidden', 403
    else: # POST
        data = request.get_json()
        if data.get('object') == 'whatsapp_business_account':
            try:
                for entry in data['entry']:
                    for change in entry['changes']:
                        if 'messages' in change['value']:
                            message_data = change['value']['messages'][0]
                            sender_phone = message_data['from']
                            message_text = message_data['text']['body']
                            user_name = change['value']['contacts'][0]['profile']['name']
                            process_message(sender_phone, user_name, message_text)
            except Exception as e:
                print(f"Erro ao processar webhook: {e}")
                pass
        return 'OK', 200

def process_message(user_phone, user_name, message):
    state = flow.get_current_state(user_phone)
    stage = state.get("stage")

    if stage == "start":
        lead_id = crm.create_lead(user_name, user_phone)
        if lead_id:
            flow.update_state(user_phone, stage="qualifying", answers={"crm_id": lead_id})
            wa.send_whatsapp_message(
                user_phone,
                f"Olá {user_name}! Bem-vindo(a). Sou o assistente de IA e preciso de algumas informações para te direcionar ao especialista certo."
            )
            next_question = flow.get_next_question(user_phone)
            wa.send_whatsapp_message(user_phone, next_question)
        else:
            wa.send_whatsapp_message(user_phone, "Tivemos um problema para iniciar seu cadastro. Por favor, tente novamente mais tarde.")
        return

    if stage == "qualifying":
        # ALTERAÇÃO AQUI: Pegamos o contexto da pergunta atual
        current_question_key = flow.get_current_question_key(user_phone)
        
        # E passamos esse contexto para o serviço de NLP
        nlp_result = nlp.analyze_message(message, current_question_key)
        entities = nlp_result.get('entities', {})
        
        # Agora 'entities' nunca estará vazio, então o fluxo sempre avançará
        if entities:
            flow.update_state(user_phone, answers=entities)
            crm_id = state.get("answers", {}).get("crm_id")
            if crm_id:
                for key, value in entities.items():
                    crm.update_lead_data(crm_id, key, value)
            print(f"Entidades extraídas para {user_phone}: {entities}")

        next_question = flow.get_next_question(user_phone)
        if next_question:
            wa.send_whatsapp_message(user_phone, next_question)
        else:
            handle_qualification_result(user_phone)

# ... (função handle_qualification_result permanece a mesma) ...

def handle_qualification_result(user_phone):
    """Decide o que fazer após a qualificação, com base nas respostas coletadas."""
    state = flow.get_current_state(user_phone)
    answers = state.get("answers", {})
    lead_id = answers.get("crm_id")

    if not lead_id:
        print(f"Erro: Tentativa de qualificar lead sem crm_id para o usuário {user_phone}")
        return

    # --- Lógica de Decisão baseada no fluxograma ---
    # Critério: Pertence ao ramo de segurança E tem mais de 10 colaboradores (exemplo)
    is_qualified = False
    try:
        employee_count = int(answers.get("employee_count", 0))
        is_security = answers.get("is_security_branch", "").lower() == "sim"
        
        if is_security and employee_count > 10: # Critério de "LEAD MADURO"
            is_qualified = True

    except (ValueError, TypeError):
        is_qualified = False

    if is_qualified:
        crm.update_lead_status(lead_id, "Qualificado")
        flow.update_state(user_phone, stage="scheduling") # Próximo passo seria agendar
        wa.send_whatsapp_message(
            user_phone,
            "Obrigado pelas respostas! Vi que temos uma ótima solução para você. Um de nossos especialistas entrará em contato para agendar uma demonstração."
        )
        # Aqui, o fluxo continuaria para agendamento, como no diagrama
    else:
        # Lead desqualificado ou não maduro
        crm.update_lead_status(lead_id, "Desqualificado")
        wa.send_whatsapp_message(
            user_phone,
            "Agradeço muito pelas informações. No momento, não parece que temos a solução ideal para o seu perfil. Manteremos seu contato para futuras oportunidades, ok?"
        )
        # Iniciar fluxo de nutrição, se aplicável
        flow.update_state(user_phone, stage="nurturing")

if __name__ == '__main__':
    app.run(port=5000, debug=True)