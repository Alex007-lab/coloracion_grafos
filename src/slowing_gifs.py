import os
from PIL import Image, ImageSequence

def ralentizar_gif_duracion_fija(archivo_entrada, archivo_salida, duracion_fija_ms):
    try:
        imagen = Image.open(archivo_entrada)
        frames = []

        for frame in ImageSequence.Iterator(imagen):
            frame = frame.copy()
            frame.info['duration'] = duracion_fija_ms
            frames.append(frame)

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
        print(f"❌ Error con {archivo_entrada}: {e}")


def procesar_carpeta(carpeta_entrada, carpeta_salida, duracion_fija_ms):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    archivos = [f for f in os.listdir(carpeta_entrada) if f.lower().endswith(".gif")]

    if not archivos:
        print("⚠️ No se encontraron archivos .gif en la carpeta.")
        return

    for archivo in archivos:
        ruta_entrada = os.path.join(carpeta_entrada, archivo)

        nombre_base = os.path.splitext(archivo)[0]
        nuevo_nombre = nombre_base + "_lento.gif"
        ruta_salida = os.path.join(carpeta_salida, nuevo_nombre)

        ralentizar_gif_duracion_fija(ruta_entrada, ruta_salida, duracion_fija_ms)

    print("\n✅ Todos los GIFs han sido procesados con duración fija y renombrados con '_lento'.")


# 👇 Aquí defines tus rutas y duración fija por frame (en milisegundos)
if __name__ == "__main__":
    carpeta_gifs_originales = "../results/grafos_coloreados"  # Cambia esta ruta según tu estructura
    carpeta_gifs_lentos = "../results/grafos_coloreados_lentos"  # Ruta de salida para los GIFs lentos

    duracion_por_frame = 3000  # 🕐 Duración en milisegundos (1000 = 1 segundo por frame)

    procesar_carpeta(carpeta_gifs_originales, carpeta_gifs_lentos, duracion_por_frame)
