from flask import Flask, request, jsonify
from memoria import get_cliente, salvar_cliente
from fluxo import responder
from utils import delay
import requests
import os

app = Flask(__name__)

# 🔒 RECOMENDADO: usar variável de ambiente no Render
TOKEN = os.getenv("KOMMO_TOKEN")

@app.route("/webhook", methods=["GET", "POST"])
@app.route("/webhooks", methods=["GET", "POST"])
def webhook():
    try:
        # 🔥 aceita qualquer formato (resolve erro 415)
        data = request.get_json(silent=True)

        if not data:
            data = request.form.to_dict() or request.args.to_dict()

        print("DADOS RECEBIDOS:", data)

        # 🔥 parsing seguro (funciona com JSON da Kommo)
        msg_data = data.get("message", {}).get("add", [{}])[0]

        mensagem = msg_data.get("text", "")
        conversation_id = msg_data.get("chat_id")
        entity_id = msg_data.get("entity_id")
        tipo = msg_data.get("type")
        user_id = msg_data.get("contact_id", "1")

        # ❌ ignora mensagens enviadas por você
        if tipo != "incoming":
            return jsonify({"status": "ignorado"})

        # 🧠 memória do cliente
        cliente = get_cliente(user_id)

        # 🤖 gera resposta
        resposta = responder(mensagem, cliente)

        salvar_cliente(user_id, cliente)

        delay()

        # 📡 envia resposta para Kommo
        url = "https://marcussiadvogados.kommo.com"

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

    except Exception as e:
        print("ERRO:", str(e))

    return "ok", 200


# 🔧 rota raiz (evita erro 404 no Render)
@app.route("/", methods=["GET"])
def home():
    return "Webhook rodando", 200


if __name__ == "__main__":
    app.run(debug=True)
