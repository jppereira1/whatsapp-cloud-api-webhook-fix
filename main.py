#### 2. Arquivo `main.py` (O Servidor Exemplo)
# Código limpo e pronto para uso.
# main.py

from fastapi import FastAPI, Query, Request
import uvicorn

app = FastAPI()

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
        print("✅ Webhook validado com sucesso!")
        return int(hub_challenge)
    return {"status": "error", "message": "Token inválido"}

# 2. Recebimento de Mensagens (POST)
@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        data = await request.json()
        print("\n📩 NOVA MENSAGEM RECEBIDA:")
        print(data) # Aqui você vê o JSON mágico
        print("-" * 30)
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
    
    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
