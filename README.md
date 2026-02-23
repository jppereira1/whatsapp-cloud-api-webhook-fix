# 💈 Projeto Agendamento Automático (WhatsApp Cloud API + OpenAI)

Este projeto é um servidor completo em Python para criar um bot de WhatsApp inteligente usando a API oficial da Meta (WhatsApp Cloud API) e integrado com a inteligência artificial da OpenAI (ChatGPT). 
Atualmente, o bot de exemplo foi configurado para atuar como o assistente virtual da barbearia **"Cortes do Fabio"**, respondendo a perguntas sobre preços e agendamentos de forma rápida, amigável e concisa.

Além do bot, o repositório conta com um script complementar para corrigir problemas comuns de não-recebimento de mensagens na API da Meta.

## 🚀 Funcionalidades

- **`main.py` (O Core do Bot):** 
  - Servidor construído com **FastAPI** expondo a rota `/webhook` (`GET` para validação da Meta e `POST` para recebimento de mensagens).
  - Integração nativa com a OpenAI (`gpt-3.5-turbo`) através de um *System Prompt* facilmente personalizável.
  - Tratamento e ajuste automático de números de telefone brasileiros (adiciona o 9º dígito automaticamente para evitar erro no envio da resposta).
  - Envio de mensagens assíncronas de texto diretas para os clientes utilizando a WhatsApp Cloud API.

- **`subscribe_fix.py` (O Corretor de Conexão Webhook da Meta):**
  - Script para forçar a vinculação/assinatura do seu Aplicativo Meta à sua WABA (*WhatsApp Business Account*).
  - Resolve o famoso problema em que testes sintéticos da plataforma funcionam, mas mensagens enviadas de celulares reais são "silenciosamente ignoradas".

## 🛠️ Dependências e Instalação

As principais bibliotecas usadas no projeto são:
- `fastapi` e `uvicorn` (Para manter a API no ar)
- `requests` (Para comunicação HTTP simplificada com os servidores do Facebook)
- `openai` (Para gerar as respostas inteligentes)
- `python-dotenv` (Para o carregamento seguro de chaves de API a partir de um arquivo `.env`)

### 1. Clonando e instalando

No seu terminal ou ambiente (como o GitHub Codespaces), instale as bibliotecas executando:

```bash
pip install fastapi uvicorn requests python-dotenv openai
```

### 2. Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes chaves de ambiente:

```env
# Chaves da Meta (WhatsApp Cloud API)
WHATSAPP_TOKEN=seu_token_de_acesso_temporario_ou_permanente
PHONE_ID=seu_id_do_numero_de_telefone
API_VERSION=v25.0

# Chave da OpenAI
OPENAI_API_KEY=sua_secret_key_da_openai
```

> ⚠️ **Atenção:** Em `main.py` também existe a variável `VERIFY_TOKEN = "seu_token_secreto"`. Altere-a e utilize a mesma senha no momento de configurar o Webhook no painel da Meta!

### 3. Rodando o Bot

Inicie o servidor local através do Python:

```bash
python main.py
```
*(O Bot ficará escutando na porta `8000` em `http://0.0.0.0:8000`)*. 
Certifique-se de que este projeto está acessível publicamente na internet para a Meta poder enviar o webhook (ex: usando um túnel reverso, hospedagem em nuvem ou a URL pública de um Codespace).

### 4. Meu Webhook validou, mas não recebo as mensagens reais! O que faço?

Se o seu webhook retornar sucesso, mas as mensagens do celular não geram requisições para o seu código:

1. Abra o arquivo `subscribe_fix.py`.
2. Pegue o seu **Identificador da Conta do WhatsApp (WABA ID)** no painel de desenvolvedores da Meta e cole na variável:
   ```python
   WABA_ID = "COLE_SEU_ID_DA_CONTA_AQUI"
   ```
3. Rode o script uma vez no seu terminal:
   ```bash
   python subscribe_fix.py
   ```
4. Se ele exibir `✅ SUCESSO! A conexão foi restabelecida.`, significa que a API da Meta ativou à força a inscrição de mensagens. Tente mandar uma mensagem pelo WhatsApp novamente!

---

## 🤖 Como Treinar ou Alterar a Personalidade do Bot

Toda a regra de negócio da IA fica dentro do arquivo `main.py`, na função `consultar_ia`.
Basta modificar o texto da mensagem com o *role* `system`. Esse texto funciona como o cérebro/comportamento inicial do seu Bot:

```python
{"role": "system", "content": """
Você é o assistente virtual da barbearia 'Cortes do Fabio'.
Seja amigável, direto e use um tom natural e conversacional.
Se o cliente perguntar preços: Corte R$50, Barba R$30.
"""}
```

O chatbot já tem uma lógica inteligente em que você mesmo define suas instruções neste formato direto.
