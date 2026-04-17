from utils import escolher, detectar_sim

def identificar_intencao(msg):
    msg = msg.lower()

    if any(p in msg for p in ["divida", "banco", "devendo"]):
        return "passivo"

    if any(p in msg for p in ["empresa", "cnpj", "abrir empresa"]):
        return "empresa"

    return "geral"


def responder(mensagem, cliente):
    msg = mensagem.lower()
    etapa = cliente.get("etapa", "inicio")

    
    if etapa == "inicio":
        cliente["intencao"] = identificar_intencao(msg)

        if cliente["intencao"] == "passivo":
            cliente["etapa"] = "pergunta_valor"
            return escolher([
                "Me conta uma coisa... você sabe mais ou menos o valor dessa dívida?",
                "Consegue me dar uma noção do valor da dívida?",
                "Sabe quanto tá aproximadamente essa dívida?"
            ])

        else:
            cliente["etapa"] = "outros_servicos"
            return escolher([
                "Perfeito! Me explica melhor o que você precisa 👇",
                "Show! Me conta mais detalhes pra eu te ajudar melhor 🙂",
                "Boa! Me fala um pouco do que você precisa"
            ])

    
    elif etapa == "pergunta_valor":
        cliente["valor"] = mensagem
        cliente["etapa"] = "pergunta_atraso"
        return escolher([
            "Entendi... essa dívida está em atraso?",
            "Ela já está atrasada ou ainda está em dia?",
            "Hoje essa dívida já está atrasada?"
        ])

    elif etapa == "pergunta_atraso":
        cliente["atraso"] = mensagem
        cliente["etapa"] = "coleta_nome"
        return escolher([
            "Perfeito. Como posso te chamar?",
            "Show! Qual seu nome?",
            "Me diz seu nome pra eu te salvar aqui 🙂"
        ])

    elif etapa == "coleta_nome":
        cliente["nome"] = mensagem
        cliente["etapa"] = "coleta_tel"
        return f"{escolher(['Prazer', 'Perfeito', 'Show'])}, {mensagem}! Pode me passar seu melhor telefone?"

    elif etapa == "coleta_tel":
        cliente["telefone"] = mensagem
        cliente["etapa"] = "final_passivo"
        return escolher([
            "Boa! Já vou encaminhar seu caso pro especialista e eles te chamam 👍",
            "Perfeito! Vou passar isso pro nosso time e já te retornam 👍",
            "Show! Agora nosso especialista pega seu caso e fala com você 👍"
        ])

    elif etapa == "outros_servicos":
        cliente["etapa"] = "tentativa_fechamento"
        return escolher([
            "Top! Já posso te explicar como funciona e te passar os próximos passos pra começar.",
            "Boa! Quer que eu te explique como funciona pra gente já iniciar?",
            "Perfeito! Posso te mostrar como funciona e já deixar tudo pronto pra você começar"
        ])

    elif etapa == "tentativa_fechamento":
        if detectar_sim(msg):
            cliente["etapa"] = "coleta_nome"
            return escolher([
                "Perfeito! Como posso te chamar?",
                "Show! Me diz seu nome 🙂",
                "Boa! Qual seu nome?"
            ])

        return escolher([
            "Sem problema! Me diz o que ficou em dúvida que eu te explico melhor 🙂",
            "Tranquilo! O que você quer entender melhor?",
            "Pode me falar sua dúvida que eu te explico 👇"
        ])

    
    return escolher([
        "Pode me explicar melhor?",
        "Não entendi muito bem, me fala de novo 🙂",
        "Me dá mais um detalhe aí 👇"
    ])
