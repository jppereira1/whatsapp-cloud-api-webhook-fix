#### 2. Arquivo `main.py` (O Servidor Exemplo)
# Código limpo e pronto para uso.
# main.py

from fastapi import FastAPI, Query, Request
import uvicorn
import requests

#--------------- Credenciais -----------------
TOKEN = "EAAMjUMSwBMcBQn3x53PdJ7gcziXiL9jdhptiDQq7xbddthQKzKolCL1XvEIJWmHM3W6gk5h5z87ScsIIh53d1SKQVAzhpY5HqZBLwejBRmEaigFJ4ZAkQWjDU5L0IBTdtKBrOTZCH2ZBWOKAe2Kg7joUw9zdh453zsXsZBZCQZCMD6E3HRZCHEsPXih3EFCF7ZAh9bl3iiCAt2TmybZA5x9Xa6E69LD4aDJpw57YMNMXNvss1zmDxGxP740hS9OV15Ecpqu5z5D6cEzy7FbZAAoJjPeZBTdf"
PHONE_ID = "946393031891418"

# --------- Criando funções de ação -------------
def enviar_resposta(numero_destino, texto_resposta):
    url = f"https://graph.facebook.com/v21.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "text",
        "text": {"body": texto_resposta}
    }
    
    # Dispara a mensagem
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"✅ Resposta enviada para {numero_destino}!")
    else:
        print(f"❌ Erro ao enviar: {response.text}")


# --------- inicializando app ---------------
app = FastAPI()
# apenas confirmação de funcionamento
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
    # DICA: Em produção, use variáveis de ambiente!
    VERIFY_TOKEN = "meu_token_secreto" 
    
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("Webhook validado com sucesso!")
        return int(hub_challenge)
    return {"status": "error", "message": "Token inválido"}

# 2. Recebimento de Mensagens (POST)
@app.post("/webhook")
@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        body = await request.json()
        
        # Navegando no JSON complexo do WhatsApp
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        # CASO 1: É UMA MENSAGEM DE TEXTO?
        if "messages" in value:
            message = value["messages"][0]
            numero_bruto = message["from"]
            texto_usuario = message["text"]["body"]
            nome = value["contacts"][0]["profile"]["name"]

            if numero_bruto.startswith("55") and len(numero_bruto) == 12:
                ddd = numero_bruto[2:4]
                resto = numero_bruto[4:]
                numero = f"55{ddd}9{resto}"
                print(f"🔧 Número corrigido de {numero_bruto} para {numero}")
            else:
                numero = numero_bruto
            
            print(f"📩 Recebido de {nome}: {texto_usuario}")
            print(f"número de telefone: {numero}\n")
            # --- AQUI ESTÁ A MÁGICA: O BOT RESPONDE! ---
            nova_resposta = f"Olá {nome}! Você disse: '{texto_usuario}'"
            enviar_resposta(numero, nova_resposta)


        # CASO 2: É APENAS UM STATUS (visto, entregue)?
        elif "statuses" in value:
            status = value["statuses"][0]["status"]
            print(f"📡 Status de entrega: {status}")

        else:
            print("⚠️ Evento desconhecido recebido.")

    except Exception as e:
        # Se o JSON vier quebrado ou diferente do esperado
        print(f"❌ Erro ao processar: {e}")
    
    # Sempre retornar 200, senão o WhatsApp bloqueia seu número!
    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
