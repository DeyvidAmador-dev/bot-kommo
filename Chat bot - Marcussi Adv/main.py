from flask import Flask, request, jsonify
from memoria import get_cliente, salvar_cliente
from fluxo import responder
from utils import delay
import requests

app = Flask(__name__)

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjFlYjY1OTcxOGE4MWE3OGU3ZjZmMWQzODM5NTRiMDg4NjY1YTZmMThjYmY2MWUzNzQ1NmMxMzgzYTBjMmViMDVmODk0OWFiN2ExNzMxMDA1In0.eyJhdWQiOiI1ODY4MDkwZi00YjQ5LTQwNzgtYmZiZi04ZjJhYTBhNzU5ZDYiLCJqdGkiOiIxZWI2NTk3MThhODFhNzhlN2Y2ZjFkMzgzOTU0YjA4ODY2NWE2ZjE4Y2JmNjFlMzc0NTZjMTM4M2EwYzJlYjA1Zjg5NDlhYjdhMTczMTAwNSIsImlhdCI6MTc3NjQ2NTc4NiwibmJmIjoxNzc2NDY1Nzg2LCJleHAiOjE4MDczMTUyMDAsInN1YiI6IjEzMzg2NTgzIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjM0NzYzNDU1LCJiYXNlX2RvbWFpbiI6ImtvbW1vLmNvbSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiNjJjYjBmY2QtMzQ5MS00ZjgxLWEyNTgtODA5MjQwNWQwODI4IiwiYXBpX2RvbWFpbiI6ImFwaS1jLmtvbW1vLmNvbSJ9.rE2sd1AIcpJHQfKnPsuMbJg9u42yC3pym4QOjFA_DeTHowW_5H9mpZkU4S1sNMn8kuIbCK9o3Ycn660uz3vwOud4CZ4zWFT4hRee5w9ADTxsNPXpAbOmufo50VXnbXPJMcAv5aSTVZAUotorPLgf-TFhAX94a_Ai0nDB6XqPfo3UpjUY__J_6lfcpVBQaImdysiZ2sOLZRIX1AacUeQgTOx_BVHj_5VcQ477RN0bVIncQKfw5o2FA9vCKgqwaCLL4mfihxkPt07MYtpHN4XnrYFdcgogjSCOcZXGxuTDDn9EHxIrTMiU9llnmhLdiVA2AiN3XUZ7WSv2VO4ncn-s0Q"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        data = request.form.to_dict()

    print("DATA RECEBIDA:", data)

    user_id = str(data.get("contact", {}).get("id", "1"))
    mensagem = data.get("message", {}).get("text", "")

    if data.get("is_outgoing"):
        return jsonify({"status": "ignorado"})

    cliente = get_cliente(user_id)

    resposta = responder(mensagem, cliente)

    salvar_cliente(user_id, cliente)

    delay()

    return jsonify({"status": "ok"})
