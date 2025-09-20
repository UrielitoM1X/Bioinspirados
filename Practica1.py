"""
    5BM1 Practica 1: Genetic Algorithms
    Miranda Ferreyra Uriel
    Santiago Illoldi Francisco Javier
"""

import random

generacion = 50
proba_cruza = 0.85
proba_mutar = 0.1
capacidad_mochila = 30
tam_poblacion = 10
max_generaciones_sin_mejora = 5

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
        if peso > capacidad_mochila:
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
        
        if peso <= capacidad and VerRestricciones(nCromosoma) and nCromosoma.fitness > 0:
            poblacion.append(nCromosoma)
    
    return poblacion

def Ruleta(poblacion):
    fitness_total = sum(cromosoma.fitness for cromosoma in poblacion)
    if fitness_total == 0:
        return random.choice(poblacion)
    
    pick = random.uniform(0, fitness_total)
    current = 0
    for cromosoma in poblacion:
        current += cromosoma.fitness
        if current > pick:
            return cromosoma
    return poblacion[-1]

def CruzaUnif(padre1, padre2):
    if random.random() > proba_cruza:
        return padre1, padre2
    
    hijo1_genes = []
    hijo2_genes = []
    
    for i in range(len(padre1.genes)):
        if random.random() < 0.5:
            hijo1_genes.append(padre1.genes[i])
            hijo2_genes.append(padre2.genes[i])
        else:
            hijo1_genes.append(padre2.genes[i])
            hijo2_genes.append(padre1.genes[i])
    
    hijo1 = Cromosoma(lista_objetos)
    hijo1.genes = hijo1_genes
    hijo1.ActFitness()
    
    hijo2 = Cromosoma(lista_objetos)
    hijo2.genes = hijo2_genes
    hijo2.ActFitness()
    
    return hijo1, hijo2

def MutarUnif(cromosoma):
    genes_mutados = cromosoma.genes.copy()
    
    for i in range(len(genes_mutados)):
        if random.random() < proba_mutar:
            if i in restricciones:
                genes_mutados[i] = random.randint(restricciones[i], 10)
            else:
                genes_mutados[i] = random.randint(0, 10)
    
    nuevo_cromosoma = Cromosoma(lista_objetos)
    nuevo_cromosoma.genes = genes_mutados
    nuevo_cromosoma.ActFitness()
    
    return nuevo_cromosoma

def torneo_padres_hijos(padre1, padre2, hijo1, hijo2):
    candidatos = [padre1, padre2, hijo1, hijo2]
    candidatos.sort(reverse=True, key=lambda x: x.fitness)
    return candidatos[0], candidatos[1]

def AlgGenetico():
    poblacion = GenPoblacion(tam_poblacion, lista_objetos, capacidad_mochila)
    mejor_solucion = max(poblacion)
    
    print(f"Generacion 0 - Fitness: {mejor_solucion.fitness}")
    
    generaciones_sin_mejora = 0
    mejor_fitness_global = mejor_solucion.fitness

    for gen in range(generacion):
        nueva_poblacion = []
        nueva_poblacion.append(mejor_solucion)
        
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = Ruleta(poblacion)
            padre2 = Ruleta(poblacion)
            
            hijo1, hijo2 = CruzaUnif(padre1, padre2)
            
            hijo1 = MutarUnif(hijo1)
            hijo2 = MutarUnif(hijo2)
            
            seleccionado1, seleccionado2 = torneo_padres_hijos(padre1, padre2, hijo1, hijo2)
            
            if (VerRestricciones(seleccionado1) and 
                seleccionado1.Totales()[0] <= capacidad_mochila and 
                seleccionado1.fitness > 0 and
                len(nueva_poblacion) < tam_poblacion):
                nueva_poblacion.append(seleccionado1)
            
            if (VerRestricciones(seleccionado2) and 
                seleccionado2.Totales()[0] <= capacidad_mochila and 
                seleccionado2.fitness > 0 and
                len(nueva_poblacion) < tam_poblacion):
                nueva_poblacion.append(seleccionado2)
        
        poblacion = nueva_poblacion
        mejor_actual = max(poblacion)
        
        print(f"Generacion {gen+1} - Fitness: {mejor_actual.fitness}")
        
        if mejor_actual.fitness > mejor_solucion.fitness:
            mejor_solucion = mejor_actual
            mejor_fitness_global = mejor_solucion.fitness
            generaciones_sin_mejora = 0
        else:
            generaciones_sin_mejora += 1
        
        if generaciones_sin_mejora >= max_generaciones_sin_mejora:
            print(f"No hay mejora {gen+1}")
            break
    
    return mejor_solucion

def Solucion(solucion):
    print("\n" + "="*45)
    print("MEJOR SOLUCION:")
    print("="*45)
    
    peso_total, precio_total = solucion.Totales()
    
    for i, gen in enumerate(solucion.genes):
        if gen > 0:
            objeto = lista_objetos[i]
            print(f"{objeto.name}: {gen} unidades")
    
    print("-"*60)
    print(f"Peso total: {peso_total} pounds")
    print(f"Precio total: {precio_total} galleons")
    print(f"Fitness: {solucion.fitness}")
    print("="*60)

mejor = AlgGenetico()
Solucion(mejor)