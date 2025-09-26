# crm_service.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

CRM_API_URL = os.getenv("CRM_API_URL")
CRM_API_KEY = os.getenv("CRM_API_KEY")

headers = {
    "Authorization": f"Bearer {CRM_API_KEY}",
    "Content-Type": "application/json"
}

def create_lead(name, phone):
    """Cria um novo lead no CRM e retorna o ID."""
    endpoint = f"{CRM_API_URL}/leads"
    payload = {
        "name": name,
        "phone": phone,
        "status": "Novo Lead" # Status inicial
    }
    print(f"Criando lead: {payload}")
    # response = requests.post(endpoint, headers=headers, json=payload)
    # response.raise_for_status()
    # return response.json()['id']
    # --- Simulação ---
    print("Lead criado no CRM com ID 12345.")
    return "12345"

def update_lead_data(lead_id, field, value):
    """Atualiza um campo específico de um lead no CRM."""
    endpoint = f"{CRM_API_URL}/leads/{lead_id}"
    payload = {field: value}
    print(f"Atualizando lead {lead_id} com {payload}")
    # requests.patch(endpoint, headers=headers, json=payload)
    # --- Simulação ---
    print(f"Campo {field} atualizado para {value} no lead {lead_id}.")

def update_lead_status(lead_id, new_status):
    """Move o card do lead para uma nova etapa no CRM."""
    print(f"Movendo lead {lead_id} para o status: {new_status}")
    update_lead_data(lead_id, "status", new_status)