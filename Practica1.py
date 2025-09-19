"""
    5BM1 Practica 1: Genetic Algorithms
    Miranda Ferreyra Uriel
    Santiago Illoldi Francisco Javier
"""
import random

# Parametros
generacion = 50
proba_cruza = 0.85
proba_mutar = 0.1
capacidad = 30
tam_poblacion = 10

class Item:
    def __init__(self, name, weight, price):
        self.name = name
        self.weight = weight
        self.price = price

lista_objetos = [
    Item("Decoy Detonators", 4, 10),
    Item("Love Potion", 2, 8),
    Item("Extendable Ears", 5, 12),
    Item("Skiving Snackbox", 5, 6),
    Item("Fever Fudge", 2, 3),
    Item("Puking Pastilles", 1.5, 2),
    Item("Nosebleed Nougat", 1, 2),

]

restricciones = {
    1: 3,   # Objeto 2 (Love Potions) minimo 3
    3: 2    # Objeto 4 (Skiving Snackbox) minimo 2
}

class Cromosoma:
    def __init__(self, lista_objetos):
        self.genes = []
        self.fitness = 0
        self.lista_objetos = lista_objetos
        self.CrearGenes()
        self.ActFitness()

    def CrearGenes(self):
        for i, _ in enumerate(self.lista_objetos):
            if i in restricciones:
                self.genes.append(random.randint(restricciones[i], 10))
            else:
                self.genes.append(random.randint(0, 10))

    def Totales(self):
        peso_total = 0
        precio_total = 0
        for i, gen in enumerate(self.genes):
            peso_total += gen * self.lista_objetos[i].weight
            precio_total += gen * self.lista_objetos[i].price
        return peso_total, precio_total
    
    def ActFitness(self):
        peso, precio = self.Totales()
        if peso > capacidad:
            self.fitness = 0
        else:
            self.fitness = precio
    
    def __lt__(self, other):
        return self.fitness < other.fitness

def VerRestricciones(cromosoma):
    for i, minimo in restricciones.items():
        if cromosoma.genes[i] < minimo:
            return False    
    return True

def GenPoblacion(cant_poblacion, lista_objetos, capacidad):
    poblacion = []
    while len(poblacion) < cant_poblacion:
        nCromosoma = Cromosoma(lista_objetos)
        peso, _ = nCromosoma.Totales()

        if peso <= capacidad and VerRestricciones:
            poblacion.append(nCromosoma) 

    return poblacion