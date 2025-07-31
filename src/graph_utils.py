def leer_grafos(ruta):
    grafos = []
    with open(ruta, "r") as archivo:
        lineas = archivo.readlines()
        i = 0
        while i < len(lineas):
            linea = lineas[i].strip()
            if linea.startswith("#") or not linea:
                i += 1
                continue
            n, m = map(int, linea.split())
            i += 1
            aristas = []
            for _ in range(m):
                while i < len(lineas) and (lineas[i].strip().startswith("#") or not lineas[i].strip()):
                    i += 1
                aristas.append(tuple(map(int, lineas[i].strip().split())))
                i += 1
            grafos.append({"nodos": n, "aristas": aristas})
    return grafos

# Ejemplo de uso
casos = leer_grafos('data/casos_coloracion_grafos.txt')  # Lee los casos del archivo
for idx, caso in enumerate(casos):  # Recorre cada caso con su índice
    print(f"Caso {idx+1}: {caso['nodos']} nodos, {len(caso['aristas'])} aristas")  # Imprime resumen
    print("Aristas:", caso['aristas'])  # Imprime las aristas de cada caso  