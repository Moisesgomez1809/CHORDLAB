import math

# ==========================================
# MATEMATICAS DISCRETAS (Z12) Y ACUSTICA
# ==========================================

NOTES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]


def obtener_intervalos(tipo):
    """Devuelve los intervalos en semitonos para un acorde Mayor o Menor."""
    return [0, 4, 7] if tipo == "Mayor" else [0, 3, 7]


def calcular_acorde(tonica, tipo):
    """Calcula las notas del acorde en aritmetica modular Z12."""
    intervalos = obtener_intervalos(tipo)
    return [(tonica + intervalo) % 12 for intervalo in intervalos]


def obtener_formula(tipo):
    """Devuelve la formula completa en modulo 12."""
    if tipo == "Mayor":
        return "M(T) = {T, (T+4) mod 12, (T+7) mod 12}"
    return "m(T) = {T, (T+3) mod 12, (T+7) mod 12}"


def obtener_formula_corta(tipo):
    """Devuelve la formula resumida para mostrar en el panel."""
    if tipo == "Mayor":
        return "M(T) = {T, T+4, T+7}"
    return "m(T) = {T, T+3, T+7}"


def obtener_sustitucion(tonica, tipo):
    """Devuelve los valores sustituidos antes de aplicar modulo 12."""
    return [tonica + intervalo for intervalo in obtener_intervalos(tipo)]


def nota_a_frecuencia(nota_mod12, octava=4):
    """
    Convierte un indice de Z12 (0 = C, 9 = A) a frecuencia en Hz.
    A4 = 440 Hz -> nota MIDI 69.
    """
    midi_note = 12 * (octava + 1) + nota_mod12
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def calcular_posicion_circulo(nota, centro_x, centro_y, radio):
    """Calcula las coordenadas (x, y) de una nota en el circulo de 12 posiciones."""
    angulo = (2 * math.pi * nota / 12) - math.pi / 2
    x = centro_x + radio * math.cos(angulo)
    y = centro_y + radio * math.sin(angulo)
    return x, y
