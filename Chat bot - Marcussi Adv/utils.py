import random
import time

def escolher(lista):
    return random.choice(lista)

def delay():
    time.sleep(random.uniform(1.2, 2.5))  

def detectar_sim(msg):
    return any(p in msg for p in ["sim", "quero", "bora", "fechar", "ok", "pode"])

def detectar_duvida(msg):
    return any(p in msg for p in ["como", "explica", "funciona", "valor", "preço"])
