# 🎨 Proyecto: Coloración de Grafos con Búsqueda Local

Este proyecto resuelve el problema de coloración de grafos minimizando conflictos mediante un algoritmo de búsqueda local. Se incluyen visualizaciones animadas del proceso para cada caso, así como informes detallados del resultado.

---

## 📦 Estructura del Proyecto

```
coloracion_grafos/
├── data/
│   └── casos_coloracion_grafos.txt         # Casos de prueba
├── results/
│   ├── soluciones.txt                      # Resultados por caso
│   ├── errores.log                         # Registro de errores
│   └── grafos_coloreados/                  # Animaciones .gif
├── src/
│   ├── main.py                             # Ejecución principal
│   ├── coloring.py                         # Algoritmo de búsqueda local
│   ├── graph_utils.py                      # Carga de grafos desde archivo
│   └── visualization.py                    # Generación de animaciones
├── informe.md                              # Informe técnico del proyecto
└── README.md                               # Este archivo
```

---

## 🚀 Cómo ejecutar el proyecto

### 1. Clona el repositorio
```bash
git clone https://github.com/tu_usuario/coloracion_grafos.git
cd coloracion_grafos
```

### 2. Instala los requisitos
Se recomienda usar Python 3.8+.

#### Instalar dependencias:
```bash
pip install networkx matplotlib imageio
```

### 3. Ejecuta el programa principal
```bash
python src/main.py
```

Esto generará:
- Resultados por cada caso en `results/soluciones.txt`
- Visualizaciones en `results/grafos_coloreados/`
- Registro de errores (si hay problemas con el archivo de entrada) en `results/errores.log`

---

## 📥 Entrada

El archivo `data/casos_coloracion_grafos.txt` debe tener:
- Una línea con `n m` (nodos y aristas)
- m líneas con pares `u v` (aristas)
- Casos separados por comentarios `# Caso X`

---

## 📤 Salida

- Resultados detallados por caso: colores, conflictos, tiempo, iteraciones.
- Animación `.gif` paso a paso para cada solución sin conflictos.
- Errores de lectura (si los hay): `results/errores.log`

---

## 📊 ¿Qué hace el algoritmo?

- Asigna colores aleatoriamente a los nodos.
- Evalúa conflictos (nodos adyacentes con el mismo color).
- Aplica búsqueda local para reducir conflictos paso a paso.
- Intenta usar menos colores si se alcanza una solución sin conflictos.

---

## 🧠 Autores

- [Nombre del equipo o integrantes]
