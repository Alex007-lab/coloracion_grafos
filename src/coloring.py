import random

def contar_conflictos(G, colores):
    # Cuenta la cantidad de aristas cuyos extremos tienen el mismo color.
    # Recorre cada arista (u,v) y suma 1 si colores[u] == colores[v].
    return sum(1 for u, v in G.edges() if colores[u] == colores[v])


def busqueda_local(G, k, max_iter, registrar_pasos=True):
    """
    Implementa el algoritmo de Búsqueda Local con estrategia de mayor mejora.

    El algoritmo busca una solución óptima para el problema de coloración de grafos
    reduciendo iterativamente el número de conflictos (aristas con nodos del mismo color).

    Parámetros:
      - G: El grafo de entrada, representado como un objeto de NetworkX.
      - k: El número máximo de colores disponibles para la coloración (los colores se
           representan como enteros de 0 a k-1).
      - max_iter: Límite de iteraciones externas. El algoritmo se detendrá si alcanza
                  este número de iteraciones o si no puede encontrar una mejora.
      - registrar_pasos: Un booleano opcional. Si es True, el algoritmo guarda
                         cada mejora de la solución en la lista `pasos`, lo cual
                         es útil para la visualización del proceso.

    Devuelve:
      - colores: Un diccionario que mapea cada nodo a su color final.
      - pasos: Una lista de tuplas `(colores, conflictos)` que representan los estados
               mejorados de la coloración a lo largo del proceso. Esta lista se usa
               para crear la animación.
      - num_iteraciones: El número de iteraciones completadas antes de que el algoritmo
                         se detuviera.
    """

    # Agregado: Inicialización de la lista de pasos para la visualización
    pasos = []  # Almacena los "snapshots" (coloración y número de conflictos) en cada mejora.
    
    # Asignación inicial aleatoria de colores a cada nodo. Cada nodo recibe un
    # color aleatorio en el rango [0, k-1].
    colores = {n: random.randint(0, k - 1) for n in G.nodes()}
    
    # Se calculan los conflictos iniciales de la coloración aleatoria.
    conflictos = contar_conflictos(G, colores)
    
    # Se registra el estado inicial del grafo (coloración y conflictos)
    # como el primer paso para la animación.
    pasos.append((colores.copy(), conflictos))
    num_iteraciones = 0  # Contador de iteraciones externas.

    # Bucle principal de la búsqueda local. Continúa mientras no se alcance el
    # límite de iteraciones o no se encuentre una solución mejor.
    for _ in range(max_iter):
        mejor_colores = colores.copy()     # Copia de la coloración actual, que será la mejor candidata en esta iteración.
        mejor_conflictos = conflictos      # El número de conflictos actual.
        num_iteraciones += 1              # Se incrementa el contador de iteraciones externas.

        # Se recorren todos los nodos para encontrar la mejor mejora global.
        # Una "mejora" es un cambio de color en un solo nodo que reduce el total de conflictos.
        for nodo in G.nodes():
            color_original = colores[nodo]  # Se guarda el color original del nodo.

            # Se prueban todos los colores posibles para el nodo actual.
            for nuevo_color in range(k):
                # Si el nuevo color es diferente al color actual del nodo...
                if nuevo_color != color_original:
                    # Se asigna temporalmente el nuevo color al nodo para evaluarlo.
                    colores[nodo] = nuevo_color
                    # Se calcula el número de conflictos con este cambio.
                    nuevos_conflictos = contar_conflictos(G, colores)

                    # Si el nuevo estado tiene menos conflictos que la mejor opción
                    # encontrada hasta ahora en esta iteración...
                    if nuevos_conflictos < mejor_conflictos:
                        # Se actualiza la mejor solución encontrada en la iteración.
                        mejor_conflictos = nuevos_conflictos
                        mejor_colores = colores.copy()  # Se guarda una copia completa de la solución mejorada.

            # Se restaura el color original del nodo para no afectar las
            # evaluaciones de los otros nodos en la iteración actual.
            colores[nodo] = color_original

        # Al final de la iteración, se aplica el mejor cambio de color encontrado.
        if mejor_conflictos < conflictos:
            # Si se encontró una mejora, se actualiza la solución principal.
            colores = mejor_colores
            conflictos = mejor_conflictos
            
            # Se registra este nuevo estado de la solución en la lista de pasos.
            # Esta condición ya no es necesaria, ya que `registrar_pasos` ahora
            # es `True` por defecto para la animación del proyecto.
            # Agregado: Se guarda el snapshot de la mejora.
            pasos.append((colores.copy(), conflictos))
            
        else:
            # No se encontró ninguna mejora en toda la iteración.
            # El algoritmo ha llegado a un óptimo local y se detiene.
            break

    # Se devuelve la coloración final, la lista de pasos para la animación y el
    # número de iteraciones realizadas.
    return colores, pasos, num_iteraciones