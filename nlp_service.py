# nlp_service.py
import os
import openai
import json
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (incluindo a OPENAI_API_KEY)
load_dotenv()

# Configura o cliente da OpenAI
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("A chave da API da OpenAI não foi encontrada no arquivo .env")
except Exception as e:
    print(f"Erro ao configurar a API da OpenAI: {e}")

# O mapa de perguntas continua útil para sabermos o que perguntar
QUESTION_MAP = {
    'company_name_cnpj': "Qual o nome e o CNPJ da sua empresa?",
    'employee_count': "Quantos colaboradores vocês possuem?",
    'is_security_branch': "Vocês já são do ramo de segurança eletrônica?",
    'is_isp': "É um provedor de internet?",
    'uses_security_software': "Utiliza algum software para segurança?",
    'uses_erp': "Utiliza algum software ERP?",
    'total_clients': "Qual o total de clientes que vocês atendem?",
    'avg_ticket': "Qual é o ticket médio por cliente?",
    'decision_maker': "Qual o nome do decisor com quem podemos conversar?",
    'has_server': "Sua empresa possui servidor próprio?",
    'has_cameras': "Vocês trabalham com câmeras ou possuem câmeras?"
}

# Este é o "cérebro" do nosso assistente. É a instrução principal para a IA.
SYSTEM_PROMPT = """
Você é um assistente de qualificação de leads para uma empresa de software de segurança.
Seu objetivo é extrair informações específicas da resposta de um cliente.
Analise a "Pergunta feita ao cliente" e a "Resposta do cliente".
Sua resposta DEVE ser um objeto JSON VÁLIDO contendo as chaves que você conseguir extrair.
As chaves possíveis são: {keys}

- Para 'employee_count', 'total_clients', e 'avg_ticket', extraia apenas o valor numérico.
- Para perguntas de sim/não ('is_security_branch', 'is_isp', etc.), retorne "sim" ou "não".
- Se uma informação não for mencionada na resposta do cliente, omita a chave do JSON.
- Se o cliente responder algo que não se encaixa em nenhuma chave específica, mas responde diretamente à pergunta, use a chave da pergunta para armazenar a resposta completa.

Exemplo de resposta esperada:
{{
  "employee_count": 50,
  "is_security_branch": "sim"
}}
""".format(keys=json.dumps(list(QUESTION_MAP.keys())))


def analyze_message(text: str, current_question_key: str = None):
    """
    Usa a API da OpenAI para extrair entidades da mensagem do usuário.
    """
    if not openai.api_key:
        print("API Key da OpenAI não configurada. Usando fallback.")
        if current_question_key:
            return {'entities': {current_question_key: text}}
        return {'entities': {}}

    try:
        question_text = QUESTION_MAP.get(current_question_key, "Pergunta geral")
        
        # CORREÇÃO AQUI: Removido o \ antes das aspas triplas
        user_content = f"""
        Pergunta feita ao cliente: "{question_text}"
        
        Resposta do cliente: "{text}"
        """

        response = openai.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ]
        )

        extracted_json = response.choices[0].message.content
        entities = json.loads(extracted_json)
        
        return {'entities': entities if isinstance(entities, dict) else {}}

    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")
        if current_question_key:
            return {'entities': {current_question_key: text}}
        return {'entities': {}}