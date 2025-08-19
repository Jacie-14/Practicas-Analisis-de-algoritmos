import numpy as np

def generar_lista(size):
    return np.random.randint(1, 200001, size).tolist() 

def busqueda_lineal(lista, x):
    for i in range(len(lista)):
        if lista[i] == x:
            return i
    return -1

def busqueda_binaria(lista, x):
    left, right = 0, len(lista) - 1  
    while left <= right:
        mid = left + (right - left) // 2  
        if lista[mid] == x:
            return mid  
        elif lista[mid] < x: 
            left = mid + 1  
        else: 
            right = mid - 1  
    return -1 
