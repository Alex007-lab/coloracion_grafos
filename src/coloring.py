import random

def contar_conflictos(G, colores):
    return sum(1 for u, v in G.edges() if colores[u] == colores[v])

def colores_usados(colores):
    return len(set(colores.values()))

def busqueda_local(G, k, max_iter, registrar_pasos=False):
    pasos = []
    colores = {n: random.randint(0, k - 1) for n in G.nodes()}
    conflictos = contar_conflictos(G, colores)
    pasos.append((colores.copy(), conflictos))
    num_iteraciones = 0

    for _ in range(max_iter):
        mejor_colores = colores.copy()
        mejor_conflictos = conflictos
        num_iteraciones += 1

        for nodo in G.nodes():
            color_original = colores[nodo]
            for nuevo_color in range(k):
                if nuevo_color != color_original:
                    colores[nodo] = nuevo_color
                    nuevos_conflictos = contar_conflictos(G, colores)
                    if nuevos_conflictos < mejor_conflictos:
                        mejor_conflictos = nuevos_conflictos
                        mejor_colores = colores.copy()
            colores[nodo] = color_original

        if mejor_conflictos < conflictos:
            colores = mejor_colores
            conflictos = mejor_conflictos
            pasos.append((colores.copy(), conflictos))
        else:
            break

    return colores, pasos, num_iteraciones
