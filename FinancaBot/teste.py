import unittest
from robo import *


CONFIANCA_MINIMA = 0.50 

class TesteFinancaBot(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.robo = configurar_robo()
        
    def testar_01_saudacoes(self):

        saudacoes = ["oi", "olá", "bom dia"]
        for saudacao in saudacoes:
            resposta = self.robo.get_response(saudacao)
            print(f"Teste Saudação '{saudacao}': {resposta.text}")
            self.assertGreaterEqual(resposta.confidence, CONFIANCA_MINIMA)
            self.assertIn("FinancaBot", resposta.text)

    def testar_02_saldo(self):
        
        perguntas = ["qual é o meu saldo?", "verificar saldo disponível"]
        for p in perguntas:
            resposta = self.robo.get_response(p)
            self.assertGreaterEqual(resposta.confidence, CONFIANCA_MINIMA)
            self.assertIn("R$ 1.750,00", resposta.text)

    def testar_03_investimentos(self):
        
        perguntas = ["mostrar investimentos", "como estão meus investimentos"]
        for p in perguntas:
            resposta = self.robo.get_response(p)
            self.assertGreaterEqual(resposta.confidence, CONFIANCA_MINIMA)
            self.assertIn("Ações", resposta.text)

    def testar_04_relatorio(self):
        
        perguntas = ["gerar relatório financeiro", "resumo do mês"]
        for p in perguntas:
            resposta = self.robo.get_response(p)
            self.assertGreaterEqual(resposta.confidence, CONFIANCA_MINIMA)
            self.assertIn("Despesas", resposta.text)
            self.assertIn("Receitas", resposta.text)

if __name__ == '__main__':
    unittest.main()