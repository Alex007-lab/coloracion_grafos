# Importaciones de librerías y módulos
import time  # Módulo estándar para medir el tiempo de ejecución.
import os  # Módulo para interactuar con el sistema operativo (manejo de archivos y rutas).
import sys  # Módulo que proporciona acceso a parámetros del sistema, como `sys.stdout`.
from graph_utils import leer_casos  # Importa la función para cargar datos de grafos.
from coloring import busqueda_local, contar_conflictos  # Algoritmo de coloración y función para contar conflictos.
from visualization import crear_animacion  # Función para generar animaciones (GIFs).

# --- Clase Logger para capturar la salida en archivo y consola ---
class Logger:
    """
    Clase que redirige la salida estándar (sys.stdout) a la consola y a un archivo de texto.
    Esto permite registrar todo lo que se imprime sin la necesidad de llamar a una función
    de guardado explícitamente.
    """
    def __init__(self, filename):
        """
        Inicializa el Logger, guardando la referencia a la salida original y abriendo el archivo.
        
        Args:
            filename (str): La ruta del archivo donde se guardará la salida.
        """
        self.terminal = sys.stdout  # Guarda la referencia a la salida estándar original.
        self.log = open(filename, "w", encoding="utf-8") # Abre el archivo en modo de escritura.

    def write(self, message):
        """
        Método que se llama automáticamente cuando se usa `print`.
        Redirige el mensaje a la consola y al archivo.
        """
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        """
        Método necesario para vaciar los buffers de escritura.
        Garantiza que el contenido se escriba en el archivo de forma inmediata.
        """
        self.terminal.flush()
        self.log.flush()

# --- Función para imprimir solución ---
def guardar_solucion(idx, colores, conflictos, tiempo, k, iteraciones):
    """
    Imprime los detalles de la solución final. La salida se registra
    automáticamente en el archivo de soluciones gracias al Logger.
    """
    print(f"\n🟢 Caso {idx}")
    print(f"  - Colores usados: {len(set(colores.values()))} (k = {k})")
    print(f"  - Conflictos: {conflictos}")
    print(f"  - Iteraciones: {iteraciones}")
    print(f"  - Tiempo: {tiempo:.4f} segundos")
    for nodo in sorted(colores.keys()):
        print(f"    Nodo {nodo}: Color {colores[nodo]}")

# --- Función principal ---
def main():
    """
    Función principal que coordina la carga de datos, la ejecución del algoritmo
    de coloración de grafos y la visualización de los resultados.
    """
    # Obtiene la ruta del directorio del script para construir rutas relativas.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construye las rutas a los archivos y directorios de entrada y salida.
    ruta = os.path.join(script_dir, "..", "data", "casos_coloracion_grafos.txt")
    results_dir = os.path.join(script_dir, "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    soluciones_path = os.path.join(results_dir, "soluciones.txt")

    # Redirige la salida estándar a una instancia de la clase Logger.
    sys.stdout = Logger(soluciones_path)

    casos = leer_casos(ruta)

    # Bucle principal para procesar cada caso de grafo.
    for idx, G in enumerate(casos, 1):
        print(f"\n🟢 Resolviendo Caso {idx}...")

        # Información del grafo para la estrategia de coloración.
        grados = dict(G.degree())
        print(f"📊 Grados de los nodos: {grados}")
        grado_max = max(grados.values())
        print(f"📈 Grado máximo: {grado_max}")

        # Se establece el valor inicial de `k` (número de colores) basándose en el Teorema de Brooks.
        k = grado_max + 1
        print(f"🎯 k inicial calculado: {k}")

        mejor_solucion = None
        pasos_totales = []  # Lista para almacenar todos los pasos de la animación.

        # Bucle para encontrar la coloración óptima (mínimo de colores).
        while k > 0:
            inicio = time.time()
            # `busqueda_local` devuelve una lista de pasos: `(colores, conflictos)`.
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

            # Acumula los pasos de cada ejecución de `busqueda_local` en una lista global.
            for i, (col, conf) in enumerate(pasos):
                descripcion = f"Iteración {i} con k={k} - Conflictos: {conf}"
                # Almacena el estado completo para la animación.
                # Es crucial usar `.copy()` para evitar que los cambios posteriores afecten a los pasos ya guardados.
                pasos_totales.append((col.copy(), conf, k, descripcion))

            if conflictos == 0:
                # Si se encuentra una solución sin conflictos, se guarda como la mejor.
                # Se usa `colores.copy()` para asegurar que se almacena una copia inmutable.
                mejor_solucion = (colores.copy(), tiempo, k, iteraciones)
                k -= 1  # Intenta con un número menor de colores.
            else:
                # Si hay conflictos, este `k` es demasiado bajo. El algoritmo termina.
                break

        # Procesa y guarda la mejor solución encontrada.
        if mejor_solucion:
            colores, tiempo, k_real, iteraciones = mejor_solucion
            print(f"\n✅ Solución final sin conflictos usando k = {k_real}")
            guardar_solucion(idx, colores, 0, tiempo, k_real, iteraciones)

            # Agrega un paso final explícito a la animación para mostrar el estado de la solución final.
            pasos_totales.append((colores.copy(), 0, k_real, "Solución final sin conflictos"))

            # Se llama a la función de animación con la lista completa de pasos.
            # `crear_animacion` recibe una lista de tuplas con 4 elementos.
            crear_animacion(G, pasos_totales, idx)
        else:
            print(f"\n❌ No se encontró solución sin conflictos para el Caso {idx}")

# El bloque `if __name__ == "__main__":` asegura que el código principal
# solo se ejecute cuando el script es el programa principal.
if __name__ == "__main__":
    main()