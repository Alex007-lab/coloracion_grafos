import os
import networkx as nx
import logging


# 🔧 Asegurar que exista la carpeta antes de escribir el log
os.makedirs("results", exist_ok=True)

# Configurar el logger
logging.basicConfig(
    filename="../results/errores.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Configura el logger para consola y archivo
logging.basicConfig(
    filename="../results/errores.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def leer_casos(ruta):
    casos = []
    with open(ruta, 'r') as f:
        lineas = [line.strip() for line in f if line.strip() != ""]

    i = 0
    while i < len(lineas):
        if lineas[i].startswith("#"):
            i += 1
            continue

        try:
            n, m = map(int, lineas[i].split())
            i += 1

            edges = []
            for _ in range(m):
                if i >= len(lineas):
                    raise ValueError("No hay suficientes líneas para las aristas indicadas.")
                if lineas[i].startswith("#"):
                    raise ValueError("Se encontró un comentario donde se esperaba una arista.")
                u, v = map(int, lineas[i].split())
                edges.append((u, v))
                i += 1

            G = nx.Graph()
            G.add_nodes_from(range(n))
            G.add_edges_from(edges)
            casos.append(G)

        except Exception as e:
            logging.error(f"Error al procesar el caso en la línea {i}: {e}")
            break

    return casos
