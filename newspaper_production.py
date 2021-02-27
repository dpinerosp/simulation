#!/usr/bin/env python

import random
import matplotlib.pyplot as plt

PRECIO = 800
COSTO = 300
MEDIA = 50000
DESVIACION = 12500
N = 365
P_MINIMO = 35000
P_MAXIMO = 65000

def ganancia(P, D, precio, costo):
    """ Calcula la ganancia de acuerdo al las unidades producidas y las unidades vendidas. """
    if D >= P:
        return (P * precio - P * costo)
    else:
        return (D * precio - P * costo)

def demanda(media, desviacion):
    """ Calcula la demanda siguiendo una distribución normal para la media y la desviación indicadas como argumento. """
    return random.gauss(media, desviacion)
    
def simulacion_n(P, n,  media, desviacion, precio, costo):
    """ Retorna el promedio de la ganancia para la simulación de n días. """
    G = []
    for i in range(1, n + 1):
        D = demanda(media, desviacion)
        G.append(ganancia(P, D, precio, costo))

    return sum(G) / len(G)

def simulacion_total(P_min, P_max, n, media, desviacion, precio, costo):
    """ Retorna una diccionario que relaciona la ganancia para cada nivel de produccion. """
    G = {}
    for i in range(P_min, P_max + 1):
        # Genera una simulación para n días guarda el resultado como una par key:value en el diccionario G
        G[i] = simulacion_n(i, n, media, desviacion, precio, costo)
    return G

if __name__ == "__main__":
    P_G = simulacion_total(P_MINIMO, P_MAXIMO, N, MEDIA, DESVIACION, PRECIO, COSTO)
    datos_p = []
    datos_g = []
    p = 0    # Almacena una lista con todos los niveles de producción usados para la simulación
    g = 0    # Almacena una lista con todas las ganancias generadas para cada nivel de producción.
    
    for produccion, ganancias in P_G.items():
        datos_p.append(produccion)
        datos_g.append(ganancias)
        if ganancias > g:    # Busca ganancia máxima
            g = ganancias    # Guarda la ganancia máxima
            p = produccion   # Guarda el nivel de producción que genera la ganancia máxima
    print('Se deberá producir {} unidades de periódicos generando una ganancia de {}.'.format(p, g))

    # Configuración y generación de la gráfica.
    fig, ax = plt.subplots()
    ax.plot(datos_p, datos_g, 'bo')
    ax.set(xlabel='Periódicos a producir', ylabel='Ganancias (COP)', title='Resultados de la simulación')
    ax.grid()
    fig.savefig("simulacion.png")
    plt.show()

