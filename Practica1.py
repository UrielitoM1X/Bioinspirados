"""
    5BM1 - Practica 1: Algoritmos geneticos
    Miranda Ferreyra Uriel
    Santiago Illoldi Francisco Javier
"""

# Imports
import random

""""Definicion de elementos a usar"""
# Productos
productos = [
    {"nombre": "Decoy Detonators", "peso": 4, "precio": 10},
    {"nombre": "Love Potion", "peso": 2, "precio": 8},
    {"nombre": "Extendable Ears", "peso": 5, "precio": 12},
    {"nombre": "Skiving Snackbox", "peso": 5, "precio": 6},
    {"nombre": "Fever Fudge", "peso": 2, "precio": 3},
    {"nombre": "Puking Pastilles", "peso": 1.5, "precio": 2},
    {"nombre": "Nosebleed Nougat", "peso": 1, "precio": 2},
]

# Parametros
capacidad = 30
poblacion = 10
generacion = 50
proba_cruza = 0.85
proba_mutar = 0.1

# Restricciones
Love_min = 3
Skiving_min = 2