import random

def contar_conflictos(G, colores):
    # Cuenta la cantidad de aristas cuyos extremos tienen el mismo color.
    # Recorre cada arista (u,v) y suma 1 si colores[u] == colores[v].
    return sum(1 for u, v in G.edges() if colores[u] == colores[v])


def busqueda_local(G, k, max_iter, registrar_pasos=False):
    """
    Búsqueda local con estrategia de *mayor mejora* (best improvement).
    Parámetros:
      - G: grafo networkx
      - k: número de colores a utilizar (0..k-1)
      - max_iter: límite de iteraciones externas
      - registrar_pasos: si True se guarda cada mejora para visualización (opcional)
    Devuelve:
      - colores: diccionario nodo->color (solución final)
      - pasos: lista de tuplas (snapshot_colores, conflictos) para animación
      - num_iteraciones: número de iteraciones externas realizadas
    """

    pasos = []  # lista para guardar snapshots (coloración, número de conflictos)
    # Asignación inicial aleatoria: cada nodo recibe un entero en 0..k-1
    colores = {n: random.randint(0, k - 1) for n in G.nodes()}
    # Calcular conflictos de la asignación inicial
    conflictos = contar_conflictos(G, colores)
    # Guardar snapshot inicial (siempre guardamos el inicial para la animación)
    pasos.append((colores.copy(), conflictos))
    num_iteraciones = 0  # contador de iteraciones externas

    # Bucle principal: máximo de 'max_iter' iteraciones externas
    for _ in range(max_iter):
        mejor_colores = colores.copy()     # copia de la coloración actual (mejor encontrada en esta iteración)
        mejor_conflictos = conflictos     # número de conflictos de la mejor_colores
        num_iteraciones += 1              # incrementamos el contador de iteraciones externas

        # Recorremos todos los nodos para buscar la mejor mejora global
        for nodo in G.nodes():
            color_original = colores[nodo]  # guardamos el color actual para restaurarlo después

            # Probar todos los colores posibles diferentes al actual
            for nuevo_color in range(k):
                # Si el nuevo color es diferente al color original del nodo
                if nuevo_color != color_original:
                    # Asignamos temporalmente el nuevo color al nodo
                    colores[nodo] = nuevo_color
                    # Calculamos cuántos conflictos hay con este cambio temporal
                    nuevos_conflictos = contar_conflictos(G, colores)

                    # Si este cambio mejora (reduce) los conflictos lo recordamos
                    if nuevos_conflictos < mejor_conflictos:
                        # Actualizamos la mejor solución encontrada dentro de esta iteración
                        mejor_conflictos = nuevos_conflictos
                        mejor_colores = colores.copy()  # guardamos la configuración completa actual

            # Restauramos el color original antes de pasar al siguiente nodo
            colores[nodo] = color_original

        # FIN del recorrido de todos los nodos: aplicamos la mejor mejora encontrada (si existe)
        if mejor_conflictos < conflictos:
            # Si encontramos reducción de conflictos, actualizamos la solución actual
            colores = mejor_colores
            conflictos = mejor_conflictos
            # Guardamos el snapshot (para animación). Respetar registrar_pasos es opcional.
            if registrar_pasos:
                pasos.append((colores.copy(), conflictos))
            else:
                # Si registrar_pasos == False igual guardamos las mejoras para la animación del proyecto
                pasos.append((colores.copy(), conflictos))
        else:
            # No se encontró ninguna mejora en toda la iteración: terminamos la búsqueda
            break

    # Devolvemos la coloración final, los pasos registrados y el número de iteraciones externas
    return colores, pasos, num_iteraciones