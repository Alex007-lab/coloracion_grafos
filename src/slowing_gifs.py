import os  # Módulo estándar para interactuar con el sistema operativo (manejo de archivos y rutas).
from PIL import Image, ImageSequence  # `Pillow`, una biblioteca de procesamiento de imágenes. Se usa para abrir, manipular y guardar GIFs.

def ralentizar_gif_duracion_fija(archivo_entrada, archivo_salida, duracion_fija_ms):
    """
    Ralentiza un archivo GIF estableciendo una duración fija para todos sus frames.

    Args:
        archivo_entrada (str): La ruta completa del archivo GIF original.
        archivo_salida (str): La ruta completa para guardar el nuevo archivo GIF ralentizado.
        duracion_fija_ms (int): La nueva duración de cada frame en milisegundos (1000 ms = 1s).
    """
    try:
        # Abre el archivo GIF de entrada para su procesamiento.
        imagen = Image.open(archivo_entrada)
        frames = []  # Lista para almacenar los frames modificados.

        # Itera sobre cada frame del GIF usando ImageSequence.Iterator.
        for frame in ImageSequence.Iterator(imagen):
            # Crea una copia del frame para evitar modificar el original.
            frame = frame.copy()
            # Establece la nueva duración para el frame actual.
            frame.info['duration'] = duracion_fija_ms
            # Agrega el frame modificado a la lista.
            frames.append(frame)

        # Guarda todos los frames en un nuevo archivo GIF.
        # `save_all=True` indica que se deben guardar todos los frames.
        # `append_images=frames[1:]` adjunta todos los frames excepto el primero.
        # `loop=...` mantiene el número de ciclos del GIF original.
        # `duration=...` establece la duración para todos los frames al guardar.
        # `disposal=2` es un parámetro común en GIFs para indicar que el fondo del frame
        # anterior debe ser restaurado antes de dibujar el siguiente.
        frames[0].save(
            archivo_salida,
            save_all=True,
            append_images=frames[1:],
            loop=imagen.info.get('loop', 0),
            duration=duracion_fija_ms,
            disposal=2
        )
        print(f"✔️ {os.path.basename(archivo_entrada)} → procesado como → {os.path.basename(archivo_salida)}")

    except Exception as e:
        # Captura cualquier error que pueda ocurrir durante el proceso, como
        # si el archivo no es un GIF válido, y lo reporta.
        print(f"❌ Error con {archivo_entrada}: {e}")

def procesar_carpeta(carpeta_entrada, carpeta_salida, duracion_fija_ms):
    """
    Procesa todos los archivos GIF en una carpeta de entrada y los guarda
    en una carpeta de salida con una duración de frame modificada.

    Args:
        carpeta_entrada (str): La ruta a la carpeta con los GIFs originales.
        carpeta_salida (str): La ruta donde se guardarán los GIFs ralentizados.
        duracion_fija_ms (int): La duración deseada por frame en milisegundos.
    """
    # Si la carpeta de salida no existe, la crea.
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Lista todos los archivos en la carpeta de entrada y filtra para incluir
    # solo los que terminan en ".gif" (sin distinción entre mayúsculas y minúsculas).
    archivos = [f for f in os.listdir(carpeta_entrada) if f.lower().endswith(".gif")]

    # Si no se encuentran archivos GIF, imprime una advertencia y termina la función.
    if not archivos:
        print(f"⚠️ No se encontraron archivos .gif en la carpeta '{carpeta_entrada}'.")
        return

    # Itera sobre cada archivo GIF encontrado.
    for archivo in archivos:
        # Construye la ruta completa del archivo de entrada de forma segura.
        ruta_entrada = os.path.join(carpeta_entrada, archivo)

        # Extrae el nombre del archivo sin la extensión.
        nombre_base = os.path.splitext(archivo)[0]
        # Crea un nuevo nombre de archivo agregando "_lento".
        nuevo_nombre = nombre_base + "_lento.gif"
        # Construye la ruta de salida completa.
        ruta_salida = os.path.join(carpeta_salida, nuevo_nombre)

        # Llama a la función principal para ralentizar y guardar el GIF.
        ralentizar_gif_duracion_fija(ruta_entrada, ruta_salida, duracion_fija_ms)

    print("\n✅ Todos los GIFs han sido procesados con duración fija y renombrados con '_lento'.")

# --- Bloque de ejecución principal ---

# Este bloque se ejecuta solo cuando el script se corre directamente.
if __name__ == "__main__":
    # Obtiene la ruta del directorio del script actual para construir rutas relativas.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta a la carpeta de entrada donde están los GIFs originales.
    carpeta_gifs_originales = os.path.join(script_dir, "..", "results", "grafos_coloreados")
    # Construye la ruta a la carpeta de salida para los GIFs ralentizados.
    carpeta_gifs_lentos = os.path.join(script_dir, "..", "results", "grafos_coloreados_lentos")

    # Define la duración deseada para cada frame en milisegundos.
    duracion_por_frame = 3000  # 🕐 Esto equivale a 3 segundos por frame.

    # Llama a la función principal para iniciar el procesamiento de la carpeta.
    procesar_carpeta(carpeta_gifs_originales, carpeta_gifs_lentos, duracion_por_frame)