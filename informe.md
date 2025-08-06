# Informe del Proyecto: Coloración de Grafos con Búsqueda Local

## 🧠 Objetivo del Proyecto

Asignar colores a los vértices de un grafo de forma que no haya dos vértices adyacentes con el mismo color, utilizando la menor cantidad posible de colores.  
Se utilizó una estrategia de **búsqueda local con mejora** para minimizar los conflictos (colisiones de colores) y posteriormente reducir el número de colores.

---

## 🧮 Función Objetivo

Minimizar el número de conflictos, definidos como pares de vértices adyacentes con el mismo color.  
Una vez que se alcanza una solución sin conflictos, se intenta minimizar la cantidad de colores utilizados.

---

## ⚙️ Algoritmo Implementado

Se implementó una versión adaptada del pseudocódigo propuesto en el enunciado del proyecto, siguiendo el enfoque de **búsqueda local con estrategia de mejor mejora**:

1. **Inicialización**: asignación aleatoria de colores a cada nodo, usando un número `k` de colores.
2. **Iteración**: se evalúa cambiar el color de cada nodo a todos los posibles colores diferentes.
3. **Evaluación**: si una nueva asignación reduce los conflictos, se actualiza la solución.
4. **Terminación**: el proceso continúa hasta que no se encuentran mejoras.
5. **Optimización**: si se encuentra una solución sin conflictos, se repite el proceso usando menos colores (`k - 1`).

---

## 🗂 Estructura del Proyecto

