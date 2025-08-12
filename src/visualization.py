# Importaciones de librerías y módulos
import matplotlib.pyplot as plt # Librería para crear gráficos y visualizaciones.
import networkx as nx           # Librería para trabajar con grafos.
import os                       # Módulo para interactuar con el sistema operativo (rutas y directorios).
import imageio                  # Librería para crear archivos GIF a partir de imágenes.

def detectar_conflictos(G, colores):
    """
    Detecta aristas con conflictos de coloración.
    Un conflicto ocurre cuando dos nodos conectados por una arista tienen el mismo color.

    Args:
        G (nx.Graph): El grafo a analizar.
        colores (dict): Un diccionario que mapea cada nodo a su color asignado.

    Returns:
        list: Una lista de tuplas (aristas) que están en conflicto.
    """
    # Retorna una lista de aristas (u, v) donde los colores de los nodos son idénticos.
    return [(u, v) for u, v in G.edges() if colores[u] == colores[v]]

def dibujar_grafo(G, colores, conflictos, pos, paso, descripcion, k_actual, carpeta_salida):
    """
    Dibuja el grafo en un estado específico de coloración y lo guarda
    como una imagen PNG temporal para la animación.

    Args:
        G (nx.Graph): El grafo a dibujar.
        colores (dict): El diccionario de colores actual de los nodos.
        conflictos (list): Una lista de aristas en conflicto.
        pos (dict): La posición precalculada de cada nodo para mantener un diseño consistente.
        paso (int): El número de paso en la animación.
        descripcion (str): Un texto descriptivo para el título.
        k_actual (str): El valor actual de k (número máximo de colores permitidos).
                        Es un string para poder usar "-" en el paso inicial.
        carpeta_salida (str): La ruta donde se guardarán las imágenes temporales.

    Returns:
        str: La ruta completa del archivo de imagen que se ha guardado.
    """
    # Crea una figura y ejes para el gráfico.
    fig, ax = plt.subplots()
    nodos = list(G.nodes())
    color_ids = [colores[n] for n in nodos]

    # Dibuja los nodos con sus respectivos colores y etiquetas.
    nx.draw_networkx_nodes(G, pos, node_color=color_ids, cmap=plt.cm.Set3, node_size=500, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color='black', ax=ax)
    
    # Dibuja todas las aristas del grafo en un color gris claro.
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="lightgray", width=2, ax=ax)

    # Si hay aristas en conflicto, las dibuja encima de las demás con un color rojo más grueso
    # para resaltarlas.
    if conflictos:
        nx.draw_networkx_edges(G, pos, edgelist=conflictos, edge_color="red", width=3, ax=ax)

    # Título principal del gráfico.
    ax.set_title(f"Paso {paso}: {descripcion}", fontsize=12)
    
    # Añade un cuadro de texto en la esquina superior izquierda con información del estado actual.
    ax.text(
        0.02, 0.98,
        f"k actual: {k_actual}\nConflictos: {len(conflictos)}",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        # Configuración de la caja de texto para mejorar la legibilidad.
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7)
    )

    plt.axis("off") # Oculta los ejes para una visualización limpia del grafo.
    
    # Construye la ruta del archivo temporal y lo guarda.
    nombre_img = os.path.join(carpeta_salida, f"tmp_{paso}.png")
    plt.savefig(nombre_img)
    plt.close() # Cierra la figura para liberar memoria del sistema.
    
    return nombre_img

def crear_animacion(G, pasos, caso_id, duration=1.2):
    """
    Crea una animación GIF a partir de una secuencia de estados de coloración del grafo.

    Args:
        G (nx.Graph): El grafo a animar.
        pasos (list): Una lista de tuplas (colores, conf, k, descripcion) que
                      representa la secuencia de estados del algoritmo.
                      - colores (dict): Asignación de colores a los nodos.
                      - conf (int): Número de conflictos en ese paso.
                      - k (int): Número de colores usados en el intento.
                      - descripcion (str): Descripción del estado para el título del frame.
        caso_id (int): El identificador del caso de prueba.
        duration (float, optional): La duración de cada frame en segundos. Por defecto es 1.2.
    """
    # Obtiene la ruta del directorio del script actual.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta al directorio de salida para los GIFs y las imágenes temporales.
    carpeta_salida = os.path.join(script_dir, "..", "results", "grafos_coloreados")
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # Define el nombre del archivo GIF final.
    ruta_gif = os.path.join(carpeta_salida, f"caso_{caso_id}.gif")
    
    # Precalcula la posición de los nodos una sola vez para mantener una consistencia
    # visual a lo largo de toda la animación.
    pos = nx.spring_layout(G, seed=42)

    frames = [] # Lista para almacenar los frames (imágenes) del GIF.
    paso = 0    # Contador de pasos para nombrar los archivos temporales.

    # --- Generación de los frames de la animación ---

    # Frame 0: Estado inicial del grafo sin coloración.
    vacio = {n: 0 for n in G.nodes()} # Asigna el color 0 a todos los nodos.
    # El valor de `k_actual` en este paso inicial se marca como "-" ya que aún no hay un intento.
    img = dibujar_grafo(G, vacio, [], pos, paso, "Creación del grafo", "-", carpeta_salida)
    frames.append(imageio.imread(img))
    paso += 1

    # Itera sobre la lista de todos los pasos acumulados para generar cada frame.
    for colores, conf, k, descripcion in pasos:
        # Detecta los conflictos en el estado de coloración actual.
        conflictos = detectar_conflictos(G, colores)
        
        # Dibuja el estado actual del grafo y guarda la imagen temporal.
        img = dibujar_grafo(G, colores, conflictos, pos, paso, descripcion, k, carpeta_salida)
        frames.append(imageio.imread(img))
        paso += 1

    # Guarda la lista de frames como un archivo GIF animado.
    imageio.mimsave(ruta_gif, frames, duration=duration)

    # --- Limpieza de archivos temporales ---
    # Este bucle elimina las imágenes PNG temporales que se crearon.
    for i in range(paso):
        tmp_path = os.path.join(carpeta_salida, f"tmp_{i}.png")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)