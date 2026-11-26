# CHORD LAB — Generador Matemático de Acordes

Aplicación interactiva desarrollada en **Python** con **Raylib (`pyray`)** que relaciona las **matemáticas discretas** (aritmética modular $\mathbb{Z}_{12}$) con la teoría musical y la síntesis de sonido en tiempo real.

Permite seleccionar cualquier tónica y tipo de acorde (**Mayor** o **Menor**), visualizar su geometría en el círculo cromático de 12 notas, inspeccionar paso a paso el cálculo matemático y escuchar el acorde generado mediante síntesis senoidal en memoria.

---

## Características

- **Aritmética modular ($\mathbb{Z}_{12}$):** cálculo de acordes Mayores y Menores usando congruencias módulo 12.
- **Visualización geométrica:** representación del acorde como un triángulo inscrito en el círculo musical de 12 nodos con animación al cambiar de acorde.
- **Panel matemático en vivo:** muestra fórmula, sustitución numérica, resultado en módulo 12, nombres de notas y frecuencias en Hz.
- **Síntesis de audio en memoria:** genera ondas senoidales con segundo armónico y envolvente de ataque/liberación directamente en Python, sin depender de archivos `.wav` o `.mp3` externos.

---

## Estructura del proyecto

```text
.
├── main.py          # Punto de entrada: conecta la interfaz, el audio y las matemáticas
├── matematicas.py   # Lógica matemática (Z12, fórmulas, frecuencias en Hz y geometría del círculo)
├── audio.py         # Síntesis de ondas senoidales y gestión de reproducción con Raylib
├── interfaz.py      # Ventana, paleta visual, controles, círculo musical y eventos
├── .gitignore
└── README.md
```

---

## Requisitos

- **Python 3.9+**
- **Raylib para Python (`raylib` / `pyray`)**
- **Windows** (utiliza la tipografía del sistema `segoeui.ttf`; en otros sistemas operativos puede ajustarse la ruta de fuente en `interfaz.py`).

Instalación de dependencias:

```bash
pip install raylib
```

---

## Ejecución

```bash
python main.py
```

### Controles

- **Tónica (`C` – `B`):** selecciona la nota raíz en $\mathbb{Z}_{12}$.
- **Tipo (`Mayor` / `Menor`):** cambia los intervalos del acorde.
- **Escuchar acorde / tecla `Espacio`:** vuelve a reproducir el acorde actual.
- **Botón `ON` / `OFF`:** activa o silencia el audio.

---

## Fundamento matemático

Las 12 notas cromáticas se modelan como el conjunto $\mathbb{Z}_{12} = \{0, 1, 2, \dots, 11\}$, donde $0 = \text{C}, 1 = \text{C\#}, \dots, 11 = \text{B}$:

- **Acorde Mayor:** $M(T) = \{T,\ (T + 4) \bmod 12,\ (T + 7) \bmod 12\}$
- **Acorde Menor:** $m(T) = \{T,\ (T + 3) \bmod 12,\ (T + 7) \bmod 12\}$

Cada nota se convierte a frecuencia en hercios (afinación temperada estándar con $A_4 = 440\text{ Hz}$):

$$f(m) = 440 \cdot 2^{\frac{m - 69}{12}}$$
