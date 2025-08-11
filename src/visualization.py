# Importa la biblioteca de visualización Matplotlib para crear gráficos.
import matplotlib.pyplot as plt
# Importa la biblioteca NetworkX para trabajar con grafos.
import networkx as nx
# Importa el módulo 'os' para interactuar con el sistema operativo (manejo de rutas y directorios).
import os
# Importa la biblioteca 'imageio' para crear animaciones a partir de imágenes.
import imageio

# Define una función que detecta conflictos en la coloración de un grafo.
# Un conflicto ocurre cuando dos nodos conectados (una arista) tienen el mismo color.
def detectar_conflictos(G, colores):
    # Retorna una lista de tuplas (aristas) donde los colores de los nodos u y v son idénticos.
    return [(u, v) for u, v in G.edges() if colores[u] == colores[v]]

# Define una función para dibujar el grafo y guardar el resultado como una imagen PNG temporal.
def dibujar_grafo(G, colores, conflictos, pos, paso, descripcion, carpeta_salida):
    # Crea una figura y un eje para el gráfico, que es el área de dibujo.
    fig, ax = plt.subplots()
    # Obtiene una lista de todos los nodos del grafo.
    nodos = list(G.nodes())
    # Crea una lista de IDs de color para cada nodo, basándose en el diccionario 'colores'.
    color_ids = [colores[n] for n in nodos]

    # Dibuja los nodos del grafo.
    # 'pos' define la posición de cada nodo.
    # 'node_color' asigna los colores según la lista 'color_ids'.
    # 'cmap' es el mapa de colores que se usará.
    # 'node_size' es el tamaño de los nodos.
    # 'ax' especifica en qué eje dibujar.
    nx.draw_networkx_nodes(G, pos, node_color=color_ids, cmap=plt.cm.Set3, node_size=500, ax=ax)
    # Dibuja las etiquetas (nombres/IDs) de los nodos.
    nx.draw_networkx_labels(G, pos, font_color='black', ax=ax)
    # Dibuja las aristas del grafo.
    # Las aristas normales se muestran en gris claro.
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="lightgray", width=2, ax=ax)

    # Si la lista de 'conflictos' no está vacía (hay conflictos)...
    if conflictos:
        # Dibuja las aristas que están en conflicto en color rojo y con un grosor mayor.
        nx.draw_networkx_edges(G, pos, edgelist=conflictos, edge_color="red", width=3, ax=ax)

    # Establece el título del gráfico para indicar el paso y una descripción.
    ax.set_title(f"Paso {paso}: {descripcion}")
    # Oculta los ejes para tener un gráfico más limpio.
    plt.axis("off")
    # Construye la ruta completa para guardar la imagen temporal.
    # Usa os.path.join para compatibilidad con diferentes sistemas operativos.
    nombre_img = os.path.join(carpeta_salida, f"tmp_{paso}.png")
    # Guarda la figura en el archivo especificado.
    plt.savefig(nombre_img)
    # Cierra la figura para liberar memoria.
    plt.close()
    # Retorna la ruta de la imagen guardada.
    return nombre_img

# Define la función principal que crea la animación (GIF).
def crear_animacion(G, pasos, caso_id, k, duration=1.2):
    # Obtiene la ruta del directorio del script actual (visualization.py).
    # Esto asegura que las rutas sean relativas al script, no al directorio de ejecución.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta completa a la carpeta donde se guardarán los GIFs.
    # Navega un nivel arriba (..) desde 'src' y entra en 'results/grafos_coloreados'.
    carpeta_salida = os.path.join(script_dir, "..", "results", "grafos_coloreados")
    
    # Crea la carpeta de salida si no existe.
    os.makedirs(carpeta_salida, exist_ok=True)
    # Construye la ruta completa para el archivo GIF final.
    ruta_gif = os.path.join(carpeta_salida, f"caso_{caso_id}_k{k}.gif")
    # Calcula la posición de los nodos del grafo para una visualización consistente.
    # 'seed=42' asegura que las posiciones sean las mismas cada vez que se ejecute.
    pos = nx.spring_layout(G, seed=42)

    # Inicializa una lista para almacenar los frames (imágenes) del GIF.
    frames = []
    # Inicializa un contador para los pasos de la animación.
    paso = 0

    # --- Creación del GIF paso a paso ---

    # Paso 0: Muestra el grafo sin coloración.
    # Crea un diccionario de colores donde todos los nodos tienen el color 0.
    vacio = {n: 0 for n in G.nodes()}
    # Dibuja el grafo en su estado inicial.
    img = dibujar_grafo(G, vacio, [], pos, paso, "Creación del grafo", carpeta_salida)
    # Agrega la imagen a la lista de frames.
    frames.append(imageio.imread(img))
    # Incrementa el contador de pasos.
    paso += 1

    # Paso 1: Muestra el estado del grafo después de la asignación de colores inicial (aleatoria).
    # Obtiene el diccionario de colores del primer paso registrado.
    colores, _ = pasos[0]
    # Detecta si hay conflictos con esta coloración inicial.
    conflictos = detectar_conflictos(G, colores)
    # Dibuja el grafo con la asignación aleatoria.
    img = dibujar_grafo(G, colores, conflictos, pos, paso, "Asignación aleatoria de colores", carpeta_salida)
    # Agrega la imagen a la lista de frames.
    frames.append(imageio.imread(img))
    # Incrementa el contador de pasos.
    paso += 1

    # Paso 2: Muestra el estado del grafo con los conflictos iniciales.
    # Reutiliza la imagen del paso anterior pero cambia la descripción.
    img = dibujar_grafo(G, colores, conflictos, pos, paso, f"Conflictos iniciales: {len(conflictos)}", carpeta_salida)
    # Agrega la imagen a la lista de frames.
    frames.append(imageio.imread(img))
    # Incrementa el contador de pasos.
    paso += 1

    # Pasos 3 en adelante: Itera sobre los pasos del algoritmo para mostrar la evolución de la coloración.
    # `pasos[1:]` omite el primer paso (la asignación aleatoria).
    for i, (colores, _) in enumerate(pasos[1:], start=1):
        # Detecta los conflictos en la coloración actual.
        conflictos = detectar_conflictos(G, colores)
        # Define una descripción para el título del gráfico.
        descripcion = f"Iteración {i} - Conflictos: {len(conflictos)}"
        # Dibuja el grafo en el estado actual del algoritmo.
        img = dibujar_grafo(G, colores, conflictos, pos, paso, descripcion, carpeta_salida)
        # Agrega la imagen a la lista de frames.
        frames.append(imageio.imread(img))
        # Incrementa el contador de pasos.
        paso += 1

    # Crea el archivo GIF a partir de la lista de frames.
    # 'ruta_gif' es el nombre del archivo de salida.
    # 'duration' es la duración de cada frame en segundos.
    imageio.mimsave(ruta_gif, frames, duration=duration)

    # Sección de limpieza: Elimina los archivos de imagen temporales que se crearon.
    # Itera sobre el número total de pasos de la animación.
    for i in range(paso):
        # Construye la ruta al archivo temporal.
        tmp_path = os.path.join(carpeta_salida, f"tmp_{i}.png")
        # Verifica si el archivo existe antes de intentar eliminarlo.
        if os.path.exists(tmp_path):
            # Elimina el archivo temporal.
            os.remove(tmp_path)