from graph_utils_IA import leer_casos
from coloring_IA import busqueda_local

def main():
    casos = leer_casos("data/casos_coloracion_grafos.txt")  # Carga todos los grafos del archivo

    for i, (n, aristas) in enumerate(casos, 1):  # Iteramos sobre cada grafo (n nodos, aristas)
        k = n  # Número máximo de colores permitidos (puedes optimizar bajando este número)
        colores, conflictos = busqueda_local(n, aristas, k)  # Ejecutamos el algoritmo
        usados = len(set(colores.values()))  # Contamos los colores realmente usados

        # Mostramos resultados
        print(f"Caso {i}:")
        print(f"  Conflictos = {conflictos}")
        print(f"  Colores usados = {usados}")
        print(f"  Colores asignados: {colores}")
        print()
if __name__ == "__main__":
    main()  # Ejecuta la función principal al correr el script  