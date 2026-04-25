from flask import Flask, request, jsonify
from memoria import get_cliente, salvar_cliente
from fluxo import responder
from utils import delay
import requests

app = Flask(__name__)

# 🔑 TOKEN DIRETO (sem variável de ambiente)
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImMxMzJjMzhlMjYxYmVhNGFjNjJiZDRmZTk0OGJjNzhiZmMzNzVhMjI3MGQwNDZiYzMyZGY4OTEzOWQ4NGIzZjRlNzlmZTQ4MzhjYWY2M2Y4In0.eyJhdWQiOiI1ODY4MDkwZi00YjQ5LTQwNzgtYmZiZi04ZjJhYTBhNzU5ZDYiLCJqdGkiOiJjMTMyYzM4ZTI2MWJlYTRhYzYyYmQ0ZmU5NDhiYzc4YmZjMzc1YTIyNzBkMDQ2YmMzMmRmODkxMzlkODRiM2Y0ZTc5ZmU0ODM4Y2FmNjNmOCIsImlhdCI6MTc3Njk2NzY5MiwibmJmIjoxNzc2OTY3NjkyLCJleHAiOjE4MDM2MDAwMDAsInN1YiI6IjEzMzg2NTgzIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjM0NzYzNDU1LCJiYXNlX2RvbWFpbiI6ImtvbW1vLmNvbSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiZGUwN2YyYzktNzFmZC00NmU0LTlhNTEtNGQ3MDk5MzYyYWRlIiwiYXBpX2RvbWFpbiI6ImFwaS1jLmtvbW1vLmNvbSJ9.h7fYq2JwgzUEbM_q3giETLU1Rm3J0Y8qiYz6x-5aCPmTRJy6VoUvLYKbjQfqFFRRckuUfvEZkZExJXL3l0PAceB0bg98R9iyONzh26mgo31pWcX7bicBSZbfrc0OboXn5yJp4spz056SY-uD5rC4K8r0SgVGkExGSzKRUDVNL9cynUpibWLFYuQx7xPDjo1rlanJzGfjyI1e8sFcQw5S2c7jnjki-JkrTIn8OwSNYv2otoDMLeuToH2r405fi5NyXQ0PZCD1CtqEwZjm1AkpEXNsO6cSZMcI1MjByCZN2zOXad6P1czf_SWdIj-WNpKQM_SR_eK4nNWhezGNYfFxZA"

@app.route("/webhook", methods=["GET", "POST"])
@app.route("/webhooks", methods=["GET", "POST"])
def webhook():
    try:
        data = request.get_json(silent=True)

        if not data:
            data = request.form.to_dict() or request.args.to_dict()

        print("DADOS RECEBIDOS:", data)

        # ✅ parsing correto da Kommo
        mensagem = data.get("message[add][0][text]")
        conversation_id = data.get("message[add][0][chat_id]")
        entity_id = data.get("message[add][0][entity_id]")
        tipo = data.get("message[add][0][type]")
        user_id = data.get("message[add][0][contact_id]", "1")

        print("mensagem:", mensagem)
        print("conversation_id:", conversation_id)

        if tipo != "incoming":
            return jsonify({"status": "ignorado"})

        if not mensagem or not conversation_id:
            print("Dados incompletos")
            return jsonify({"status": "erro_dados"}), 400

        cliente = get_cliente(user_id)
        resposta = responder(mensagem, cliente)
        salvar_cliente(user_id, cliente)

        delay()

        # ✅ endpoint correto
        url =  "https://marcussiadvogados.kommo.com/api/v4/leads/messages"

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }

        # ✅ payload correto
        payload = {
            "conversation_id": conversation_id,
            "text": resposta
        }

        r = requests.post(url, json=payload, headers=headers)

        print("RESPOSTA KOMMO:", r.status_code, r.text)

    except Exception as e:
        print("ERRO:", str(e))

    return "ok", 200


@app.route("/", methods=["GET"])
def home():
    return "Webhook rodando", 200


if __name__ == "__main__":
    app.run(debug=True)
