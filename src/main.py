import time  # Para medir tiempos de ejecución
import os  # Para manejo de archivos y carpetas
from graph_utils import leer_casos  # Función para leer grafos desde archivo
from coloring import busqueda_local, contar_conflictos, colores_usados  # Funciones del algoritmo de coloración
from visualization import crear_animacion  # Función para generar animación de la solución

# Función para guardar la solución de cada caso en un archivo de texto
def guardar_solucion(idx, colores, conflictos, tiempo, k, iteraciones):
    # Obtener la ruta del directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construir la ruta al archivo de soluciones de forma segura
    soluciones_path = os.path.join(script_dir, "..", "results", "soluciones.txt")

    # Abrir (o crear) el archivo soluciones.txt en modo añadir texto
    with open(soluciones_path, "a") as f:
        f.write(f"\n🟢 Caso {idx}\n")  # Indicar número del caso
        f.write(f"  - Colores usados: {len(set(colores.values()))} (k = {k})\n")  # Cantidad de colores usados
        f.write(f"  - Conflictos: {conflictos}\n")  # Número de conflictos (idealmente 0)
        f.write(f"  - Iteraciones: {iteraciones}\n")  # Iteraciones realizadas en búsqueda local
        f.write(f"  - Tiempo: {tiempo:.4f} segundos\n")  # Tiempo total en segundos
        # Guardar el color asignado a cada nodo, ordenado por nodo
        for nodo in sorted(colores.keys()):
            f.write(f"    Nodo {nodo}: Color {colores[nodo]}\n")

# Función principal que ejecuta todo el programa
def main():
    # Obtener la ruta del directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo con casos de prueba de forma segura
    ruta = os.path.join(script_dir, "..", "data", "casos_coloracion_grafos.txt")

    # Construir la ruta al directorio de resultados de forma segura
    results_dir = os.path.join(script_dir, "..", "results")

    # Crear la carpeta results si no existe para guardar resultados y animaciones
    os.makedirs(results_dir, exist_ok=True)

    # Construir la ruta al archivo de soluciones de forma segura
    soluciones_path = os.path.join(results_dir, "soluciones.txt")

    # Limpiar o crear el archivo soluciones.txt (sobrescribe contenido anterior)
    open(soluciones_path, "w").close()

    # Leer los casos desde el archivo, retorna una lista de grafos NetworkX
    casos = leer_casos(ruta)

    # Iterar sobre cada grafo leído, con índice comenzando en 1
    for idx, G in enumerate(casos, 1):
        print(f"\n🟢 Resolviendo Caso {idx}...")

        # Determinar el número máximo de colores posibles (k) como el grado máximo del grafo + 1
        k = max(dict(G.degree()).values()) + 1  

        mejor_solucion = None  # Variable para guardar la mejor solución sin conflictos

        # Ciclo para intentar soluciones con k colores, decreciendo k
        while k > 0:
            inicio = time.time()  # Guardar tiempo inicial

            # Ejecutar la búsqueda local con el grafo G, k colores y máximo 1000 iteraciones
            colores, pasos, iteraciones = busqueda_local(G, k, max_iter=1000)

            tiempo = time.time() - inicio  # Calcular tiempo que tardó la búsqueda

            conflictos = contar_conflictos(G, colores)  # Contar conflictos en la solución actual

            # Mostrar información del intento actual
            print(f"\n🔎 Intento con k = {k}")
            print(f"  - Conflictos: {conflictos}")
            print(f"  - Colores usados: {len(set(colores.values()))}")
            print(f"  - Iteraciones: {iteraciones}")
            print(f"  - Tiempo: {tiempo:.4f} segundos")

            # Mostrar el color asignado a cada nodo
            for nodo in sorted(G.nodes()):
                print(f"    Nodo {nodo}: Color {colores[nodo]}")

            # Si no hay conflictos, guardamos esta solución como la mejor y probamos con menos colores
            if conflictos == 0:
                mejor_solucion = (colores, pasos, tiempo, k, iteraciones)
                k -= 1  # Disminuir k para buscar solución con menos colores
            else:
                break  # Si hay conflictos, paramos y usamos la última solución sin conflictos

        # Después de probar varios k, mostrar la mejor solución encontrada sin conflictos
        if mejor_solucion:
            colores, pasos, tiempo, k_real, iteraciones = mejor_solucion
            print(f"\n✅ Solución final sin conflictos usando k = {k_real}")

            # Guardar los resultados en archivo
            guardar_solucion(idx, colores, 0, tiempo, k_real, iteraciones)

            # Crear animación mostrando el proceso de búsqueda local
            crear_animacion(G, pasos, idx, k_real)
        else:
            # Si no se encontró ninguna solución sin conflictos
            print(f"\n❌ No se encontró solución sin conflictos para el Caso {idx}")

# Este bloque ejecuta main() solo si este script se ejecuta directamente
if __name__ == "__main__":
    main()
    