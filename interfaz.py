import os
import pyray as rl

from matematicas import (
    NOTES,
    calcular_posicion_circulo,
    nota_a_frecuencia,
    obtener_formula_corta,
    obtener_sustitucion,
)

# ==========================================
# CONFIGURACION DE VENTANA Y ESTILO
# ==========================================

WIDTH = 1280
HEIGHT = 820
FONT_SPACING = 0.5

# ---------- PALETA MINIMALISTA (BLANCO + AZUL MARINO) ----------
BG = rl.Color(255, 255, 255, 255)         # Blanco puro
PANEL = rl.Color(246, 249, 253, 255)      # Blanco azulado muy suave
BORDER = rl.Color(214, 224, 238, 255)     # Borde sutil azul grisaceo
NAVY = rl.Color(15, 37, 68, 255)          # Azul marino principal
NAVY_MID = rl.Color(30, 64, 112, 255)     # Azul marino medio
NAVY_SOFT = rl.Color(92, 114, 145, 255)   # Azul grisaceo para etiquetas
ACCENT = rl.Color(23, 78, 166, 255)       # Azul marino brillante / acento
DARK_NODE = rl.Color(235, 241, 249, 255)

# ---------- GEOMETRIA ----------
CENTER_X = 685
CENTER_Y = 435
RADIUS = 255
NODE_RADIUS = 23


class Interfaz:
    """Encargada de la ventana, tipografia, dibujo de componentes y lectura de controles."""

    def __init__(self):
        rl.init_window(WIDTH, HEIGHT, "CHORD LAB | Matematicas Discretas")
        font_path = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "segoeui.ttf")
        self.ui_font = rl.load_font_ex(font_path, 64, None, 0)
        if not rl.is_font_valid(self.ui_font):
            rl.close_window()
            raise RuntimeError(f"No se pudo cargar la tipografia: {font_path}")
        rl.set_target_fps(60)

    def cerrar(self):
        rl.unload_font(self.ui_font)
        rl.close_window()

    # ==========================================
    # FUNCIONES DE DIBUJO MINIMALISTAS
    # ==========================================

    def texto(self, contenido, x, y, size=20, color=NAVY):
        rl.draw_text_ex(
            self.ui_font,
            str(contenido),
            rl.Vector2(float(x), float(y)),
            float(size),
            FONT_SPACING,
            color
        )

    def ancho_texto(self, contenido, size):
        return rl.measure_text_ex(
            self.ui_font,
            str(contenido),
            float(size),
            FONT_SPACING
        ).x

    def rectangulo(self, x, y, w, h, color=PANEL, borde=BORDER):
        rect = rl.Rectangle(x, y, w, h)
        rl.draw_rectangle_rounded(rect, 0.12, 8, color)
        rl.draw_rectangle_rounded_lines_ex(rect, 0.12, 8, 1.0, borde)
        return rect

    def boton(self, x, y, w, h, label, seleccionado, color_activo=NAVY):
        rect = rl.Rectangle(x, y, w, h)
        fondo = color_activo if seleccionado else PANEL
        borde = color_activo if seleccionado else BORDER
        color_texto = BG if seleccionado else NAVY

        rl.draw_rectangle_rounded(rect, 0.18, 8, fondo)
        rl.draw_rectangle_rounded_lines_ex(rect, 0.18, 8, 1.2, borde)

        text_width = self.ancho_texto(label, 19)
        self.texto(
            label,
            x + (w - text_width) / 2,
            y + (h - 19) / 2,
            19,
            color_texto
        )
        return rect

    def obtener_posicion(self, nota):
        x, y = calcular_posicion_circulo(nota, CENTER_X, CENTER_Y, RADIUS)
        return rl.Vector2(x, y)

    # ==========================================
    # SECCIONES DE LA INTERFAZ
    # ==========================================

    def dibujar_encabezado(self):
        self.texto("CHORD LAB", 40, 34, 32, NAVY)
        self.texto("MATEMATICAS DISCRETAS  |  Z12", 265, 46, 15, NAVY_SOFT)
        rl.draw_line(40, 88, 1245, 88, BORDER)

    def dibujar_pie(self):
        rl.draw_line(40, 742, 1245, 742, BORDER)
        self.texto("Z12 = {0, 1, 2, ..., 11}   ·   ESPACIO: reproducir", 40, 758, 15, NAVY_SOFT)
        self.texto("CHORD LAB v1.1", 1125, 758, 15, NAVY_SOFT)

    def dibujar_circulo(self, acorde, tonica, tipo_acorde, progreso_animacion):
        color_acorde = ACCENT if tipo_acorde == "Mayor" else NAVY_MID

        rl.draw_circle_lines(CENTER_X, CENTER_Y, RADIUS, BORDER)
        rl.draw_circle_lines(CENTER_X, CENTER_Y, 92, BORDER)

        puntos = [self.obtener_posicion(nota) for nota in acorde]

        segmentos = [
            (puntos[0], puntos[1]),
            (puntos[1], puntos[2]),
            (puntos[2], puntos[0])
        ]

        cantidad = min(3, int(progreso_animacion * 3) + 1)

        for i in range(cantidad):
            inicio, fin = segmentos[i]
            rl.draw_line_ex(inicio, fin, 3.0, color_acorde)

        for i in range(12):
            posicion = self.obtener_posicion(i)
            seleccionado = i in acorde

            color = color_acorde if seleccionado else DARK_NODE
            borde_nodo = color_acorde if seleccionado else BORDER
            color_etiqueta = BG if seleccionado else NAVY
            radio = NODE_RADIUS + 2 if seleccionado else NODE_RADIUS

            rl.draw_circle_v(posicion, radio, color)
            rl.draw_circle_lines(int(posicion.x), int(posicion.y), radio, borde_nodo)

            ancho = self.ancho_texto(NOTES[i], 17)
            self.texto(
                NOTES[i],
                posicion.x - ancho / 2,
                posicion.y - 8,
                17,
                color_etiqueta
            )

        rl.draw_circle(CENTER_X, CENTER_Y, 48, BG)
        rl.draw_circle_lines(CENTER_X, CENTER_Y, 48, BORDER)

        ancho = self.ancho_texto(NOTES[tonica], 26)
        self.texto(
            NOTES[tonica],
            CENTER_X - ancho // 2,
            CENTER_Y - 13,
            26,
            NAVY
        )

    def dibujar_controles(self, tonica, tipo_acorde, sonido_activo):
        self.texto("TONICA", 40, 122, 15, NAVY_SOFT)

        botones_notas = []
        for i in range(12):
            fila = i // 3
            columna = i % 3

            x = 40 + columna * 88
            y = 152 + fila * 56

            rect = self.boton(x, y, 76, 42, NOTES[i], tonica == i, NAVY)
            botones_notas.append((rect, i))

        self.texto("TIPO", 40, 405, 15, NAVY_SOFT)

        boton_mayor = self.boton(40, 435, 125, 44, "Mayor", tipo_acorde == "Mayor", ACCENT)
        boton_menor = self.boton(180, 435, 125, 44, "Menor", tipo_acorde == "Menor", NAVY_MID)

        self.texto("AUDIO", 40, 505, 15, NAVY_SOFT)

        boton_escuchar = self.boton(40, 535, 165, 44, "Escuchar acorde", False, NAVY)
        boton_sonido = self.boton(
            215, 535, 90, 44,
            "ON" if sonido_activo else "OFF",
            sonido_activo,
            NAVY_MID
        )

        return botones_notas, boton_mayor, boton_menor, boton_escuchar, boton_sonido

    def dibujar_resultado(self, acorde, tonica, tipo_acorde):
        self.rectangulo(990, 122, 255, 560, PANEL, BORDER)

        self.texto("ACORDE", 1015, 148, 14, NAVY_SOFT)
        self.texto(f"{NOTES[tonica]} {tipo_acorde}", 1015, 174, 28, NAVY)

        rl.draw_line(1015, 222, 1220, 222, BORDER)

        self.texto("FORMULA", 1015, 242, 14, NAVY_SOFT)
        formula = obtener_formula_corta(tipo_acorde)
        self.texto(formula, 1015, 268, 17, NAVY)

        self.texto("SUSTITUCION", 1015, 318, 14, NAVY_SOFT)
        sust = obtener_sustitucion(tonica, tipo_acorde)
        self.texto("{" + ", ".join(map(str, sust)) + "}", 1015, 344, 21, NAVY_MID)

        self.texto("MODULO 12", 1015, 394, 14, NAVY_SOFT)
        self.texto("{" + ", ".join(map(str, acorde)) + "}", 1015, 420, 22, ACCENT)

        rl.draw_line(1015, 468, 1220, 468, BORDER)

        self.texto("NOTAS", 1015, 488, 14, NAVY_SOFT)
        self.texto(" - ".join(NOTES[n] for n in acorde), 1015, 516, 23, NAVY)
        self.texto("Tonica / Tercera / Quinta", 1015, 554, 14, NAVY_SOFT)

        self.texto("FRECUENCIAS (HZ)", 1015, 594, 14, NAVY_SOFT)
        freqs = ", ".join(f"{nota_a_frecuencia(n, 4):.0f}" for n in acorde)
        self.texto(f"{freqs} Hz", 1015, 620, 15, NAVY_MID)

    # ==========================================
    # DETECCION DE EVENTOS DE ENTRADA
    # ==========================================

    def leer_evento(self, controles):
        """
        Revisa clics del mouse y teclado sobre los controles.
        Devuelve una tupla (accion, valor) o None si no hubo evento.
        """
        botones_notas, boton_mayor, boton_menor, boton_escuchar, boton_sonido = controles

        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            mouse = rl.get_mouse_position()

            for rect, numero in botones_notas:
                if rl.check_collision_point_rec(mouse, rect):
                    return ("tonica", numero)

            if rl.check_collision_point_rec(mouse, boton_mayor):
                return ("tipo", "Mayor")

            if rl.check_collision_point_rec(mouse, boton_menor):
                return ("tipo", "Menor")

            if rl.check_collision_point_rec(mouse, boton_escuchar):
                return ("reproducir", None)

            if rl.check_collision_point_rec(mouse, boton_sonido):
                return ("alternar_sonido", None)

        if rl.is_key_pressed(rl.KEY_SPACE):
            return ("reproducir", None)

        return None
