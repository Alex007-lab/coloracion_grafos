# 📝 Informe Técnico — Coloración de Grafos con Búsqueda Local

## 🎯 Objetivo

Asignar colores a los vértices de un grafo de forma que no haya dos vértices adyacentes con el mismo color, utilizando el menor número posible de colores, aplicando búsqueda local con estrategia de mejor mejora.

---

## ⚙️ Pseudocódigo del algoritmo utilizado

```text
Algoritmo ColoraciónGrafo(Grafo G, k colores, iteraciones máximas)

1. Colorear aleatoriamente cada nodo con uno de los k colores.
2. Calcular el número de conflictos iniciales (aristas cuyos extremos tienen el mismo color).
3. Mientras haya mejoras y no se alcance el límite de iteraciones:
    a. Para cada nodo:
        i. Probar todos los colores posibles distintos al actual.
        ii. Si alguno reduce el número de conflictos, guardar la mejor opción.
    b. Si alguna mejora se encontró, actualizar la coloración.
    c. Si no hay mejoras, terminar.
4. Si no hay conflictos, intentar de nuevo con k - 1 colores.
5. Guardar la mejor solución sin conflictos.
```

---

## 🔢 Descripción de entrada y salida

### Entrada:
- Archivo `data/casos_coloracion_grafos.txt`
- Cada caso tiene:
  - Una línea con `n m`: número de nodos y aristas.
  - Luego, `m` líneas con pares de nodos (las aristas).
  - Separación con comentarios como `# Caso X: ...`

### Salida:
- Color por nodo.
- Número de conflictos.
- Número total de colores.
- Iteraciones.
- Tiempo de ejecución.
- Animación `.gif` visualizando todo el proceso.

---

## 📘 Ejemplo: Resolución del Caso 1 paso a paso

### Entrada del caso:
```
# Caso 1: grafo simple de 5 nodos
5 6
0 1
0 2
1 2
1 3
2 4
3 4
```

### Paso 1: Creación del grafo
Se crean 5 nodos (0 a 4) y se agregan las 6 aristas indicadas.

### Paso 2: Coloración aleatoria inicial
Ejemplo inicial:
- Nodo 0: color 0
- Nodo 1: color 0
- Nodo 2: color 1
- Nodo 3: color 2
- Nodo 4: color 1

Conflictos detectados:
- Nodo 0 y 1 (color 0)
- Nodo 2 y 4 (color 1)

Conflictos iniciales: 2

### Paso 3: Búsqueda local con mejor mejora
1. Se evalúa cambiar el color de nodo 1 de 0 → 2 → reduce conflictos a 1.
2. Luego se cambia el color de nodo 4 de 1 → 2 → reduce conflictos a 0.

Coloración final:
- Nodo 0: color 0
- Nodo 1: color 2
- Nodo 2: color 1
- Nodo 3: color 2
- Nodo 4: color 2

Conflictos finales: 0  
Colores usados: 3  
Iteraciones: 2  
Tiempo: 0.002s (ejemplo)

### Paso 4: Intentar con menos colores (k = 2)
Se intenta colorear el grafo usando solo 2 colores. Si ya no se puede resolver sin conflictos, se conserva la mejor solución anterior (k = 3).

---

## 📈 Visualización

Se genera un `.gif` para cada caso resuelto exitosamente sin conflictos.

Para el caso 1:
```
results/grafos_coloreados/caso_1_k3.gif
```

La animación muestra:
1. El grafo vacío.
2. La asignación inicial aleatoria.
3. Conflictos resaltados.
4. Mejoras paso a paso del algoritmo hasta alcanzar una solución válida.

---

## ✅ Conclusiones

- La búsqueda local con mejor mejora permite resolver la mayoría de los grafos eficientemente.
- La reducción progresiva del número de colores optimiza la solución final.
- Las animaciones permiten visualizar claramente cada paso del algoritmo.
- El código está modularizado para su mantenimiento, extensión y evaluación.

---

## 📦 Entregables

- ✅ Código fuente (`src/`)
- ✅ Archivo de entrada (`data/casos_coloracion_grafos.txt`)
- ✅ Resultados (`results/soluciones.txt`)
- ✅ Visualizaciones (`results/grafos_coloreados/`)
- ✅ Informe técnico (`informe.md`)
- ✅ Presentación (`presentacion.pptx`) — por preparar para exposición

---

## 👥 Autores

- [Nombre del equipo o integrantes]
