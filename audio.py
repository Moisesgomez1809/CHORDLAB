import ctypes
import math
import pyray as rl

from matematicas import nota_a_frecuencia

# ==========================================
# AUDIO (SINTESIS SENOIDAL EN MEMORIA)
# ==========================================

SAMPLE_RATE = 44100


def crear_sonido_nota(frecuencia, duracion=0.65, volumen=0.22):
    """
    Genera un rl.Sound con onda senoidal + segundo armonico suave
    y envolvente para evitar clics.
    """
    num_samples = int(SAMPLE_RATE * duracion)
    buffer = (ctypes.c_short * num_samples)()

    attack = int(SAMPLE_RATE * 0.015)
    release = int(SAMPLE_RATE * 0.14)

    for i in range(num_samples):
        t = i / SAMPLE_RATE

        if i < attack:
            env = i / max(1, attack)
        elif i > num_samples - release:
            env = max(0.0, (num_samples - i) / max(1, release))
        else:
            progress = (i - attack) / max(1, num_samples - attack - release)
            env = 1.0 - 0.35 * progress

        onda = (
            0.82 * math.sin(2.0 * math.pi * frecuencia * t)
            + 0.18 * math.sin(2.0 * math.pi * (frecuencia * 2.0) * t)
        )

        muestra = max(-1.0, min(1.0, onda * env * volumen))
        buffer[i] = int(muestra * 32767)

    # Constructor posicional de rl.Wave en pyray:
    # (frameCount, sampleRate, sampleSize, channels, data)
    wave = rl.Wave(
        num_samples,
        SAMPLE_RATE,
        16,
        1,
        memoryview(buffer)
    )

    sonido = rl.load_sound_from_wave(wave)
    return sonido, buffer


class GestorAudio:
    """Encargado de inicializar, sintetizar, reproducir y liberar el audio."""

    def __init__(self, habilitado=True):
        self.habilitado = habilitado
        self.sonidos_notas = []
        self._buffers_audio = []

        rl.init_audio_device()
        self._cargar_notas()

    def _cargar_notas(self):
        for idx in range(12):
            freq = nota_a_frecuencia(idx, octava=4)
            snd, buf = crear_sonido_nota(freq, duracion=0.70, volumen=0.20)
            self.sonidos_notas.append(snd)
            self._buffers_audio.append(buf)

    def reproducir_acorde(self, acorde):
        if not self.habilitado:
            return
        for nota in acorde:
            rl.play_sound(self.sonidos_notas[nota])

    def reproducir_nota_unica(self, nota):
        if not self.habilitado:
            return
        rl.play_sound(self.sonidos_notas[nota])

    def alternar_sonido(self):
        self.habilitado = not self.habilitado
        return self.habilitado

    def cerrar(self):
        for snd in self.sonidos_notas:
            rl.unload_sound(snd)
        self.sonidos_notas.clear()
        self._buffers_audio.clear()
        rl.close_audio_device()
