import random  # Usamos random para generar colores aleatorios

def asignar_colores(n, k):
    # Retorna un diccionario con {nodo: color aleatorio entre 0 y k-1}
    return {i: random.randint(0, k-1) for i in range(n)}

def contar_conflictos(colores, aristas):
    # Cuenta cuántas aristas tienen el mismo color en ambos extremos (conflictos)
    return sum(1 for u, v in aristas if colores[u] == colores[v])

def busqueda_local(n, aristas, k, max_iter=1000):
    colores = asignar_colores(n, k)  # Paso 1: Asignación inicial aleatoria
    conflictos = contar_conflictos(colores, aristas)  # Evaluamos cuántos conflictos hay

    for _ in range(max_iter):  # Iteramos hasta llegar al número máximo de iteraciones
        mejor = colores.copy()  # Copia de la mejor solución encontrada hasta ahora
        mejor_conflictos = conflictos  # Número de conflictos de esa solución
        hubo_mejora = False  # Bandera para saber si encontramos una mejor solución

        for nodo in range(n):  # Probamos cambiar el color de cada nodo
            color_actual = colores[nodo]
            for nuevo_color in range(k):  # Probamos todos los colores posibles
                if nuevo_color == color_actual:
                    continue  # No tiene sentido probar el mismo color

                colores[nodo] = nuevo_color  # Aplicamos el cambio temporal
                nuevos_conflictos = contar_conflictos(colores, aristas)  # Recalculamos conflictos

                if nuevos_conflictos < mejor_conflictos:
                    # Si mejora, actualizamos mejor solución
                    mejor_conflictos = nuevos_conflictos
                    mejor = colores.copy()
                    hubo_mejora = True
            
            colores[nodo] = color_actual  # Restauramos el color original para el siguiente intento

        if not hubo_mejora:
            break  # Si en toda la iteración no hubo mejoras, detenemos la búsqueda

        # Actualizamos solución
        colores = mejor
        conflictos = mejor_conflictos

    return colores, conflictos  # Retornamos la mejor solución encontrada
