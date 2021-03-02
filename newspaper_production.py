#!/usr/bin/env python

import matplotlib.pyplot as plt
import random
import operator

PRECIO = 800       # Precio por unidad de periódico vendido
PRECIO_EXCEDENTE = 50   # Precio de venta de los periódicos excedente
COSTO = 300        # Costo de producir una unidad de periódico
MEDIA = 50000      # Demanda promedio
DESVIACION = 12500 # Desviación de la demanda
N = 50             # Días a simular
P_MINIMO = 1       # Límite inferior de la producción a simular
P_MAXIMO = 100000  # Límite superior de la producción a simular

def ganancia(P, D, precio, costo, precio_excedentes=0):
    """ Calcula la ganancia de acuerdo al las unidades producidas y las unidades vendidas. """
    if D >= P:
        return P * (precio - costo)
    else:
        return (D * precio - P * costo + precio_excedentes*(P-D))

def demanda(media, desviacion, n):
    """ Calcula la demanda siguiendo una distribución normal para la media y la desviación indicadas como argumento. """
    random.seed(0)
    D = [random.gauss(media, desviacion) for i in range(n)]
    
    return D
    
def simulacion_n(P, D, n,  media, desviacion, precio, costo, precio_excedente=0):
    """ Retorna el promedio de la ganancia para la simulación de n días. """
    G = [ganancia(P, i, precio, costo, precio_excedente) for i in D]
    return sum(G) / len(G)

def simulacion_total(P_min, P_max, n, media, desviacion, precio, costo, precio_excedente=0):
    """ Retorna una diccionario que relaciona la ganancia para cada nivel de produccion. """
    D = demanda(media, desviacion, n)
    G = {}
    for i in range(P_min, P_max + 1):
        # Genera una simulación para n días guarda el resultado como una par key:value en el diccionario G
        G[i] = simulacion_n(i, D, n, media, desviacion, precio, costo, precio_excedente)
    return G

def generar_grafica(datos_P, datos_G, p, g, nombre):
    """ Genera la gráfica de los niveles de producción y las ganancias para cada nivel de producción. """
    fg, ax = plt.subplots()
    ax.plot(datos_P, datos_G, 'bo', label='Datos')
    ax.plot(p, g, 'ro', label='Máximo')
    ax.legend()
    ax.set(xlabel='Periódicos a producir', ylabel='Ganancias (COP)', title='Resultados: ' + nombre)
    ax.grid()
    fg.savefig(nombre + ".png")

if __name__ == "__main__":
    P_G_a = simulacion_total(P_MINIMO, P_MAXIMO, N, MEDIA, DESVIACION, PRECIO, COSTO)  # Simulación caso a
    P_G_b = simulacion_total(P_MINIMO, P_MAXIMO, N, MEDIA, DESVIACION, PRECIO, COSTO, PRECIO_EXCEDENTE)    # Simulación caso b

    # Resultados simulación del caso a
    p_a, g_a  = max(P_G_a.items(), key=operator.itemgetter(1))
    print('Caso a: Se deberá producir {} unidades de periódicos generando una ganancia de {}.'.format(p_a, g_a))
    grafica_a = generar_grafica(list(P_G_a.keys()), list(P_G_a.values()),p_a, g_a, 'simulacion_a')

    # Resultados simulación del caso b
    p_b, g_b  = max(P_G_b.items(), key=operator.itemgetter(1))
    print('Caso b: Se deberá producir {} unidades de periódicos generando una ganancia de {}.'.format(p_b, g_b))
    grafica_b = generar_grafica(list(P_G_b.keys()), list(P_G_b.values()), p_b, g_b, 'simulacion_b')

    # Mostrar las gráficas
    plt.show()
    
