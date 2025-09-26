# flow_manager.py
from nlp_service import QUESTION_MAP

conversation_states = {}

def get_current_state(user_phone):
    if user_phone not in conversation_states:
        conversation_states[user_phone] = {
            "stage": "start",
            "answers": {},
            "unanswered_questions": list(QUESTION_MAP.keys())
        }
    return conversation_states[user_phone]

def update_state(user_phone, stage=None, answers=None):
    state = get_current_state(user_phone)
    if stage:
        state["stage"] = stage
    if answers:
        for key, value in answers.items():
            state["answers"][key] = value
            if key in state["unanswered_questions"]:
                state["unanswered_questions"].remove(key)
    conversation_states[user_phone] = state
    return state

def get_next_question(user_phone):
    state = get_current_state(user_phone)
    if not state["unanswered_questions"]:
        return None
    next_question_key = state["unanswered_questions"][0]
    return QUESTION_MAP[next_question_key]

# FUNÇÃO ADICIONADA AQUI
def get_current_question_key(user_phone):
    """Retorna a chave da pergunta que está sendo feita agora."""
    state = get_current_state(user_phone)
    if state["unanswered_questions"]:
        return state["unanswered_questions"][0]
    return None