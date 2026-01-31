from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

import json

CONVERSAS = [
    "conversas\saudacoes.json",
    "conversas/financas.json",
]

NOME_ROBO = "FinancaBot"
CONFIANCA_MINIMA = 0.60

def configurar_treinador():
    robo = ChatBot(NOME_ROBO)
    treinador = ListTrainer(robo)
    
    return treinador

def carregar_conversar():
    conversas = []
    
    for arquivo_conversa in CONVERSAS:
        with open(arquivo_conversa, "r", encoding="utf-8") as arquivo:
            conversas.append(json.load(arquivo)["conversas"])
            
            arquivo.close()
    
    return conversas

def treinar(treinador, conversas):
    for conversa in conversas:
        for mensagens_resposta in conversa:
            mensagens = mensagens_resposta["mensagens"]
            resposta = mensagens_resposta["resposta"]
            
            for mensagem in mensagens:
                print(f"treinando mensagem: '{mensagem}', reposta: '{resposta}'")
                treinador.train([mensagem.lower(), resposta])
                
if __name__ == "__main__":
    treinador = configurar_treinador()
    conversas = carregar_conversar()
    
    if treinador and conversas:
        treinar(treinador, conversas)