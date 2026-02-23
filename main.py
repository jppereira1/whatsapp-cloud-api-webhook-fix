#### 2. Arquivo `main.py` (O Servidor Exemplo)
# Código limpo e pronto para uso.
# main.py

import os
import uvicorn
from fastapi import FastAPI, Request
import requests
from dotenv import load_dotenv  # <-- Importa o leitor de .env
from openai import OpenAI       # <-- Importa a IA
from fastapi.responses import PlainTextResponse

# 1. Carrega as variáveis do arquivo .env para a memória
load_dotenv()

app = FastAPI()

# 2. Pega as chaves de forma segura
# (Certifique-se de que WHATSAPP_TOKEN e PHONE_ID também estejam no seu .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_ID")
API_VERSION = os.getenv("API_VERSION")

# 3. Inicializa o cliente da IA
client = OpenAI(api_key=OPENAI_API_KEY)

# --- O CÉREBRO (IA) ---
def consultar_ia(texto_usuario):
    print("🧠 Consultando a OpenAI...")
    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo", # Pode usar gpt-4o-mini se preferir (é mais barato e rápido)
            messages=[
                # SYSTEM PROMPT: A personalidade e as regras do bot
                {"role": "system", "content": """
                 Você é o assistente virtual da barbearia 'Cortes do Fabio'.
                 Seja amigável, direto e use um tom natural e conversacional.
                 Se o cliente perguntar preços: Corte R$50, Barba R$30.
                 Se o cliente quiser agendar, diga que em breve você terá acesso à agenda, 
                 mas por enquanto está apenas em fase de testes.
                 Responda de forma concisa (máximo 50 palavras).
                 """},
                {"role": "user", "content": texto_usuario}
            ],
            temperature=0.7 # Controla a criatividade (0 = robótico, 1 = muito criativo)
        )
        return resposta.choices[0].message.content
    except Exception as e:
        print(f"❌ Erro na IA: {e}")
    return "Desculpe, estou com um pouco de dor de cabeça agora. Tente novamente em instantes."

# --- FUNÇÃO DE ENVIO DE WHATSAPP ---
def enviar_resposta(numero_destino, texto_resposta):
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "text",
        "text": {"body": texto_resposta}
    }
    requests.post(url, json=payload, headers=headers)

# --- O WEBHOOK ---
from fastapi import Query

@app.get("/")
def home():
    return {"message": "O Bot está ON! 🤖 Vá para /webhook"}

# 1. Validação do Webhook (GET)
@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    # Pode colocar a string direta aqui ou puxar do .env
    VERIFY_TOKEN = "seu_token_secreto" 
    
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("✅ Webhook validado pela Meta!")
        # A Meta exige retorno em texto puro, não JSON:
        return PlainTextResponse(content=hub_challenge)
    
    # Print para debug se os tokens não baterem:
    print(f"❌ Falha. Token no .env: {VERIFY_TOKEN} | Token da Meta: {hub_verify_token}")
    return {"status": "error", "message": "Falha na validação"}

# 2. Recebimento das Mensagens (POST)
@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        body = await request.json()
        
        entry = body.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})

        # FILTRO: É MENSAGEM?
        if "messages" in value:
            message = value["messages"][0]
            numero_bruto = message["from"]
            
            # Corrige o número
            if numero_bruto.startswith("55") and len(numero_bruto) == 12:
                numero = f"55{numero_bruto[2:4]}9{numero_bruto[4:]}"
            else:
                numero = numero_bruto

            texto_usuario = message.get("text", {}).get("body", "")
            nome = value["contacts"][0]["profile"]["name"]
            
            if texto_usuario:
                # print(f"📩 {nome} disse: {texto_usuario}")
                print(f"📩 {nome} enviou mensagem!")
                
                # --- A MÁGICA ACONTECE AQUI ---
                resposta_ia = consultar_ia(texto_usuario)
                
                # print(f"🤖 IA respondeu: {resposta_ia}")
                print("🤖 IA respondeu")
                enviar_resposta(numero, resposta_ia)

    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
    
    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)