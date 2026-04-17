clientes = {}

def get_cliente(user_id):
    return clientes.get(user_id, {
        "etapa": "inicio"
    })

def salvar_cliente(user_id, data):
    clientes[user_id] = data
