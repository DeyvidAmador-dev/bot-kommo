from flask import Flask, request, jsonify
from memoria import get_cliente, salvar_cliente
from fluxo import responder
from utils import delay
import requests
import os

app = Flask(__name__)

# 🔐 Token (recomendado usar variável de ambiente no Render)
TOKEN = os.getenv("KOMMO_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    # 👇 aceita JSON ou FORM (Kommo envia form-data)
    data = request.get_json(silent=True)

    if not data:
        data = request.form.to_dict()

    print("DATA RECEBIDA:", data)

    try:
        # 🔥 EXTRAÇÃO CORRETA DOS DADOS (formato Kommo)
        mensagem = data.get("message[add][0][text]", "")
        conversation_id = data.get("message[add][0][chat_id]")
        entity_id = data.get("message[add][0][entity_id]")
        tipo = data.get("message[add][0][type]")
        user_id = data.get("message[add][0][contact_id]", "1")

        # ❌ ignora mensagens enviadas por você
        if tipo != "incoming":
            return jsonify({"status": "ignorado"})

        # 🧠 lógica do seu bot
        cliente = get_cliente(user_id)
        resposta = responder(mensagem, cliente)
        salvar_cliente(user_id, cliente)

        delay()

        # 🚀 envia resposta para Kommo
        url = "https://api-c.kommo.com/v4/messages"

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "message": {
                "text": resposta
            },
            "conversation_id": conversation_id,
            "entity_id": entity_id,
            "entity_type": "leads"
        }

        r = requests.post(url, json=payload, headers=headers)

        print("RESPOSTA KOMMO:", r.status_code, r.text)

        return jsonify({"status": "ok"})

    except Exception as e:
        print("ERRO:", str(e))
        return jsonify({"status": "erro", "msg": str(e)})


# 🚀 Rota de teste (pra evitar 404 na raiz)
@app.route("/", methods=["GET"])
def home():
    return "Bot Kommo rodando 🚀"


# 🔥 necessário pro Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
