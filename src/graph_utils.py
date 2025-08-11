import os  # Módulo para manejo de archivos y directorios
import networkx as nx  # Librería para crear y manipular grafos. Es ideal para representar estructuras de datos como redes.
import logging  # Módulo para registrar eventos y errores. Es muy útil para depurar y rastrear el comportamiento del programa.

# --- Configuración Inicial del Proyecto y Logs ---

# Obtener la ruta del directorio del script actual. Esto es crucial para
# asegurar que las rutas relativas funcionen sin importar desde dónde se
# ejecute el script.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta al directorio 'results' de forma segura.
results_dir = os.path.join(script_dir, "..", "results")

# Crear la carpeta "results" si no existe. El argumento `exist_ok=True` evita
# que el programa genere un error si el directorio ya existe.
os.makedirs(results_dir, exist_ok=True)

# Construir la ruta al archivo de log.
log_path = os.path.join(results_dir, "errores.log")

# Configurar el logger para que guarde mensajes en un archivo de log.
logging.basicConfig(
    filename=log_path,  # Archivo donde se guardarán los mensajes de registro.
    filemode="w",  # Modo de escritura 'w' para sobrescribir el archivo cada vez que
                   # se ejecuta el programa. Esto asegura que el log esté siempre
                   # actualizado y sin información de ejecuciones anteriores.
    level=logging.INFO,  # Nivel mínimo de mensajes que se registran. `INFO` es
                         # un buen balance para reportar eventos importantes. Otros
                         # niveles son DEBUG, WARNING, ERROR y CRITICAL.
    format="%(asctime)s [%(levelname)s] %(message)s"  # Define la estructura de cada
                                                      # mensaje de log: fecha y hora,
                                                      # nivel de gravedad, y el mensaje
                                                      # en sí.
)

# --- Funciones Principales ---

# Definición de función para leer casos de grafos desde un archivo de texto.
# El formato esperado es:
# n m
# u1 v1
# ...
# um vm
def leer_casos(ruta):
    casos = []  # Lista donde se guardarán los grafos cargados.

    # Usar `with open(...)` para asegurar que el archivo se cierre
    # automáticamente, incluso si ocurre un error.
    with open(ruta, 'r') as f:
        # Leer todas las líneas del archivo. `.strip()` elimina los espacios
        # en blanco al inicio y al final de cada línea, y el condicional
        # `if line.strip() != ""` omite las líneas completamente vacías.
        lineas = [line.strip() for line in f if line.strip() != ""]

    i = 0  # Inicializar un índice para recorrer las líneas del archivo.

    # Ciclo principal para procesar todos los casos de prueba en el archivo.
    while i < len(lineas):

        # Si la línea actual empieza con "#", se considera un comentario y se ignora.
        if lineas[i].startswith("#"):
            i += 1  # Avanzar al siguiente índice.
            continue  # Saltar el resto de la iteración y continuar con el siguiente caso.

        try:
            # Intentar leer la cantidad de nodos (n) y aristas (m).
            # `map(int, ...)` convierte las cadenas de texto en números enteros.
            n, m = map(int, lineas[i].split())
            i += 1  # Avanzar a la siguiente línea, que contendrá las aristas.

            edges = []  # Lista para almacenar las aristas del grafo actual.

            # Leer las siguientes 'm' líneas, que representan las aristas.
            for _ in range(m):
                # Verificar que no se haya llegado al final del archivo inesperadamente.
                if i >= len(lineas):
                    raise ValueError("El archivo termina antes de leer todas las aristas indicadas.")

                # Verificar si una línea de arista es un comentario. Esto asegura
                # que el formato del archivo sea consistente.
                if lineas[i].startswith("#"):
                    raise ValueError("Se encontró un comentario donde se esperaba una arista.")

                # Leer los dos nodos que forman la arista y convertirlos a enteros.
                u, v = map(int, lineas[i].split())

                edges.append((u, v))  # Agregar la tupla (u, v) a la lista de aristas.
                i += 1  # Avanzar a la siguiente línea.

            # Crear un grafo vacío no dirigido con NetworkX.
            G = nx.Graph()

            # Agregar los nodos al grafo. `range(n)` crea nodos de 0 a n-1.
            G.add_nodes_from(range(n))

            # Agregar todas las aristas leídas al grafo.
            G.add_edges_from(edges)

            # Añadir el grafo creado a la lista de casos.
            casos.append(G)

        except Exception as e:
            # Capturar cualquier error que ocurra durante el procesamiento de un caso.
            # `logging.error(...)` registra el error en el archivo de log.
            logging.error(f"Error al procesar el caso en la línea {i}: {e}")
            # Romper el ciclo para detener el procesamiento de los casos restantes,
            # ya que un error de formato puede afectar a los siguientes.
            break

    # Devolver la lista con todos los grafos leídos correctamente.
    return casos