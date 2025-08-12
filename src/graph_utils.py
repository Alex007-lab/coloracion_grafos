# Importa el módulo 'os' para interactuar con el sistema operativo (manejo de rutas y directorios).
import os
# Importa la librería 'networkx' para la creación y manipulación de grafos.
import networkx as nx
# Importa el módulo 'logging' para registrar eventos y errores.
import logging

# --- Configuración Inicial y Manejo de Logs ---
# Esta sección se ejecuta una sola vez al importar el módulo para configurar el entorno.

# Obtiene la ruta del directorio donde se encuentra este script. Esto es crucial
# para que las rutas relativas funcionen sin importar desde dónde se ejecute el programa principal.
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construye la ruta al directorio 'results' navegando un nivel arriba de 'src'.
results_dir = os.path.join(script_dir, "..", "results")
# Crea la carpeta 'results' si aún no existe. `exist_ok=True` evita errores si ya está creada.
os.makedirs(results_dir, exist_ok=True)
# Define la ruta completa para el archivo de logs.
log_path = os.path.join(results_dir, "errores.log")

# Configura el logger para que guarde los mensajes en el archivo de log.
logging.basicConfig(
    filename=log_path,  # Especifica el archivo donde se guardarán los logs.
    filemode="w",       # Abre el archivo en modo de escritura ('w'), sobrescribiendo el contenido anterior
                        # en cada nueva ejecución. Esto asegura que el log esté siempre actualizado.
    level=logging.INFO, # Establece el nivel mínimo para los mensajes de log. Solo se registrarán
                        # mensajes de nivel INFO, WARNING, ERROR y CRITICAL.
    format="%(asctime)s [%(levelname)s] %(message)s" # Define el formato del mensaje del log.
)

# --- Funciones Principales ---

def leer_casos(ruta):
    """
    Lee uno o varios grafos desde un archivo de texto en un formato específico.

    El formato del archivo es el siguiente:
    # Comentario opcional
    n m
    u1 v1
    u2 v2
    ...
    um vm
    
    Donde:
      - n: número de nodos del grafo.
      - m: número de aristas del grafo.
      - ui vi: los nodos conectados por una arista.

    Args:
        ruta (str): La ruta al archivo de texto con los casos de prueba.

    Returns:
        list: Una lista de objetos de NetworkX, donde cada objeto es un grafo
              leído correctamente del archivo.
    """
    casos = []  # Inicializa la lista para almacenar los grafos leídos.
    
    # Abre el archivo de forma segura con `encoding="utf-8"` para evitar errores
    # con caracteres especiales y asegura que se cierre automáticamente.
    with open(ruta, 'r', encoding="utf-8") as f:
        # Lee todas las líneas, elimina los espacios en blanco y filtra las líneas vacías.
        lineas = [line.strip() for line in f if line.strip() != ""]

    i = 0  # Inicializa un índice para recorrer las líneas del archivo.
    
    # Bucle principal que procesa cada caso de grafo.
    while i < len(lineas):
        # Si la línea es un comentario (empieza con '#'), la ignora y avanza.
        if lineas[i].startswith("#"):
            i += 1
            continue

        try:
            # Lee el número de nodos (n) y aristas (m) del grafo actual.
            # `split()` divide la línea por espacios, y `map(int, ...)` convierte los resultados a enteros.
            n, m = map(int, lineas[i].split())
            i += 1  # Avanza a la siguiente línea, donde se esperan las aristas.
            
            edges = []  # Lista temporal para guardar las aristas del grafo actual.
            
            # Bucle para leer las 'm' aristas del grafo.
            for _ in range(m):
                # Verifica si el archivo se ha quedado sin líneas antes de leer todas las aristas esperadas.
                if i >= len(lineas):
                    raise ValueError("El archivo termina antes de leer todas las aristas.")
                
                # Lanza un error si se encuentra un comentario donde se espera una arista.
                if lineas[i].startswith("#"):
                    raise ValueError("Se encontró un comentario donde se esperaba una arista.")
                
                # Lee los nodos de la arista (u, v) y los convierte a enteros.
                u, v = map(int, lineas[i].split())
                
                # Agrega la arista a la lista temporal.
                edges.append((u, v))
                i += 1  # Avanza al siguiente par de nodos.
            
            # Crea un objeto de grafo no dirigido usando la librería NetworkX.
            G = nx.Graph()
            
            # Agrega 'n' nodos al grafo, numerados desde 0 hasta n-1.
            G.add_nodes_from(range(n))
            
            # Agrega todas las aristas leídas al grafo.
            G.add_edges_from(edges)
            
            # Mensaje de depuración para confirmar que un caso ha sido leído correctamente.
            print(f"📥 Caso leído -> Nodos: {G.number_of_nodes()}, Aristas: {G.number_of_edges()}")
            
            # Añade el grafo completo a la lista de casos.
            casos.append(G)

        except Exception as e:
            # Captura cualquier error (como un formato de archivo incorrecto) y lo registra en el log.
            logging.error(f"Error al procesar el caso en la línea {i}: {e}")
            # Rompe el bucle para no seguir procesando datos corruptos.
            break
    
    # Devuelve la lista de grafos leídos.
    return casos