from flask import Flask, request, jsonify
from memoria import get_cliente, salvar_cliente
from fluxo import responder
from utils import delay
import requests

app = Flask(__name__)

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijg4MzRlNTIxY2RmNWFmMzAzMzhlY2IyNTZlZTRhZDFjYjJiZGRiODMxMGU1NjAzZjE4MWFlZDA4MjBkMzg1NjY1NDQyNDM5YWFkYjRlNjU5In0.eyJhdWQiOiI1ODY4MDkwZi00YjQ5LTQwNzgtYmZiZi04ZjJhYTBhNzU5ZDYiLCJqdGkiOiI4ODM0ZTUyMWNkZjVhZjMwMzM4ZWNiMjU2ZWU0YWQxY2IyYmRkYjgzMTBlNTYwM2YxODFhZWQwODIwZDM4NTY2NTQ0MjQzOWFhZGI0ZTY1OSIsImlhdCI6MTc3NjQ3NzEzMSwibmJmIjoxNzc2NDc3MTMxLCJleHAiOjE4MDc5MjAwMDAsInN1YiI6IjEzMzg2NTgzIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjM0NzYzNDU1LCJiYXNlX2RvbWFpbiI6ImtvbW1vLmNvbSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiMWZkN2MyZWEtYzFhYi00ZjJkLTk0YzItMWZhYWQ2ODZlYmJhIiwiYXBpX2RvbWFpbiI6ImFwaS1jLmtvbW1vLmNvbSJ9.h4eNfYIrAhZ9oKRQFjdMf0bZHwHwkfv4OUEm0J-iGA1pYnFV4EyzidD7aCBGixMRgab9aiEYnbKCMmXPpKpna-sMec3p1Snu2qzMIZi2HPzYEG61bCcjjI8K0qBIq8wyqxWUqw5sEqJDCtyQgyoOl5dDJkrpFNu6yRIiW4XRY2__TXkSh8qj8FQC8CbIcDglEFGL3_bDGDVkHXGlZ54hvt8A4dk370CHXQg7L-6UrTFyIR2XyS-kVgxa3DMnB-gA0oc4WORCi_T6ceoQvXTKEJ8lBIUxRuBcZylaz8rJ7TpDsHCghDhbN29qqTZPzGNP1tq3ndvMc8It6NQzVEq12Q"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        data = request.form.to_dict()

    print("DATA RECEBIDA:", data)

    mensagem = data.get("message[add][0][text]", "")
    conversation_id = data.get("message[add][0][chat_id]")
    entity_id = data.get("message[add][0][entity_id]")
    tipo = data.get("message[add][0][type]")

    # 🔥 IGNORA mensagens suas
    if tipo != "incoming":
        return jsonify({"status": "ignorado"})

    user_id = data.get("message[add][0][contact_id]", "1")

    cliente = get_cliente(user_id)

    resposta = responder(mensagem, cliente)

    salvar_cliente(user_id, cliente)

    delay()

    # 🔥 ENVIA RESPOSTA PRA KOMMO
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
