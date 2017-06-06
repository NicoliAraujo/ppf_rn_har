from sklearn.neural_network.multilayer_perceptron import MLPClassifier as MLPC
import pandas as pd


class RedesNeurais:
    def __init__(self, min, max, nome):
        self.min = min
        self.max = max
        self.nome = nome
        self.camadas = self.set_camadas()
        self.redes = self.set_redes()

    def set_camadas(self):
        camadas = [(i, self.max - i) for i in range(self.min, self.max - self.min + 1)]
        for i in range(self.min, self.max + 1):
            camadas.append((i,))
        return camadas

    def set_redes(self):
        redes = []
        for camada in self.camadas:
            for funcaoAtiv in ['logistc', 'tanh']:
                for taxaApren in [0.001, 0.003]:
                    redes.append(MLPC(hidden_layer_sizes=camada, activation=funcaoAtiv, solver='sgd',
                                      learning_rate='adaptive', shuffle=False,
                                      learning_rate_init=taxaApren, early_stopping=True))
        return redes

    def salvar(self):
        dic = {'Camadas': [self.redes[i].hidden_layer_sizes for i in range(0, len(self.redes))],
               'FuncAtic': [self.redes[i].activation for i in range(0, len(self.redes))],
               'TaxaApren': [self.redes[i].learning_rate_init for i in range(0, len(self.redes))]}
        dv = pd.DataFrame(dic)
        dv.to_csv("redes_"+self.nome+".csv")


class ConjuntoDados:
    def __init__(self):
        self.entrada_treinamento = []
        self.saida_treinamento = []
        self.entrada_teste = []
        self.saida_teste = []

r = RedesNeurais(9, 38, "1000ms")
r.salvar()
print('ok')