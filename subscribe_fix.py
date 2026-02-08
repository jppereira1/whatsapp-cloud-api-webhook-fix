# subscribe_fix.py
import requests

# --- CONFIGURAÇÃO ---
# Pegue estes dados na aba "API Setup" ou "Testes de API" do seu App na Meta
ACCESS_TOKEN = "SEU_ACCESS_TOKEN_AQUI"
PHONE_NUMBER_ID = "SEU_PHONE_NUMBER_ID_AQUI" 
API_VERSION = "v21.0"

def fix_webhook_connection():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    print(f"1. Buscando WABA ID para o telefone {PHONE_NUMBER_ID}...")
    
    # Passo 1: Descobrir o WABA ID (Business Account)
    url_get_waba = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}"
    params = {"fields": "whatsapp_business_account"}
    
    resp = requests.get(url_get_waba, headers=headers, params=params)
    
    if resp.status_code != 200:
        print(f"Erro ao buscar conta: {resp.text}")
        return

    waba_id = resp.json().get('whatsapp_business_account', {}).get('id')
    
    if not waba_id:
        print("WABA ID não encontrado. Verifique se o telefone está vinculado a uma conta.")
        return
        
    print(f"WABA ID Encontrado: {waba_id}")
    print(f"2. Forçando assinatura do App na conta {waba_id}...")

    # Passo 2: Forçar a assinatura (Subscribe)
    url_subscribe = f"https://graph.facebook.com/{API_VERSION}/{waba_id}/subscribed_apps"
    payload = {"subscribed_fields": ["messages"]}
    
    sub_resp = requests.post(url_subscribe, headers=headers, json=payload)
    
    if sub_resp.status_code == 200 and sub_resp.json().get('success'):
        print("\nSUCESSO! A conexão foi restabelecida.")
        print("Agora o Facebook sabe para onde enviar as mensagens reais.")
        print("Teste enviando um 'Oi' do seu celular para o Bot.")
    else:
        print(f"\nFalha ao assinar: {sub_resp.text}")

if __name__ == "__main__":
    fix_webhook_connection()
