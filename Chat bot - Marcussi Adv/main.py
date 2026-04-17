from flask import Flask, request, jsonify
from memoria import get_cliente, salvar_cliente
from fluxo import responder
from utils import delay

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    user_id = str(data.get("contact", {}).get("id", "1"))
    mensagem = data.get("message", {}).get("text", "")

    if data.get("is_outgoing"):
        return jsonify({"status": "ignorado"})

    cliente = get_cliente(user_id)

    resposta = responder(mensagem, cliente)

    salvar_cliente(user_id, cliente)

    delay()

    return jsonify({"reply": resposta})
