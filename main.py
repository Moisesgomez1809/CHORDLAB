import pyray as rl

from audio import GestorAudio
from interfaz import BG, Interfaz
from matematicas import calcular_acorde

# ==========================================
# CHORD LAB
# Generador matematico de acordes + Audio
# Python + Raylib
# ==========================================


def main():
    ui = Interfaz()
    audio = GestorAudio(habilitado=True)

    tonic = 0
    chord_type = "Mayor"
    animation_progress = 1.0

    audio.reproducir_acorde(calcular_acorde(tonic, chord_type))

    try:
        while not rl.window_should_close():
            rl.begin_drawing()
            rl.clear_background(BG)

            ui.dibujar_encabezado()

            controles = ui.dibujar_controles(tonic, chord_type, audio.habilitado)
            evento = ui.leer_evento(controles)

            if evento is not None:
                accion, valor = evento

                if accion == "tonica":
                    tonic = valor
                    animation_progress = 0.0
                    audio.reproducir_acorde(calcular_acorde(tonic, chord_type))
                elif accion == "tipo" and chord_type != valor:
                    chord_type = valor
                    animation_progress = 0.0
                    audio.reproducir_acorde(calcular_acorde(tonic, chord_type))
                elif accion == "reproducir":
                    audio.reproducir_acorde(calcular_acorde(tonic, chord_type))
                elif accion == "alternar_sonido":
                    if audio.alternar_sonido():
                        audio.reproducir_acorde(calcular_acorde(tonic, chord_type))

            acorde = calcular_acorde(tonic, chord_type)

            if animation_progress < 1:
                animation_progress = min(1.0, animation_progress + 0.035)

            ui.dibujar_circulo(acorde, tonic, chord_type, animation_progress)
            ui.dibujar_resultado(acorde, tonic, chord_type)
            ui.dibujar_pie()

            rl.end_drawing()
    finally:
        audio.cerrar()
        ui.cerrar()


if __name__ == "__main__":
    main()
