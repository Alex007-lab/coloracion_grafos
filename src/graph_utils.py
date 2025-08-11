import os  # Módulo para manejo de archivos y directorios
import networkx as nx  # Librería para crear y manipular grafos
import logging  # Módulo para registrar eventos y errores en archivos o consola

# Crear la carpeta "results" si no existe, para guardar archivos de resultados o logs
os.makedirs("results", exist_ok=True)

# Configurar el logger para que guarde mensajes en un archivo de log
logging.basicConfig(
    filename="../results/errores.log",  # Archivo donde se guardan los logs
    filemode="w",  # Modo escritura, sobreescribe el archivo cada vez que corre el programa
    level=logging.INFO,  # Nivel mínimo de mensajes que se registran (INFO y superiores)
    format="%(asctime)s [%(levelname)s] %(message)s"  # Formato del mensaje de log
)

# Definición de función para leer casos desde un archivo
def leer_casos(ruta):
    casos = []  # Lista donde se guardarán los grafos cargados

    # Abrir el archivo indicado en modo lectura
    with open(ruta, 'r') as f:
        # Leer todas las líneas, eliminando espacios al inicio y final, y omitiendo líneas vacías
        lineas = [line.strip() for line in f if line.strip() != ""]

    i = 0  # Índice para recorrer las líneas del archivo

    # Ciclo para procesar todas las líneas del archivo
    while i < len(lineas):

        # Si la línea empieza con "#", es un comentario y se ignora
        if lineas[i].startswith("#"):
            i += 1  # Avanzar a la siguiente línea
            continue  # Saltar el resto y continuar el ciclo

        try:
            # Leer la cantidad de nodos (n) y aristas (m) de la línea actual
            n, m = map(int, lineas[i].split())
            i += 1  # Avanzar a la siguiente línea

            edges = []  # Lista para almacenar las aristas del grafo actual

            # Leer las siguientes m líneas, que representan las aristas
            for _ in range(m):
                # Verificar que no se haya llegado al final del archivo
                if i >= len(lineas):
                    raise ValueError("No hay suficientes líneas para las aristas indicadas.")

                # Si la línea donde se espera una arista es un comentario, lanzar error
                if lineas[i].startswith("#"):
                    raise ValueError("Se encontró un comentario donde se esperaba una arista.")

                # Leer los dos nodos que forman la arista
                u, v = map(int, lineas[i].split())

                edges.append((u, v))  # Agregar la arista a la lista
                i += 1  # Avanzar a la siguiente línea

            # Crear un grafo vacío con NetworkX
            G = nx.Graph()

            # Agregar los nodos numerados del 0 a n-1
            G.add_nodes_from(range(n))

            # Agregar todas las aristas leídas al grafo
            G.add_edges_from(edges)

            # Añadir el grafo creado a la lista de casos
            casos.append(G)

        except Exception as e:
            # Si ocurre algún error al procesar el caso, registrar el error con línea y mensaje
            logging.error(f"Error al procesar el caso en la línea {i}: {e}")
            break  # Salir del ciclo para no seguir procesando más casos si hay error

    # Devolver la lista con todos los grafos leídos correctamente
    return casos

