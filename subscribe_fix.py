import requests
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
API_VERSION = os.getenv("API_VERSION", "v25.0")
WABA_ID = "COLE_SEU_ID_DA_CONTA_AQUI" # <-- Copie do painel da Meta

def fix_webhook_connection():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    url_subscribe = f"https://graph.facebook.com/{API_VERSION}/{WABA_ID}/subscribed_apps"
    payload = {"subscribed_fields": ["messages"]}
    
    sub_resp = requests.post(url_subscribe, headers=headers, json=payload)
    
    if sub_resp.status_code == 200 and sub_resp.json().get('success'):
        print("✅ SUCESSO! A conexão foi restabelecida.")
    else:
        print(f"❌ Falha ao assinar: {sub_resp.text}")

if __name__ == "__main__":
    fix_webhook_connection()
