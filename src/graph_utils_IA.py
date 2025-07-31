def leer_casos(path):
    casos = []  # Lista para guardar todos los casos
    with open(path, 'r') as file:  # Abre el archivo en modo lectura
        lines = file.readlines()   # Lee todas las líneas del archivo
    i = 0  # Índice para recorrer las líneas
    while i < len(lines):  # Mientras no se llegue al final del archivo
        line = lines[i].strip()  # Quita espacios y saltos de línea
        if line.startswith('#') or not line:  # Si la línea es comentario o está vacía
            i += 1  # Pasa a la siguiente línea
            continue  # Salta el resto del ciclo y vuelve a empezar
        # Si la línea no es comentario ni vacía, contiene nodos y aristas
        n, m = map(int, line.split())  # Convierte los dos números en enteros
        i += 1  # Avanza a la siguiente línea
        aristas = []  # Lista para guardar las aristas de este caso
        for _ in range(m):  # Repite m veces (cantidad de aristas)
            # Salta comentarios o líneas vacías entre aristas
            while i < len(lines) and (lines[i].strip().startswith('#') or not lines[i].strip()):
                i += 1
            # Lee la arista y la convierte en una tupla de enteros
            aristas.append(tuple(map(int, lines[i].strip().split())))
            i += 1  # Avanza a la siguiente línea
        # Guarda el caso como un diccionario con nodos y aristas
        casos.append({'nodos': n, 'aristas': aristas})
    return casos  # Devuelve la lista de casos

# Ejemplo de uso
casos = leer_casos('data/casos_coloracion_grafos.txt')  # Lee los casos del archivo
for idx, caso in enumerate(casos):  # Recorre cada caso con su índice
    print(f"Caso {idx+1}: {caso['nodos']} nodos, {len(caso['aristas'])} aristas")  # Imprime resumen
    print("Aristas:", caso['aristas'])  # Imprime las aristas de cada caso  