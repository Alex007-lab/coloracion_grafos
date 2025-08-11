# Importaciones de librerías y módulos
import time  # Módulo estándar de Python para medir el tiempo de ejecución.
import os  # Módulo estándar para interactuar con el sistema operativo (manejo de archivos y rutas).
from graph_utils import leer_casos  # Importa la función `leer_casos` para cargar datos de grafos desde un archivo.
from coloring import busqueda_local, contar_conflictos  # Importa el algoritmo de `busqueda_local` y la función para `contar_conflictos` entre nodos.
from visualization import crear_animacion  # Importa la función para generar animaciones (GIFs) del proceso de coloración.

# --- Funciones Auxiliares ---

# Función para guardar los resultados finales de cada caso de coloración en un archivo de texto.
def guardar_solucion(idx, colores, conflictos, tiempo, k, iteraciones):
    """
    Guarda los detalles de la solución de un grafo en un archivo de texto.

    Args:
        idx (int): El índice del caso de prueba.
        colores (dict): Un diccionario que mapea cada nodo a su color.
        conflictos (int): El número de conflictos en la solución final (idealmente 0).
        tiempo (float): El tiempo de ejecución del algoritmo.
        k (int): El número de colores utilizados para la coloración.
        iteraciones (int): El número de iteraciones que tomó el algoritmo.
    """
    # Obtener la ruta del directorio donde se encuentra este script (`main.py`).
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta completa al archivo de soluciones (`soluciones.txt`).
    # `os.path.join` maneja la sintaxis de rutas para diferentes sistemas operativos (`/` vs `\`).
    soluciones_path = os.path.join(script_dir, "..", "results", "soluciones.txt")

    # Abrir el archivo en modo de añadir (`"a"`), lo que permite escribir al final sin borrar el contenido anterior.
    with open(soluciones_path, "a", encoding="utf-8") as f:
        f.write(f"\n🟢 Caso {idx}\n")  # Encabezado del caso.
        f.write(f"  - Colores usados: {len(set(colores.values()))} (k = {k})\n")  # Muestra la cantidad de colores únicos usados.
        f.write(f"  - Conflictos: {conflictos}\n")  # Reporta el número de conflictos.
        f.write(f"  - Iteraciones: {iteraciones}\n")  # Reporta las iteraciones del algoritmo.
        f.write(f"  - Tiempo: {tiempo:.4f} segundos\n")  # Muestra el tiempo de ejecución con 4 decimales.
        
        # Iterar sobre los nodos ordenados para una salida consistente.
        for nodo in sorted(colores.keys()):
            f.write(f"    Nodo {nodo}: Color {colores[nodo]}\n")

# --- Función Principal ---

# Función principal que coordina la lectura de datos, la ejecución del algoritmo y el guardado de resultados.
def main():
    """
    Función principal para ejecutar el proceso de coloración de grafos.
    """
    # Obtener la ruta del directorio del script actual (`main.py`).
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo de datos de los grafos.
    ruta = os.path.join(script_dir, "..", "data", "casos_coloracion_grafos.txt")

    # Construir la ruta al directorio de resultados.
    results_dir = os.path.join(script_dir, "..", "results")

    # Crear la carpeta `results` si no existe. `exist_ok=True` evita errores si ya está creada.
    os.makedirs(results_dir, exist_ok=True)

    # Construir la ruta al archivo `soluciones.txt`.
    soluciones_path = os.path.join(results_dir, "soluciones.txt")

    # Limpiar o crear el archivo `soluciones.txt` antes de cada ejecución.
    # El modo `"w"` sobrescribe el contenido anterior.
    open(soluciones_path, "w", encoding="utf-8").close()

    # Leer todos los casos de grafos del archivo de datos.
    casos = leer_casos(ruta)

    # Iterar sobre cada grafo en la lista de casos.
    for idx, G in enumerate(casos, 1):  # `enumerate` con `start=1` numera los casos desde 1.
        print(f"\n🟢 Resolviendo Caso {idx}...")

        # Estrategia de inicialización de `k`: Se usa `grado_max + 1`.
        # El teorema de Brooks garantiza que este número de colores es suficiente
        # para colorear cualquier grafo, por lo que es un buen punto de partida.
        k = max(dict(G.degree()).values()) + 1  

        mejor_solucion = None  # Almacena la mejor solución sin conflictos encontrada.

        # Ciclo para buscar una solución óptima probando con un número decreciente de colores (`k`).
        # Comienza con un `k` alto (que garantiza una solución) y lo reduce para encontrar
        # la menor cantidad de colores posible que satisfaga la condición.
        while k > 0:
            inicio = time.time()  # Marca el tiempo de inicio para medir la duración de la búsqueda.

            # Ejecutar el algoritmo de búsqueda local.
            colores, pasos, iteraciones = busqueda_local(G, k, max_iter=1000)

            tiempo = time.time() - inicio  # Calcula el tiempo transcurrido.

            conflictos = contar_conflictos(G, colores)  # Cuenta los conflictos en la solución actual.

            # Imprimir el estado del intento actual.
            print(f"\n🔎 Intento con k = {k}")
            print(f"  - Conflictos: {conflictos}")
            print(f"  - Colores usados: {len(set(colores.values()))}")
            print(f"  - Iteraciones: {iteraciones}")
            print(f"  - Tiempo: {tiempo:.4f} segundos")

            # Muestra la asignación de colores a cada nodo.
            for nodo in sorted(G.nodes()):
                print(f"    Nodo {nodo}: Color {colores[nodo]}")

            # Condición para determinar si se encontró una solución válida.
            if conflictos == 0:
                # Si no hay conflictos, se guarda esta solución como la mejor hasta el momento.
                mejor_solucion = (colores, pasos, tiempo, k, iteraciones)
                k -= 1  # Se reduce `k` y se intenta encontrar una solución con menos colores.
            else:
                # Si se encuentran conflictos, significa que `k` es demasiado pequeño
                # y no se pudo encontrar una solución. Se rompe el ciclo y se
                # usa la última `mejor_solucion` sin conflictos.
                break

        # Una vez que el ciclo `while` termina, se procesa la mejor solución encontrada.
        if mejor_solucion:
            colores, pasos, tiempo, k_real, iteraciones = mejor_solucion
            print(f"\n✅ Solución final sin conflictos usando k = {k_real}")

            # Guardar los resultados en el archivo de soluciones.
            guardar_solucion(idx, colores, 0, tiempo, k_real, iteraciones)

            # Crear una animación del proceso de coloración.
            crear_animacion(G, pasos, idx, k_real)
        else:
            # En el caso de que no se haya encontrado ninguna solución sin conflictos.
            print(f"\n❌ No se encontró solución sin conflictos para el Caso {idx}")

# Bloque de ejecución principal.
# El código dentro de `if __name__ == "__main__":` se ejecuta solo si el script se
# corre directamente (no cuando se importa como un módulo).
if __name__ == "__main__":
    main()