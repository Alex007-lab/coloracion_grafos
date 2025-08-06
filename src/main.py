import time
import os
from graph_utils import leer_casos
from coloring import busqueda_local, contar_conflictos, colores_usados
from visualization import crear_animacion

def guardar_solucion(idx, colores, conflictos, tiempo, k, iteraciones):
    with open("../results/soluciones.txt", "a") as f:
        f.write(f"\n🟢 Caso {idx}\n")
        f.write(f"  - Colores usados: {len(set(colores.values()))} (k = {k})\n")
        f.write(f"  - Conflictos: {conflictos}\n")
        f.write(f"  - Iteraciones: {iteraciones}\n")
        f.write(f"  - Tiempo: {tiempo:.4f} segundos\n")
        for nodo in sorted(colores.keys()):
            f.write(f"    Nodo {nodo}: Color {colores[nodo]}\n")
def main():
    ruta = "../data/casos_coloracion_grafos.txt"
    os.makedirs("results", exist_ok=True)
    open("../results/soluciones.txt", "w").close()

    casos = leer_casos(ruta)

    for idx, G in enumerate(casos, 1):
        print(f"\n🟢 Resolviendo Caso {idx}...")
        k = len(G.nodes())
        mejor_solucion = None

        while k > 0:
            inicio = time.time()
            colores, pasos, iteraciones = busqueda_local(G, k, max_iter=1000)
            tiempo = time.time() - inicio
            conflictos = contar_conflictos(G, colores)

            print(f"\n🔎 Intento con k = {k}")
            print(f"  - Conflictos: {conflictos}")
            print(f"  - Colores usados: {len(set(colores.values()))}")
            print(f"  - Iteraciones: {iteraciones}")
            print(f"  - Tiempo: {tiempo:.4f} segundos")

            for nodo in sorted(G.nodes()):
                print(f"    Nodo {nodo}: Color {colores[nodo]}")

            if conflictos == 0:
                mejor_solucion = (colores, pasos, tiempo, k, iteraciones)
                k -= 1
            else:
                break  # Último intento sin conflictos ya está en mejor_solucion

        # Mostrar solo la mejor solución sin conflictos
        if mejor_solucion:
            colores, pasos, tiempo, k_real, iteraciones = mejor_solucion
            print(f"\n✅ Solución final sin conflictos usando k = {k_real}")
            guardar_solucion(idx, colores, 0, tiempo, k_real, iteraciones)
            crear_animacion(G, pasos, idx, k_real)
        else:
            print(f"\n❌ No se encontró solución sin conflictos para el Caso {idx}")


if __name__ == "__main__":
    main()
