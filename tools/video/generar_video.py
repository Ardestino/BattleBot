"""Genera el video promocional del evento Battle Bot (19 de noviembre).

Uso:  python generar_video.py
Salida: BattleBot_19_Noviembre.mp4 (1920x1080, 30 fps, ~20 s, con audio sintetizado)
Requiere: Pillow, numpy, ffmpeg en el PATH.
"""
import math
import os
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))  # raíz del repositorio (tools/video -> raíz)
ROBOT_PNG = os.path.join(RAIZ, "hardware", "cad", "renders", "hercules_iso.png")
SALIDA = os.path.join(AQUI, "BattleBot_19_Noviembre.mp4")
WAV = os.path.join(AQUI, "_audio.wav")

W, H, FPS = 1920, 1080, 30
DUR = 20.0
NFRAMES = int(DUR * FPS)
BPM = 120
BEAT = 60 / BPM

# ---------- textos (edítalos aquí) ----------
TXT_INTRO = "SE ACERCA EL COMBATE..."
TXT_TITULO_1 = "BATTLE"
TXT_TITULO_2 = "BOT"
TXT_SUB = "TORNEO DE COMBATE DE ROBOTS"
TXT_LEMAS = ["CONSTRUYE.", "PROGRAMA.", "DESTRUYE."]
TXT_PREGUNTA = "¿QUIÉN SOBREVIVIRÁ?"
TXT_DIA = "JUEVES"
TXT_NUM = "19"
TXT_MES = "NOVIEMBRE"
TXT_ANIO = "2026"
TXT_CIERRE = "¡NO TE LO PIERDAS!"

# ---------- tiempos de los golpes (s) ----------
T_BATTLE, T_BOT = 3.0, 3.5
T_LEMAS = [7.0, 7.75, 8.5]
T_SC3, T_SC4, T_SC5 = 6.5, 11.5, 15.0
T_VS = 12.0
T_NUM, T_MES, T_CIERRE = 15.5, 16.0, 17.0
IMPACTOS = [T_BATTLE, T_BOT, *T_LEMAS, T_SC4, T_VS, T_NUM, T_MES, T_CIERRE]

FONT_DIR = "C:/Windows/Fonts"


def fuente(nombre, tam):
    for n in (nombre, "impact.ttf", "arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(os.path.join(FONT_DIR, n), tam)
        except OSError:
            continue
    return ImageFont.load_default()


# ---------- utilidades ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_back(x):
    x = clamp(x)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def texto_capa(txt, font, relleno, borde=(0, 0, 0), grosor=6, glow=None, glow_r=18, pad=60):
    """Devuelve una imagen RGBA con el texto, borde y resplandor."""
    tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
    x0, y0, x1, y1 = tmp.textbbox((0, 0), txt, font=font, stroke_width=grosor)
    w, h = x1 - x0 + pad * 2, y1 - y0 + pad * 2
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((pad - x0, pad - y0), txt, font=font, fill=glow + (255,),
                               stroke_width=grosor + 6, stroke_fill=glow + (255,))
        g = g.filter(ImageFilter.GaussianBlur(glow_r))
        capa = Image.alpha_composite(capa, g)
        capa = Image.alpha_composite(capa, g)
    d = ImageDraw.Draw(capa)
    d.text((pad - x0, pad - y0), txt, font=font, fill=relleno, stroke_width=grosor, stroke_fill=borde)
    return capa


def metal(capa, arriba, abajo):
    """Pinta el relleno del texto con un degradado vertical metálico, conservando borde y glow."""
    a = np.array(capa).astype(np.float32)
    h = a.shape[0]
    grad = np.linspace(0, 1, h)[:, None, None]
    col = np.array(arriba, np.float32) * (1 - grad) + np.array(abajo, np.float32) * grad
    # franja brillante a media altura
    brillo = np.exp(-((np.linspace(0, 1, h) - 0.47) ** 2) / 0.002)[:, None, None] * 90
    col = np.clip(col + brillo, 0, 255)
    blanco = (a[..., 0] > 250) & (a[..., 1] > 250) & (a[..., 2] > 250) & (a[..., 3] > 250)
    a[..., :3][blanco] = np.broadcast_to(col, a[..., :3].shape)[blanco]
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def pegar(base, capa, cx, cy, escala=1.0, alpha=1.0):
    if alpha <= 0.01 or escala <= 0.01:
        return
    if abs(escala - 1) > 0.01:
        capa = capa.resize((max(1, int(capa.width * escala)), max(1, int(capa.height * escala))),
                           Image.BILINEAR)
    if alpha < 0.99:
        capa = capa.copy()
        capa.putalpha(capa.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)))


def golpe(t, t0, dur=0.22):
    """Escala de entrada tipo 'slam': grande -> 1 con rebote."""
    if t < t0:
        return 0.0
    x = (t - t0) / dur
    if x >= 1:
        return 1.0
    return 3.2 - 2.2 * ease_out(x)


# ---------- recursos ----------
def recortar_robot():
    img = Image.open(ROBOT_PNG).convert("RGB")
    a = np.array(img).astype(int)
    claro = (a.min(axis=2) > 185) & ((a.max(axis=2) - a.min(axis=2)) < 35)
    m = Image.new("L", img.size)
    m.paste(Image.fromarray((claro * 255).astype(np.uint8), "L"))  # copia editable
    for p in [(0, 0), (m.width - 1, 0), (0, m.height - 1), (m.width - 1, m.height - 1)]:
        ImageDraw.floodfill(m, p, 128)
    alpha = (np.array(m) != 128).astype(np.uint8) * 255
    am = Image.fromarray(alpha, "L").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
    rgba = img.convert("RGBA")
    rgba.putalpha(am)
    return rgba.crop(rgba.getbbox())


def silueta(robot, color=(15, 4, 6)):
    s = Image.new("RGBA", robot.size, color + (255,))
    s.putalpha(robot.getchannel("A"))
    return s.transpose(Image.FLIP_LEFT_RIGHT)


def borde_brillo(robot, color, r=25):
    tam = (robot.width + 160, robot.height + 160)
    a = Image.new("L", tam)
    a.paste(robot.getchannel("A"), (80, 80))
    a = a.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(r))
    g = Image.new("RGBA", tam, color + (0,))
    g.putalpha(a)
    lienzo = Image.new("RGBA", tam, (0, 0, 0, 0))
    lienzo.alpha_composite(g)
    lienzo.alpha_composite(g)
    lienzo.alpha_composite(robot, (80, 80))
    return lienzo


yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIGNETA = (1 - 0.75 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2)[..., None]
VIGNETA = np.clip(VIGNETA, 0.25, 1)


def fondo_degradado(c_centro, c_borde):
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 1.6
    r = np.clip(r, 0, 1)[..., None]
    return (np.array(c_centro, np.float32) * (1 - r) + np.array(c_borde, np.float32) * r)


FONDO_ROJO = fondo_degradado((120, 15, 10), (8, 0, 0))
FONDO_ACERO = fondo_degradado((45, 50, 60), (5, 6, 8))
FONDO_NARANJA = fondo_degradado((200, 90, 10), (40, 8, 0))
FONDO_VIOLETA = fondo_degradado((90, 0, 30), (5, 0, 4))


def franjas(t, base, alpha=0.18, vel=120):
    """Franjas de peligro diagonales que se desplazan."""
    f = ((xx + yy + t * vel) % 160) < 80
    out = base.copy()
    out[f] = out[f] * (1 - alpha) + np.array([255, 190, 0], np.float32) * alpha
    return out


def rejilla(t, base, color=(255, 80, 20), intens=0.5):
    """Suelo de rejilla en perspectiva (estilo arena)."""
    horizonte = H * 0.55
    out = base.copy()
    mask = yy > horizonte
    z = 400 / np.maximum(yy - horizonte, 1)
    lin_z = (np.abs(((z + t * 2.0) % 1.0) - 0.5) > 0.47)
    xw = (xx - W / 2) * z / 400
    lin_x = (np.abs((xw * 6) % 1.0 - 0.5) > 0.46)
    lin = (lin_z | lin_x) & mask
    fade = np.clip((yy - horizonte) / (H - horizonte), 0, 1)
    k = (lin * fade * intens)[..., None]
    out = out * (1 - k) + np.array(color, np.float32) * k
    return out


class Chispas:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.p = []  # [x, y, vx, vy, vida, vida0]

    def rafaga(self, x, y, n, vel=1400, ang=(0, 2 * math.pi)):
        for _ in range(n):
            a = self.rng.uniform(*ang)
            v = self.rng.uniform(0.3, 1.0) * vel
            vida = self.rng.uniform(0.3, 0.9)
            self.p.append([x, y, math.cos(a) * v, math.sin(a) * v, vida, vida])

    def paso(self, dt):
        vivos = []
        for q in self.p:
            q[0] += q[2] * dt
            q[1] += q[3] * dt
            q[3] += 1800 * dt
            q[2] *= 0.985
            q[4] -= dt
            if q[4] > 0 and -50 < q[0] < W + 50 and q[1] < H + 50:
                vivos.append(q)
        self.p = vivos

    def dibujar(self, img):
        d = ImageDraw.Draw(img)
        for x, y, vx, vy, vida, v0 in self.p:
            k = vida / v0
            col = (255, int(150 + 105 * k), int(60 * k), int(255 * min(1, k * 1.5)))
            d.line([(x, y), (x - vx * 0.02, y - vy * 0.02)], fill=col, width=3 if k > 0.5 else 2)


def rayo(d, x0, y0, x1, y1, rng, color, ancho=5):
    pts = [(x0, y0)]
    n = 12
    for i in range(1, n):
        f = i / n
        pts.append((x0 + (x1 - x0) * f + rng.uniform(-60, 60), y0 + (y1 - y0) * f + rng.uniform(-30, 30)))
    pts.append((x1, y1))
    d.line(pts, fill=color, width=ancho + 8)
    d.line(pts, fill=(255, 255, 255, 255), width=ancho)


# ---------- audio ----------
SR = 44100


def generar_audio():
    n = int(DUR * SR)
    out = np.zeros(n, np.float64)
    rng = np.random.default_rng(7)
    t_all = np.arange(n) / SR

    def add(sig, t0, gain=1.0):
        i = int(t0 * SR)
        if i >= n:
            return
        j = min(n, i + len(sig))
        out[i:j] += sig[: j - i] * gain

    def kick():
        t = np.arange(int(0.45 * SR)) / SR
        f = 45 + 110 * np.exp(-t * 28)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)

    def snare():
        t = np.arange(int(0.25 * SR)) / SR
        ruido = rng.standard_normal(len(t))
        ruido = np.diff(ruido, prepend=0)
        return (ruido * 0.6 + np.sin(2 * np.pi * 190 * t) * 0.5) * np.exp(-t * 18)

    def hat():
        t = np.arange(int(0.06 * SR)) / SR
        r = np.diff(np.diff(rng.standard_normal(len(t)), prepend=0), prepend=0)
        return r * np.exp(-t * 70) * 0.25

    def impacto(largo=2.0):
        t = np.arange(int(largo * SR)) / SR
        f = 30 + 90 * np.exp(-t * 6)
        boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
        ruido = rng.standard_normal(len(t))
        # paso bajo simple
        k = 0.08
        lp = np.zeros_like(ruido)
        for i in range(1, len(ruido)):
            lp[i] = lp[i - 1] + k * (ruido[i] - lp[i - 1])
        crash = (ruido * 0.25 * np.exp(-t * 5)) + lp * 1.2 * np.exp(-t * 3)
        metal_ = np.sin(2 * np.pi * 1730 * t) * np.sin(2 * np.pi * 2410 * t) * np.exp(-t * 6) * 0.25
        return np.tanh((boom * 1.4 + crash + metal_) * 1.5)

    # riser de la intro
    t = np.arange(int(3.0 * SR)) / SR
    env = (t / 3.0) ** 2
    f = 150 + 1500 * (t / 3.0) ** 2
    riser = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25 * env
    riser += rng.standard_normal(len(t)) * 0.18 * env
    add(riser, 0.0)
    # dron grave de la intro
    add(np.sin(2 * np.pi * 41 * t) * 0.35 * np.minimum(1, t), 0.0)

    # ritmo
    b = 3.0
    while b < 18.9:
        add(kick(), b, 0.9)
        idx = round((b - 3.0) / BEAT)
        if b >= T_SC3 and idx % 2 == 1:
            add(snare(), b, 0.45)
        if b >= T_SC3:
            add(hat(), b + BEAT / 2, 1.0)
        b += BEAT

    # bajo distorsionado (patrón en semicorcheas sobre La/Fa/Sol)
    notas = [55.0, 55.0, 43.65, 49.0]
    seg = 3.0
    while seg < 17.0:
        compas = int((seg - 3.0) / (BEAT * 4)) % 4
        fr = notas[compas]
        largo = BEAT / 2
        tt = np.arange(int(largo * SR)) / SR
        saw = 2 * ((tt * fr) % 1) - 1
        nota = np.tanh(saw * 3) * np.exp(-tt * 6) * 0.22
        add(nota, seg)
        seg += BEAT / 2

    for ti in IMPACTOS:
        add(impacto(2.2 if ti != T_CIERRE else 3.0), ti, 0.9)

    # sub final
    tt = np.arange(int(3.0 * SR)) / SR
    add(np.sin(2 * np.pi * (60 - 25 * tt / 3) * tt) * np.exp(-tt * 1.2) * 0.6, T_CIERRE)

    # fundido final
    fade = np.clip((DUR - t_all) / 1.2, 0, 1)
    out *= fade
    out = np.tanh(out * 1.1)
    out /= np.max(np.abs(out)) + 1e-9
    out *= 0.89
    pcm = (out * 32767).astype(np.int16)
    est = np.stack([pcm, pcm], axis=1)
    with wave.open(WAV, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(est.tobytes())


# ---------- video ----------
def main():
    print("Generando audio...")
    generar_audio()

    print("Preparando recursos...")
    robot = recortar_robot()
    esc_robot = 640 / robot.height
    robot = robot.resize((int(robot.width * esc_robot), 640), Image.LANCZOS)
    robot_glow = borde_brillo(robot, (255, 120, 20))
    robot_vs = borde_brillo(robot.resize((int(robot.width * 0.85), int(robot.height * 0.85)), Image.LANCZOS),
                            (255, 170, 40), r=20)
    rival = borde_brillo(silueta(robot.resize((int(robot.width * 0.85), int(robot.height * 0.85)))),
                         (255, 20, 40), r=20)

    f_mono = fuente("consolab.ttf", 64)
    f_titulo = fuente("impact.ttf", 330)
    f_sub = fuente("ariblk.ttf", 58)
    f_lema = fuente("impact.ttf", 150)
    f_vs = fuente("impact.ttf", 380)
    f_preg = fuente("impact.ttf", 110)
    f_num = fuente("impact.ttf", 520)
    f_mes = fuente("impact.ttf", 190)
    f_dia = fuente("ariblk.ttf", 80)
    f_cierre = fuente("impact.ttf", 120)
    f_q = fuente("impact.ttf", 200)

    BLANCO = (255, 255, 255)
    c_battle = metal(texto_capa(TXT_TITULO_1, f_titulo, BLANCO, (20, 0, 0), 10, (255, 60, 0), 30),
                     (255, 240, 200), (200, 60, 0))
    c_bot = metal(texto_capa(TXT_TITULO_2, f_titulo, BLANCO, (20, 0, 0), 10, (255, 60, 0), 30),
                  (255, 240, 200), (200, 60, 0))
    c_sub = texto_capa(TXT_SUB, f_sub, (255, 210, 60), (0, 0, 0), 4, (0, 0, 0), 8)
    c_lemas = [texto_capa(s, f_lema, BLANCO, (0, 0, 0), 7, c, 22)
               for s, c in zip(TXT_LEMAS, [(255, 170, 0), (0, 170, 255), (255, 30, 30)])]
    c_vs = metal(texto_capa("VS", f_vs, BLANCO, (0, 0, 0), 12, (255, 255, 120), 35),
                 (255, 255, 230), (255, 150, 0))
    c_preg = texto_capa(TXT_PREGUNTA, f_preg, BLANCO, (0, 0, 0), 7, (255, 0, 40), 20)
    c_q = texto_capa("???", f_q, (255, 40, 50), (0, 0, 0), 8, (255, 0, 0), 25)
    c_dia = texto_capa(TXT_DIA, f_dia, (255, 210, 60), (0, 0, 0), 5, (0, 0, 0), 8)
    c_num = metal(texto_capa(TXT_NUM, f_num, BLANCO, (20, 0, 0), 14, (255, 70, 0), 40),
                  (255, 250, 220), (230, 70, 0))
    c_mes = metal(texto_capa(TXT_MES, f_mes, BLANCO, (20, 0, 0), 9, (255, 70, 0), 28),
                  (255, 250, 220), (230, 70, 0))
    c_anio = texto_capa(TXT_ANIO, f_dia, BLANCO, (0, 0, 0), 5, (0, 0, 0), 8)
    c_cierre = texto_capa(TXT_CIERRE, f_cierre, (255, 230, 0), (0, 0, 0), 8, (255, 40, 0), 22)

    chispas = Chispas(1)
    rng_fx = np.random.default_rng(3)
    disparadas = set()

    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", WAV,
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", SALIDA]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    dt = 1 / FPS
    for fi in range(NFRAMES):
        t = fi * dt

        # disparar ráfagas de chispas en los impactos
        for ti in IMPACTOS:
            if ti not in disparadas and t >= ti:
                disparadas.add(ti)
                chispas.rafaga(W / 2 + rng_fx.uniform(-300, 300), H / 2 + rng_fx.uniform(-150, 150), 90)
                chispas.rafaga(0, H * 0.8, 40, 1600, (-1.2, -0.3))
                chispas.rafaga(W, H * 0.8, 40, 1600, (math.pi + 0.3, math.pi + 1.2))
        if t < T_BATTLE and fi % 2 == 0:
            chispas.rafaga(rng_fx.uniform(0, W), -10, 3, 500, (1.2, 1.9))
        if T_SC3 <= t < T_SC4 and fi % 3 == 0:
            chispas.rafaga(rng_fx.uniform(W * 0.45, W * 0.9), H * 0.92, 4, 900, (-2.2, -0.9))
        if t >= T_SC5 and fi % 4 == 0:
            chispas.rafaga(rng_fx.uniform(0, W), H + 5, 3, 1100, (-2.0, -1.1))
        chispas.paso(dt)

        pulso = math.exp(-((t - T_BATTLE) % BEAT) * 6) if t >= T_BATTLE else 0

        # ---------- escena ----------
        if t < T_BATTLE:  # intro
            base = FONDO_ACERO * (0.25 + 0.15 * (t / T_BATTLE))
            if rng_fx.random() < 0.08:
                base = base * 1.8
            img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
            n = int(len(TXT_INTRO) * clamp((t - 0.4) / 1.6))
            if n > 0:
                cursor = "_" if int(t * 4) % 2 == 0 else " "
                c = texto_capa(TXT_INTRO[:n] + cursor, f_mono, (255, 60, 40), (0, 0, 0), 0, (255, 0, 0), 12)
                img.alpha_composite(c, (int(W / 2 - texto_capa(TXT_INTRO + "_", f_mono, (0, 0, 0), grosor=0).width / 2),
                                        int(H / 2 - c.height / 2)))
        elif t < T_SC3:  # título
            base = franjas(t, FONDO_ROJO, 0.10 + 0.08 * pulso)
            base = rejilla(t, base, (255, 90, 20), 0.6)
            img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
            pegar(img, c_battle, W / 2, H / 2 - 150, golpe(t, T_BATTLE))
            pegar(img, c_bot, W / 2, H / 2 + 140, golpe(t, T_BOT))
            if t > 4.5:
                k = ease_out((t - 4.5) / 0.4)
                pegar(img, c_sub, W / 2, H / 2 + 380 + 40 * (1 - k), 1.0, k)
        elif t < T_SC4:  # robot + lemas
            base = rejilla(t, FONDO_ACERO, (255, 140, 30), 0.55)
            # foco giratorio
            ang = math.sin(t * 1.3) * 0.35
            foco = np.exp(-((xx - (W * 0.68 + math.sin(ang) * 400)) ** 2) / (2 * 380 ** 2))[..., None]
            base = base + foco * np.array([90, 55, 20], np.float32) * (0.8 + 0.4 * pulso)
            img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
            k = ease_back((t - T_SC3) / 0.6)
            rx = W + 500 - (W + 500 - W * 0.70) * k
            ry = H * 0.58 + math.sin(t * 6) * 8 - pulso * 10
            # sombra
            ImageDraw.Draw(img).ellipse([rx - 300, H * 0.84, rx + 300, H * 0.84 + 50], fill=(0, 0, 0, 140))
            pegar(img, robot_glow, rx, ry, 1.0 + 0.02 * pulso)
            for i, (cl, tl) in enumerate(zip(c_lemas, T_LEMAS)):
                if t >= tl:
                    s = golpe(t, tl, 0.18)
                    pegar(img, cl, W * 0.28, H * 0.27 + i * 210, s)
        elif t < T_SC5:  # VS
            izq = FONDO_NARANJA
            der = FONDO_VIOLETA
            corte = W / 2 + (yy - H / 2) * 0.25
            mezcla = (xx < corte)[..., None]
            base = np.where(mezcla, izq, der)
            base = franjas(t, base, 0.08)
            img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
            ka = ease_out((t - T_SC4) / 0.45)
            pegar(img, robot_vs, -300 + (W * 0.25 + 300) * ka, H * 0.55 + math.sin(t * 5) * 6)
            pegar(img, rival, W + 300 - (W * 0.25 + 300) * ka, H * 0.55 + math.sin(t * 5 + 1) * 6)
            if t >= T_SC4 + 0.3:
                pegar(img, c_q, W * 0.78, H * 0.18 + math.sin(t * 8) * 5, 1.0,
                      0.7 + 0.3 * math.sin(t * 12))
            if t >= T_VS:
                d = ImageDraw.Draw(img)
                if int(t * FPS) % 3 != 0 and t < T_VS + 1.5:
                    rayo(d, W / 2 + rng_fx.uniform(-100, 100), 0, W / 2, H / 2, rng_fx, (255, 240, 120, 120))
                    rayo(d, W / 2, H / 2, W / 2 + rng_fx.uniform(-150, 150), H, rng_fx, (255, 240, 120, 120))
                pegar(img, c_vs, W / 2, H / 2 - 20, golpe(t, T_VS) * (1 + 0.04 * pulso))
            if t >= 13.0:
                k = ease_out((t - 13.0) / 0.4)
                pegar(img, c_preg, W / 2, H * 0.89 + 60 * (1 - k), 1.0, k)
        else:  # fecha
            base = franjas(t, FONDO_ROJO, 0.06 + 0.06 * pulso, 60)
            base = rejilla(t, base, (255, 120, 20), 0.5)
            img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
            if t >= T_SC5 + 0.2:
                k = ease_out((t - T_SC5 - 0.2) / 0.3)
                pegar(img, c_dia, W / 2, H * 0.12 - 40 * (1 - k), 1.0, k)
            # 19 grande a la izquierda, mes a la derecha
            if t >= T_NUM:
                pegar(img, c_num, W * 0.30, H * 0.45, golpe(t, T_NUM, 0.25) * (1 + 0.03 * pulso))
            if t >= T_MES:
                pegar(img, c_mes, W * 0.66, H * 0.40, golpe(t, T_MES, 0.2))
                k = ease_out((t - T_MES - 0.3) / 0.3)
                pegar(img, c_anio, W * 0.66, H * 0.56, 1.0, k)
            if t >= T_CIERRE:
                s = golpe(t, T_CIERRE, 0.2) * (1 + 0.05 * math.sin((t - T_CIERRE) * 2 * math.pi / BEAT))
                pegar(img, c_cierre, W / 2, H * 0.84, s)

        chispas.dibujar(img)
        arr = np.array(img.convert("RGB")).astype(np.float32)

        # destello + sacudida + aberración cromática en impactos
        flash = 0.0
        sacudida = 0.0
        for ti in IMPACTOS:
            if 0 <= t - ti < 0.4:
                e = math.exp(-(t - ti) * 12)
                flash = max(flash, e * 0.85)
                sacudida = max(sacudida, e * 28)
        for tc in (T_SC3, T_SC5):
            if 0 <= t - tc < 0.2:
                flash = max(flash, 1 - (t - tc) / 0.2)
        if sacudida > 1:
            dx, dy = int(rng_fx.uniform(-1, 1) * sacudida), int(rng_fx.uniform(-1, 1) * sacudida)
            arr = np.roll(arr, (dy, dx), axis=(0, 1))
            s = int(sacudida / 2)
            if s > 0:
                arr[..., 0] = np.roll(arr[..., 0], s, axis=1)
                arr[..., 2] = np.roll(arr[..., 2], -s, axis=1)

        arr = arr * VIGNETA
        # líneas de escaneo sutiles
        arr[::3] *= 0.93
        if flash > 0:
            arr = arr * (1 - flash) + 255 * flash
        # fundido de entrada / salida
        fin = clamp((DUR - t) / 0.8)
        ini = clamp(t / 0.3)
        arr *= min(fin, ini)

        proc.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
        if fi % 30 == 0:
            print(f"  fotograma {fi}/{NFRAMES}")
            if fi in (60, 150, 240, 330, 420, 540):
                Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(
                    os.path.join(AQUI, f"_preview_{fi:03d}.jpg"), quality=80)

    proc.stdin.close()
    proc.wait()
    os.remove(WAV)
    print("Listo:", SALIDA)


if __name__ == "__main__":
    main()
