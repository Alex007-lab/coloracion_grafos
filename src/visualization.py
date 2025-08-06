import matplotlib.pyplot as plt
import networkx as nx
import os
import imageio

def detectar_conflictos(G, colores):
    return [(u, v) for u, v in G.edges() if colores[u] == colores[v]]

def dibujar_grafo(G, colores, conflictos, pos, paso, descripcion, carpeta_salida):
    fig, ax = plt.subplots()
    nodos = list(G.nodes())
    color_ids = [colores[n] for n in nodos]

    nx.draw_networkx_nodes(G, pos, node_color=color_ids, cmap=plt.cm.Set3, node_size=500, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color='black', ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="lightgray", width=2, ax=ax)

    if conflictos:
        nx.draw_networkx_edges(G, pos, edgelist=conflictos, edge_color="red", width=3, ax=ax)

    ax.set_title(f"Paso {paso}: {descripcion}")
    plt.axis("off")
    nombre_img = f"{carpeta_salida}/tmp_{paso}.png"
    plt.savefig(nombre_img)
    plt.close()
    return nombre_img

def crear_animacion(G, pasos, caso_id, k, carpeta_salida="../results/grafos_coloreados", duration=1.2):
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta_gif = f"{carpeta_salida}/caso_{caso_id}_k{k}.gif"
    pos = nx.spring_layout(G, seed=42)

    frames = []
    paso = 0

    # Paso 0: grafo vacío
    vacio = {n: 0 for n in G.nodes()}
    img = dibujar_grafo(G, vacio, [], pos, paso, "Creación del grafo", carpeta_salida)
    frames.append(imageio.imread(img))
    paso += 1

    # Paso 1: asignación aleatoria (pasos[0])
    colores, _ = pasos[0]
    conflictos = detectar_conflictos(G, colores)
    img = dibujar_grafo(G, colores, conflictos, pos, paso, "Asignación aleatoria de colores", carpeta_salida)
    frames.append(imageio.imread(img))
    paso += 1

    # Paso 2: conflictos iniciales
    img = dibujar_grafo(G, colores, conflictos, pos, paso, f"Conflictos iniciales: {len(conflictos)}", carpeta_salida)
    frames.append(imageio.imread(img))
    paso += 1

    # Paso 3+: pasos del algoritmo
    for i, (colores, _) in enumerate(pasos[1:], start=1):
        conflictos = detectar_conflictos(G, colores)
        descripcion = f"Iteración {i} - Conflictos: {len(conflictos)}"
        img = dibujar_grafo(G, colores, conflictos, pos, paso, descripcion, carpeta_salida)
        frames.append(imageio.imread(img))
        paso += 1

    imageio.mimsave(ruta_gif, frames, duration=duration)

    # Limpieza
    for i in range(paso):
        tmp_path = f"{carpeta_salida}/tmp_{i}.png"
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
