# /// script
# dependencies = ["bd_warehouse"]
# ///
"""Ensamble de ejemplo v1 del BattleBot: orugas triangulares con tracción abajo + sierra vertical de 6".

Es un modelo de ejemplo para discutir el acomodo, no un diseño cerrado. Usa los componentes
registrados en hardware/referencias/ y tornillería y rodamientos estándar.

Cambios respecto a v0:
- La catarina motriz está en la esquina trasera de abajo y la rueda de arriba es libre. Si se pierde
  la oruga, el robot baja ~8 mm y sigue andando sobre las catarinas (con 2 O-rings 35 x 3 cada una)
  y las ruedas delanteras.
- Arma: hoja de sierra de 6" (Ø152.4 x 1.8 mm) de la desbrozadora de 21 V, en eje de 12 mm con
  2 rodamientos 6201-2RS, movida por banda HTD-5M de 310 mm desde el motor de la desbrozadora
  (775 de 20 V: Ø41.81 x 67 mm, eje de 5 x 17 mm; barrenos de la cara supuestos).
- Todos los tornillos que entran por debajo de la placa base son de cabeza avellanada (al ras).
- Martillo: el monito del logotipo del CETI (escala 3x del STL de referencia) parado con los dos pies en
  el eje de giro, un eje de 8 mm entre las placas laterales (2 x 608-2RS). Gira hasta 105° hacia atrás
  (lado contrario a la sierra) movido por un servo MG995 con engranes 1:1 de módulo 1.5 (20/20 dientes).

Resto:
- Tracción: 2 motorreductores JGB37-520 atornillados a las placas laterales (6 x M3 avellanados en
  círculo de Ø31) y orugas triangulares impresas de 43 eslabones (paso 12.5 mm, pernos de 3 mm).
- Ruedas libres con 2 rodamientos 606-2RS cada una sobre tornillo M6; la delantera va en ranura
  para tensar la oruga.
- Electrónica: baterías apiladas al centro, Freenove + ESP32-S3 y relevador en una cubierta encima;
  L298N al frente sobre la placa base.

Ejes: X hacia el frente (lado del arma), Y hacia la izquierda, Z hacia arriba; el piso es z = 0.
Medidas en mm. Las piezas compradas sin plano (Freenove, L298N, baterías, relevador, motor del arma)
son volúmenes aproximados para revisar espacio: hay que medirlas.
"""
import math

import build123d as bd
from cad import model

# ---------------------------------------------------------------- Oruga
P = 12.5             # paso del eslabón (entre pernos)
LINK_W = 30.0        # ancho de la oruga
LINK_T = 5.0         # espesor de la placa del eslabón
GROUSER_H = 2.0      # taco de agarre
HORN_H = 5.0         # guía central (entra en la ranura de las ruedas y en la catarina)
HORN_W = 7.0
HORN_L = 6.0
PIN_D = 3.2          # perno: hilo de nylon de 3 mm (desbrozadora) o varilla de 3 mm
N_TEETH = 12
N_LINKS = 43

RC_SPROCKET = P / (2 * math.sin(math.pi / N_TEETH))           # radio de los pernos en la catarina
LINK_IN_SPROCKET = math.sqrt(RC_SPROCKET**2 - (P / 2) ** 2) - LINK_T / 2   # cara interior del eslabón (20.83)
R_SPROCKET = 20.2                                              # rin de la catarina
ORING_CS = 3.0                                                 # O-ring 35 x 3 mm (NBR)
ORING_R_IN = 17.7                                              # fondo de la ranura (O-ring estirado 1 %)
ORING_Z = (4.0, 24.0)                                          # posición de las ranuras (local)
GRUB_Z = 6.5                                                   # prisionero M3 (local; 1 mm bajo los dientes)
R_IDLER = 17.8                                                 # rueda libre (Ø35.6)
RC_IDLER = math.sqrt((18.0 + LINK_T / 2) ** 2 + (P / 2) ** 2)  # radio de los pernos en la rueda libre
IDLER_Z = RC_IDLER + LINK_T / 2 + GROUSER_H                    # la oruga toca el piso en z = 0
SPROCKET_X = -80.0                                             # catarina motriz: abajo atrás
SPROCKET_Z = RC_SPROCKET + LINK_T / 2 + GROUSER_H
TOP_X, TOP_Z = 0.0, IDLER_Z + 90.0                             # rueda libre de arriba
FRONT_X_RANGE = (65.0, 95.0)                                   # la delantera tensa (se calcula)
TENSION_SLOT = 4.0

# ---------------------------------------------------------------- Chasis
FRAME_IN = 75.0      # cara interior de la placa lateral izquierda (y)
FRAME_T = 5.0        # aluminio 6061 de 5 mm
FRAME_OUT = FRAME_IN + FRAME_T
WHEEL_W = 28.0
WHEEL_Y0 = FRAME_OUT + 4.0
TRACK_Y = WHEEL_Y0 + WHEEL_W / 2
BASE_Z0 = 12.0       # placa base de aluminio de 3 mm
BASE_T = 3.0
BASE_TOP = BASE_Z0 + BASE_T
BASE_X = (-105.0, 140.0)
BASE_HALF_W = 74.5

# ---------------------------------------------------------------- Motor de tracción JGB37-520
GEAR_D, GEAR_L = 37.0, 22.0
CAN_D, CAN_L = 33.0, 22.7
BOSS_D, BOSS_L = 12.0, 6.0
SHAFT_D, SHAFT_FLAT, SHAFT_L = 6.0, 5.5, 15.5
SHAFT_OFFSET = 7.0
FACE_PCD = 31.0
GEAR_Z = SPROCKET_Z + SHAFT_OFFSET   # el eje queda 7 mm abajo del centro del reductor

# ---------------------------------------------------------------- Arma
BLADE_R = 6 * 25.4 / 2               # hoja de 6"
BLADE_T = 1.8
BLADE_BORE = 20.0
BLADE_TEETH = 40
DISC_X, DISC_Z = 110.0, 105.0        # centro de la hoja
SHAFT_W_D = 12.0
UPRIGHT_Y = (14.0, 24.0)             # postes del eje (lado izquierdo; el derecho es espejo)
LOCK_ANGLE = math.radians(135)
LOCK_R = 35.0
LOCK_X = DISC_X + LOCK_R * math.cos(LOCK_ANGLE)
LOCK_Z = DISC_Z + LOCK_R * math.sin(LOCK_ANGLE)
PULLEY_PD = 31.83                    # HTD-5M de 20 dientes
BELT_LEN = 310.0                     # banda HTD-5M 310 mm (62 dientes)
BELT_C = (BELT_LEN - math.pi * PULLEY_PD) / 2   # distancia entre centros con poleas iguales
WMOTOR_D, WMOTOR_L = 41.81, 67.0     # 775 de 20 V: Ø medido (41.81) y largo del plano (67; la lata sola mide 60.40)
WMOTOR_BOSS = (17.5, 4.4)
WMOTOR_SHAFT = (5.0, 17.0)           # eje de 5 x 17 mm (plano del motor)
WMOTOR_REAR = (12.0, 4.0, 5.0, 6.0)  # buje trasero Ø12 x 4 y punta de eje Ø5 x 6 (98 mm en total)
WMOTOR_HOLES = 29.0                  # 2 x M4 en la cara
WMOTOR_Z = 38.0
WMOTOR_X = DISC_X - math.sqrt(BELT_C**2 - (DISC_Z - WMOTOR_Z) ** 2)
WMOTOR_Y0 = -25.0                    # cara frontal (lado de la polea)
MOUNT_T = 6.0                        # soporte impreso del motor del arma
PULLEY_Y = (-34.0, -50.0)            # ancho de dientes de las poleas

# ---------------------------------------------------------------- Martillo (monito del CETI)
HAMMER_X, HAMMER_Z = -25.0, 116.0    # eje de giro (a lo ancho del robot)
HAMMER_STRIKE = 105.0                # giro máximo hacia atrás, en grados
H_SHAFT_D = 8.0                      # eje de aluminio de 8 mm
H_SHAFT_Y = (-69.0, 70.0)
H_BEARING_Y = (61.0, 68.0)           # 608-2RS izquierdo (el derecho es espejo)
H_GEAR_Y = 54.0                      # plano medio de los engranes (lado izquierdo)
H_GEAR_W = 8.0
H_GEAR_M = 1.5
H_GEAR_TEETH = (20, 20)              # servo / martillo: 1:1, el martillo gira lo mismo que el servo
H_CENTER = H_GEAR_M * sum(H_GEAR_TEETH) / 2      # 30 mm entre ejes
H_SERVO_ANGLE = math.radians(100)    # el servo va adelante y abajo, fuera del recorrido del martillo
H_SERVO_X = HAMMER_X + H_CENTER * math.sin(H_SERVO_ANGLE)
H_SERVO_Z = HAMMER_Z + H_CENTER * math.cos(H_SERVO_ANGLE)
# Servo MG995 (medidas típicas de servo estándar; medir el real): eje de salida a +Y
MG995_L, MG995_W, MG995_H = 40.7, 19.7, 37.0     # caja: largo (vertical, hacia +Z), ancho (X), alto (Y)
MG995_OUT = 10.0                                  # eje de salida a 10 mm del extremo de abajo
MG995_EARS = (54.0, 2.5, 28.0)                    # largo con orejas, espesor, altura de la oreja desde el fondo
MG995_HOLES = (49.5, 10.0)                        # barrenos de las orejas (Ø4.5)
MG995_SPLINE = (5.8, 4.0)                         # estría de 25 dientes
MG995_HORN = (20.0, 2.0)                          # cuerno redondo (viene con el servo)
H_SERVO_TOP_Y = H_GEAR_Y - H_GEAR_W / 2 - MG995_HORN[1] - MG995_SPLINE[1]   # cara superior del servo
H_BRACKET_ZMIN = 93.0                # los soportes no bajan de aquí (relevador y pila de 9 V abajo)
H_SCREW_DZ = 12.0                    # tornillos de los soportes a la placa lateral: (X, Z ± 12)
FIG_SCALE = 3.0                      # escala del monito respecto al STL de referencia (62 mm de alto)
FIG_FOOT_R = 12.0                    # los pies son dos mazas de Ø24 montadas en el eje
BACK_T = 3.0                         # placa trasera que une las dos mitades y la cabeza

# ---------------------------------------------------------------- Colores
ALU = "#b9bfc7"
STEEL = "#8c9096"
BLACK = "#2a2a2a"
PETG = "#e0761f"
TPU = "#3a3a3a"
PCB_RED = "#b3262a"
PCB_BLACK = "#1e1e1e"


# ================================================================= utilidades
def place(shape, origin, z_dir, x_dir=None):
    """Mueve una pieza modelada con su eje en +Z al punto `origin` con el eje en `z_dir`."""
    z = bd.Vector(*z_dir).normalized()
    x = bd.Vector(*(x_dir or (1, 0, 0)))
    if abs(x.dot(z)) > 0.99:
        x = bd.Vector(0, 1, 0) if abs(z.Y) < 0.99 else bd.Vector(1, 0, 0)
    x = (x - z * x.dot(z)).normalized()
    return shape.moved(bd.Location(bd.Plane(origin=origin, x_dir=x, z_dir=z)))


def finish(shape, label, color):
    shape.label = label
    shape.color = color
    return shape


def mirror_y(shape):
    """Espejo respecto al plano XZ conservando etiqueta y color."""
    m = bd.mirror(shape, bd.Plane.XZ)
    return finish(m, shape.label, shape.color)


def cyl(r, h, z0=0.0):
    return bd.Pos(0, 0, z0) * bd.Cylinder(r, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def tube(ro, ri, h, z0=0.0):
    return cyl(ro, h, z0) - cyl(ri, h + 2, z0 - 1)


def box_min(x0, y0, z0, x1, y1, z1):
    return bd.Pos(x0, y0, z0) * bd.Box(x1 - x0, y1 - y0, z1 - z0, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))


def xz_plane(y):
    """Plano cuyo eje local Y apunta a +Z y cuya normal es -Y: dibujar (x, z) y extruir hacia -Y."""
    return bd.Plane(origin=(0, y, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))


def hull(*sketches):
    return bd.make_hull([e for s in sketches for e in s.edges()])


# ================================================================= tornillería estándar
SHCS = {3: (5.5, 3.0, 2.5), 4: (7.0, 4.0, 3.0), 5: (8.5, 5.0, 4.0), 6: (10.0, 6.0, 5.0)}   # ISO 4762: dk, k, s
CSK = {3: (6.72, 1.86, 2.0), 4: (8.96, 2.48, 2.5)}                                          # ISO 10642: dk, k, s
NUT = {3: (5.5, 2.4, 4.0), 4: (7.0, 3.2, 5.0), 5: (8.0, 4.7, 5.0), 6: (10.0, 5.2, 8.0)}     # s, m (ISO 4032), h (ISO 7040)
WASHER = {3: (7.0, 0.5), 4: (9.0, 0.8), 6: (12.0, 1.6)}                                     # ISO 7089


def socket_cap_screw(d, length):
    """ISO 4762. Cabeza en z 0..k, cuerpo en z -length..0."""
    dk, k, s = SHCS[d]
    head = cyl(dk / 2, k)
    head = bd.fillet(head.edges().group_by(bd.Axis.Z)[-1], 0.08 * dk)
    socket = bd.extrude(bd.Pos(0, 0, k) * bd.RegularPolygon(s / math.sqrt(3), 6), amount=-0.6 * k)
    body = head - socket + cyl(d / 2, length, -length)
    return finish(body, f"tornillo_M{d}x{length:g}_ISO4762", BLACK)


def countersunk_screw(d, length):
    """ISO 10642. La cara de la cabeza queda en z = 0; el largo incluye la cabeza."""
    dk, k, s = CSK[d]
    head = bd.Pos(0, 0, -k) * bd.Cone(d / 2, dk / 2, k, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    socket = bd.extrude(bd.RegularPolygon(s / math.sqrt(3), 6), amount=-0.7 * k)
    body = head - socket + cyl(d / 2, length - k, -length)
    return finish(body, f"tornillo_M{d}x{length:g}_ISO10642", BLACK)


def csk_hole(d, depth):
    """Barreno avellanado a 90° (cara en z = 0, hacia -Z)."""
    dk = CSK[d][0]
    cone = bd.Pos(0, 0, -(dk / 2 - d / 2 - 0.1)) * bd.Cone(d / 2 + 0.2, dk / 2 + 0.1, dk / 2 - d / 2 - 0.1 + 0.1, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return cone + cyl(d / 2 + 0.2, depth + 1, -depth)


def set_screw(d, length):
    body = cyl(d / 2, length, -length) - bd.extrude(bd.RegularPolygon(0.25 * d, 6), amount=-0.4 * length)
    return finish(body, f"prisionero_M{d}x{length:g}_ISO4026", BLACK)


def nut(d, nyloc=True):
    """ISO 7040 (con anillo de nylon) o ISO 4032. Asienta en z = 0 y crece hacia +Z."""
    s, m, h = NUT[d]
    hexa = bd.extrude(bd.RegularPolygon(s / math.sqrt(3), 6), amount=m)
    hexa = hexa & cyl(s / 2 * 1.08, m)  # chaflanes de la tuerca
    if nyloc:
        hexa = hexa + cyl(s * 0.47, h - m, m)
    body = hexa - cyl(d / 2, h + 2, -1)
    return finish(body, f"tuerca_M{d}_{'ISO7040' if nyloc else 'ISO4032'}", STEEL)


def washer(d):
    od, t = WASHER[d]
    return finish(tube(od / 2, d / 2 + 0.2, t), f"rondana_M{d}_ISO7089", STEEL)


def hex_standoff(length, across=5.5, d=3):
    body = bd.extrude(bd.RegularPolygon(across / math.sqrt(3), 6), amount=length) - cyl(d / 2, length + 2, -1)
    return finish(body, f"separador_M{d}x{length:g}", "#c8a24a")


# ================================================================= rodamientos y O-rings
def bearing(d, outer, width, name):
    """Rodamiento rígido de bolas con sellos 2RS (eje en +Z, de z = 0 a z = width)."""
    ring = (outer - d) / 2
    body = tube(outer / 2, d / 2, width)
    seal = tube(outer / 2 - 0.22 * ring, d / 2 + 0.28 * ring, 0.4)
    body = body - seal - bd.Pos(0, 0, width - 0.4) * seal
    return finish(body, f"rodamiento_{name}", "#2e5d9e")


def bearing_606():
    return bearing(6, 17, 6, "606_2RS")


def bearing_6201():
    return bearing(12, 32, 10, "6201_2RS")


def o_ring(r_in, cs, z):
    return finish(bd.Pos(0, 0, z) * bd.Torus(r_in + cs / 2, cs / 2), "oring_35x3_NBR", "#151515")


# ================================================================= trayectoria de la oruga
def belt_segments(circles):
    """Contorno exterior (sentido antihorario en el plano x-z) alrededor de círculos (x, z, r)."""
    n = len(circles)
    tangents = []
    for i in range(n):
        x1, z1, r1 = circles[i]
        x2, z2, r2 = circles[(i + 1) % n]
        dx, dz = x2 - x1, z2 - z1
        dist = math.hypot(dx, dz)
        ux, uz = dx / dist, dz / dist
        sa = (r1 - r2) / dist
        ca = math.sqrt(1 - sa * sa)
        nx, nz = sa * ux + ca * uz, sa * uz - ca * ux
        tangents.append(((x1 + r1 * nx, z1 + r1 * nz), (x2 + r2 * nx, z2 + r2 * nz)))
    segs = []
    for i in range(n):
        segs.append(("line", tangents[i][0], tangents[i][1]))
        j = (i + 1) % n
        cx, cz, r = circles[j]
        a0 = math.atan2(tangents[i][1][1] - cz, tangents[i][1][0] - cx)
        a1 = math.atan2(tangents[j][0][1] - cz, tangents[j][0][0] - cx)
        while a1 < a0:
            a1 += 2 * math.pi
        segs.append(("arc", (cx, cz), r, a0, a1))
    return segs


def seg_len(seg):
    return math.dist(seg[1], seg[2]) if seg[0] == "line" else seg[2] * (seg[4] - seg[3])


def path_point(segs, s):
    total = sum(seg_len(g) for g in segs)
    s %= total
    for g in segs:
        length = seg_len(g)
        if s <= length:
            if g[0] == "line":
                t = s / length
                return (g[1][0] + t * (g[2][0] - g[1][0]), g[1][1] + t * (g[2][1] - g[1][1]))
            a = g[3] + s / g[2]
            return (g[1][0] + g[2] * math.cos(a), g[1][1] + g[2] * math.sin(a))
        s -= length
    raise ValueError(s)


def chain_hinges(segs, n_links):
    """Pernos de una cadena de paso P que sigue la trayectoria; devuelve (pernos, sobrante)."""
    total = sum(seg_len(g) for g in segs)
    s = 0.0
    hinges = [path_point(segs, 0.0)]
    for _ in range(n_links):
        a = path_point(segs, s)
        lo, hi = s + P, s + 1.3 * P
        for _ in range(60):
            mid = (lo + hi) / 2
            if math.dist(path_point(segs, mid), a) < P:
                lo = mid
            else:
                hi = mid
        s = hi
        hinges.append(path_point(segs, s))
    return hinges, s - total


def track_layout():
    """Busca la posición de la rueda delantera que cierra la cadena con N_LINKS eslabones."""

    def circles(x_front):
        return [(SPROCKET_X, SPROCKET_Z, RC_SPROCKET), (x_front, IDLER_Z, RC_IDLER), (TOP_X, TOP_Z, RC_IDLER)]

    lo, hi = FRONT_X_RANGE          # más adelante = cadena más larga
    for _ in range(50):
        mid = (lo + hi) / 2
        _, extra = chain_hinges(belt_segments(circles(mid)), N_LINKS)
        if extra > 0:               # sobra cadena: alejar la rueda
            lo = mid
        else:
            hi = mid
    x_front = (lo + hi) / 2
    hinges, extra = chain_hinges(belt_segments(circles(x_front)), N_LINKS)
    assert abs(extra) < 0.01, extra
    return x_front, hinges


# ================================================================= piezas de la oruga
def track_link_body():
    """Eslabón (sistema local: X a lo largo de la oruga, Z hacia afuera, perno en x = ±P/2)."""
    clear = 0.4
    r_k = LINK_T / 2
    inner = (4.0, 9.0)              # zona de los nudillos del extremo -X (|y|)
    outer = (inner[1] + clear, LINK_W / 2)
    plate_x = P / 2 - r_k - clear
    body = bd.Box(2 * plate_x, LINK_W, LINK_T)
    for sign, (y0, y1) in ((1, outer), (-1, inner)):
        for side in (1, -1):
            yc = side * (y0 + y1) / 2
            tongue = bd.Pos(sign * P / 4, yc, 0) * bd.Box(P / 2, y1 - y0, LINK_T)
            knuckle = bd.Pos(sign * P / 2, yc, 0) * bd.Rot(90, 0, 0) * bd.Cylinder(r_k, y1 - y0)
            body = body + tongue + knuckle
    for sign in (1, -1):
        body = body - bd.Pos(sign * P / 2, 0, 0) * bd.Rot(90, 0, 0) * bd.Cylinder(PIN_D / 2, LINK_W + 2)
    # guía central hacia adentro (-Z), con punta más angosta
    horn = bd.extrude(
        bd.Plane.XZ
        * bd.Polygon(
            (-HORN_L / 2, -LINK_T / 2 + 0.01),
            (HORN_L / 2, -LINK_T / 2 + 0.01),
            (HORN_L / 2 - 1.2, -LINK_T / 2 - HORN_H),
            (-HORN_L / 2 + 1.2, -LINK_T / 2 - HORN_H),
            align=None,
        ),
        amount=HORN_W / 2,
        both=True,
    )
    grouser = bd.Pos(0, 0, LINK_T / 2 + GROUSER_H / 2 - 0.01) * bd.Box(4.0, LINK_W - 2.0, GROUSER_H)
    return body + horn + grouser


def sprocket_body(bore_angle=0.0):
    """Catarina motriz de 12 dientes con 2 ranuras para O-ring (local: Z = eje; z = 0 cara del chasis).

    Los O-rings sobresalen 0.5 mm del rin pero quedan 0.13 mm debajo de los eslabones: si se pierde la
    oruga, son la llanta con la que el robot sigue empujando.
    """
    hub_len = WHEEL_Y0 - (FRAME_IN + BOSS_L) - 0.5               # del buje del motor a la cara de la rueda
    shaft_end = FRAME_IN + BOSS_L + SHAFT_L - WHEEL_Y0           # fin del eje en coordenadas locales
    body = cyl(R_SPROCKET, WHEEL_W) + cyl(10.0, hub_len, -hub_len)
    body = bd.fillet(body.edges().filter_by(bd.GeomType.CIRCLE).filter_by(lambda e: e.radius > R_SPROCKET - 0.1), 1.0)
    for z in ORING_Z:
        body = body - tube(R_SPROCKET + 1, ORING_R_IN, ORING_CS + 0.2, z - (ORING_CS + 0.2) / 2)
    pocket_w, pocket_d, pocket_axial = HORN_L + 2.5, HORN_H + 1.5, HORN_W + 3.0
    for i in range(N_TEETH):
        a = 360.0 * i / N_TEETH
        body = body - bd.Rot(0, 0, a) * bd.Pos(R_SPROCKET - pocket_d / 2 + 0.5, 0, WHEEL_W / 2) * bd.Box(
            pocket_d + 1.0, pocket_w, pocket_axial
        )
    for i in range(6):  # aligeramientos: 1.5 mm de pared hasta el fondo de los huecos de los dientes
        a = math.radians(60 * i + 30)
        body = body - bd.Pos(10.0 * math.cos(a), 10.0 * math.sin(a), 0) * cyl(2.2, WHEEL_W + 1)
    # barreno: redondo junto al buje del motor y en D donde el eje tiene su plano
    flat_start = shaft_end - 12.0 + 0.5
    d_bore = cyl(SHAFT_D / 2 + 0.05, flat_start + hub_len + 1, -hub_len - 1) + bd.extrude(
        bd.Pos(0, 0, flat_start) * (bd.Circle(SHAFT_D / 2 + 0.05) - bd.Pos(SHAFT_FLAT - SHAFT_D / 2 + 3.5, 0) * bd.Rectangle(7, 8)),
        amount=shaft_end - flat_start + 1,
    )
    grub_hole = bd.Pos(0, 0, GRUB_Z) * bd.Rot(0, 90, 0) * cyl(1.5, R_SPROCKET + 1)   # M3, machuelear o inserto
    return body - bd.Rot(0, 0, bore_angle) * (d_bore + grub_hole)


def idler_body():
    """Rueda libre con ranura para la guía y alojamientos para 2 rodamientos 606."""
    body = cyl(R_IDLER, WHEEL_W)
    body = bd.fillet(body.edges().filter_by(bd.GeomType.CIRCLE), 1.0)
    body = body - tube(R_IDLER + 1, R_IDLER - HORN_H - 2.0, HORN_W + 3.0, WHEEL_W / 2 - (HORN_W + 3.0) / 2)
    body = body - cyl(17.0 / 2 + 0.05, 6.05, -0.02) - cyl(17.0 / 2 + 0.05, 6.05, WHEEL_W - 6.03)
    body = body - cyl(4.0, WHEEL_W + 2, -1)
    return body


@model
def eslabon_oruga():
    return finish(track_link_body(), "eslabon_oruga", TPU)


@model
def catarina():
    return finish(sprocket_body(), "catarina", PETG)


@model
def rueda_libre():
    return finish(idler_body(), "rueda_libre", PETG)


# ================================================================= placa lateral
ANGLE_X = (-40.0, 0.0, 52.0)       # ángulos de aluminio que unen placas laterales y base
ANGLE_HOLE_Z = 27.0
ANGLE_LEG = 19.05                  # ángulo de 3/4" x 1/8"
ANGLE_T = 3.175
ANGLE_LEN = 15.0


def gear_screw_points():
    for i in range(6):
        a = math.radians(60 * i)
        yield SPROCKET_X + FACE_PCD / 2 * math.cos(a), GEAR_Z + FACE_PCD / 2 * math.sin(a)


def frame_plate_body(x_front):
    """Placa lateral izquierda de aluminio de 5 mm (y de FRAME_IN a FRAME_OUT)."""
    outline = hull(
        bd.Pos(SPROCKET_X, GEAR_Z) * bd.Circle(22.0),
        bd.Pos(x_front - TENSION_SLOT, IDLER_Z) * bd.Circle(14.0),
        bd.Pos(x_front + TENSION_SLOT, IDLER_Z) * bd.Circle(14.0),
        bd.Pos(TOP_X, TOP_Z) * bd.Circle(14.0),
        bd.Pos(HAMMER_X, HAMMER_Z) * bd.Circle(18.0),
    )
    window = bd.Polygon((-44.0, 37.0), (44.0, 37.0), (0.0, 80.0), align=None)
    window = bd.fillet(window.vertices(), 6.0)
    holes = (
        bd.Pos(SPROCKET_X, SPROCKET_Z) * bd.Circle(BOSS_D / 2 + 0.5)
        + bd.Pos(TOP_X, TOP_Z) * bd.Circle(3.2)
        + bd.Pos(x_front, IDLER_Z) * bd.SlotCenterToCenter(2 * TENSION_SLOT, 6.4)
        + bd.Pos(-40.0, 62.0) * bd.Circle(9.0)
        + bd.Pos(40.0, 62.0) * bd.Circle(9.0)
    )
    for x in ANGLE_X:
        holes += bd.Pos(x, ANGLE_HOLE_Z) * bd.Circle(1.7)
    plate = bd.extrude(xz_plane(FRAME_OUT) * (outline - window - holes), amount=FRAME_T)
    for x, z in list(gear_screw_points()) + hammer_screw_points():   # M3 avellanados desde el lado de la oruga
        plate = plate - place(csk_hole(3, FRAME_T + 1), (x, FRAME_OUT, z), (0, 1, 0))
    return plate


def hammer_screw_points():
    return [(HAMMER_X, HAMMER_Z + H_SCREW_DZ), (HAMMER_X, HAMMER_Z - H_SCREW_DZ)]


def angle_bracket_body():
    """Tramo de ángulo de aluminio 3/4" x 1/8", con un barreno en cada ala."""
    prof = bd.Polygon(
        (0, 0), (ANGLE_LEG, 0), (ANGLE_LEG, ANGLE_T), (ANGLE_T, ANGLE_T), (ANGLE_T, ANGLE_LEG), (0, ANGLE_LEG), align=None
    )
    body = bd.extrude(bd.Plane.YZ * prof, amount=ANGLE_LEN / 2, both=True)
    body = body - bd.Pos(0, 11.0, -1) * cyl(1.7, ANGLE_T + 2)                                        # ala horizontal
    body = body - bd.Pos(0, 0, ANGLE_HOLE_Z - BASE_TOP) * bd.Rot(-90, 0, 0) * cyl(1.7, ANGLE_T + 2, -1)  # ala vertical
    return body


def angle_bracket(x):
    body = angle_bracket_body().moved(bd.Location((x, FRAME_IN, BASE_TOP), (0, 0, 180)))
    return finish(body, "angulo_aluminio_3-4x1-8", ALU)


# ================================================================= motor de tracción (referencia)
def drive_motor_body():
    """JGB37-520 izquierdo: cara del reductor en y = FRAME_IN, cuerpo hacia -Y, eje abajo."""
    yax = (0, -1, 0)
    x = SPROCKET_X
    gear = place(cyl(GEAR_D / 2, GEAR_L), (x, FRAME_IN, GEAR_Z), yax)
    can = place(cyl(CAN_D / 2, CAN_L), (x, FRAME_IN - GEAR_L, GEAR_Z), yax)
    cap = place(cyl(CAN_D / 2 - 1.0, 3.0), (x, FRAME_IN - GEAR_L - CAN_L, GEAR_Z), yax)
    bush = place(cyl(7.5 / 2, 3.25), (x, FRAME_IN - GEAR_L - CAN_L - 3.0, GEAR_Z), yax)
    body = gear + can + cap + bush
    for s in (1, -1):
        body = body + place(bd.Box(3, 0.6, 6.7, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)),
                            (x + s * 12.25, FRAME_IN - GEAR_L - CAN_L, GEAR_Z), yax)
    body = body + place(cyl(BOSS_D / 2, BOSS_L), (x, FRAME_IN, SPROCKET_Z), (0, 1, 0))
    shaft = cyl(SHAFT_D / 2, SHAFT_L) - bd.Pos(SHAFT_FLAT - SHAFT_D / 2 + 2, 0, SHAFT_L - 6.0 + 0.5) * bd.Box(4, 8, 13.0)
    body = body + place(shaft, (x, FRAME_IN + BOSS_L, SPROCKET_Z), (0, 1, 0))
    for hx, hz in gear_screw_points():  # 6 x M3, 4 mm de profundidad, en la cara del reductor
        body = body - place(cyl(1.5, 4.0), (hx, FRAME_IN, hz), (0, -1, 0))
    return body


# ================================================================= un lado de tracción
def wheel_on_bolt(parts, x, z):
    """Rueda libre: tornillo M6 x 50 desde adentro, separador, 2 rodamientos 606, rondana y tuerca."""
    parts.append(finish(place(idler_body(), (x, WHEEL_Y0, z), (0, 1, 0)), "rueda_libre", PETG))
    parts.append(place(bearing_606(), (x, WHEEL_Y0, z), (0, 1, 0)))
    parts.append(place(bearing_606(), (x, WHEEL_Y0 + WHEEL_W - 6.0, z), (0, 1, 0)))
    parts.append(finish(place(tube(5.0, 3.1, WHEEL_Y0 - FRAME_OUT), (x, FRAME_OUT, z), (0, 1, 0)), "separador_M6", STEEL))
    parts.append(place(washer(6), (x, WHEEL_Y0 + WHEEL_W, z), (0, 1, 0)))
    parts.append(place(nut(6), (x, WHEEL_Y0 + WHEEL_W + WASHER[6][1], z), (0, 1, 0)))
    parts.append(place(socket_cap_screw(6, 50), (x, FRAME_IN, z), (0, -1, 0)))


def drive_side_left():
    x_front, hinges = track_layout()
    parts = [finish(frame_plate_body(x_front), "placa_lateral", ALU), finish(drive_motor_body(), "motor_jgb37_520", "#9aa0a6")]
    for x, z in gear_screw_points():
        parts.append(place(countersunk_screw(3, 8), (x, FRAME_OUT, z), (0, 1, 0)))
    for x, z in hammer_screw_points():   # soporte del martillo (rosca en inserto de latón)
        parts.append(place(countersunk_screw(3, 10), (x, FRAME_OUT, z), (0, 1, 0)))

    # catarina orientada para que sus huecos coincidan con las guías de la oruga
    centers = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(hinges[:-1], hinges[1:])]
    mid_r = math.sqrt(RC_SPROCKET**2 - (P / 2) ** 2)
    near = min(centers, key=lambda c: abs(math.dist(c, (SPROCKET_X, SPROCKET_Z)) - mid_r))
    phi = math.degrees(math.atan2(near[1] - SPROCKET_Z, near[0] - SPROCKET_X))
    spr_loc = bd.Location(bd.Plane(origin=(SPROCKET_X, WHEEL_Y0, SPROCKET_Z), x_dir=(1, 0, 0), z_dir=(0, 1, 0)))
    rot = bd.Rot(0, 0, -phi)            # Y local = -Z del robot; el barreno en D compensa el giro
    parts.append(finish(sprocket_body(bore_angle=phi).moved(spr_loc * rot), "catarina", PETG))
    grub = set_screw(3, 6).moved(bd.Location((SHAFT_FLAT - SHAFT_D / 2 + 6.0, 0, GRUB_Z), (0, 90, 0)))
    parts.append(finish(grub.moved(spr_loc), "prisionero_M3x6_ISO4026", BLACK))
    for z in ORING_Z:
        o = o_ring(ORING_R_IN, ORING_CS, z)
        parts.append(finish(o.moved(spr_loc), o.label, o.color))

    wheel_on_bolt(parts, x_front, IDLER_Z)
    wheel_on_bolt(parts, TOP_X, TOP_Z)

    link = track_link_body()
    for a, b in zip(hinges[:-1], hinges[1:]):
        tx, tz = (b[0] - a[0]) / P, (b[1] - a[1]) / P
        c = ((a[0] + b[0]) / 2, TRACK_Y, (a[1] + b[1]) / 2)
        loc = bd.Location(bd.Plane(origin=c, x_dir=(tx, 0, tz), z_dir=(tz, 0, -tx)))
        parts.append(finish(link.moved(loc), "eslabon_oruga", TPU))

    for x in ANGLE_X:
        parts.append(angle_bracket(x))
        parts.append(place(socket_cap_screw(3, 16), (x, FRAME_IN - ANGLE_T, ANGLE_HOLE_Z), (0, -1, 0)))
        parts.append(place(nut(3), (x, FRAME_OUT, ANGLE_HOLE_Z), (0, 1, 0)))
        parts.append(place(countersunk_screw(3, 12), (x, FRAME_IN - 11.0, BASE_Z0), (0, 0, -1)))
        parts.append(place(nut(3), (x, FRAME_IN - 11.0, BASE_TOP + ANGLE_T), (0, 0, 1)))
    return parts, x_front


# ================================================================= posiciones del interior
STANDOFF_XY = [(-56.0, 64.0), (-56.0, -64.0), (26.0, 64.0), (26.0, -64.0)]
DECK_Z = 60.0
DECK_T = 3.0
DECK_X = (-60.0, 30.0)
UPRIGHT_HOLES_X = (DISC_X - 15.0, DISC_X + 15.0)
L298_C = (85.5, 47.0)
L298_HOLE = 37.0                   # separación supuesta de los barrenos del módulo (medir)
SADDLE = (12.0, 46.0, 25.0, 35.0)  # cuna del motor del arma: x0, x1, y0, y1
MOUNT_X = (8.0, 52.0)              # soporte frontal del motor del arma
MOUNT_FOOT_HOLES = [(14.0, WMOTOR_Y0 - MOUNT_T - 5.0), (46.0, WMOTOR_Y0 - MOUNT_T - 5.0)]
REAR_X = BASE_X[0]
SWITCH_Y = 13.0
SWITCH_Z = 47.0
REAR_FOOT_HOLES = [(REAR_X + 10.5, 10.0), (REAR_X + 10.5, -10.0)]
FREENOVE_X = (-58.0, 28.0)
FREENOVE_W = 88.0
FREENOVE_HOLES = [(FREENOVE_X[0] + 4, 30.0), (FREENOVE_X[0] + 4, -30.0), (FREENOVE_X[1] - 4, 30.0), (FREENOVE_X[1] - 4, -30.0)]  # supuestos
FREENOVE_Z = DECK_Z + DECK_T + 6.0
RELAY_C = (-20.0, 59.0)
RELAY_HOLES_X = (RELAY_C[0] - 17.5, RELAY_C[0] + 17.5)
CELL_D, CELL_L = 18.6, 65.2            # celda 18650 (con forro)
BAT_3S = (-61.0, 7.0, 3 * CELL_D + 2.0, CELL_D + 2.0)   # 3S1P acostada: x0, x1, ancho (y), alto; abajo
BAT_5S = (-61.0, 7.0, 5 * CELL_D + 2.0, CELL_D + 2.0)   # 5S1P, arriba de la 3S
PILA_9V = (48.5, 17.5, 26.5)          # 6LR61 de canto: largo (x), ancho (y), alto (z)
PILA_X0, PILA_Y0 = -50.0, -71.0       # sobre la cubierta, lado derecho
PILA_SCREWS_X = (PILA_X0 + 8.0, PILA_X0 + PILA_9V[0] - 8.0)


def l298_holes():
    for dx in (-L298_HOLE / 2, L298_HOLE / 2):
        for dy in (-L298_HOLE / 2, L298_HOLE / 2):
            yield L298_C[0] + dx, L298_C[1] + dy


def base_csk_holes():
    """Barrenos con tornillo avellanado desde abajo: (x, y, métrica)."""
    pts = []
    for x in ANGLE_X:
        for s in (1, -1):
            pts.append((x, s * (FRAME_IN - 11.0), 3))
    pts += [(x, y, 3) for x, y in STANDOFF_XY]
    pts += [(x, y, 3) for x, y in REAR_FOOT_HOLES]
    pts += [(x, y, 3) for x, y in l298_holes()]
    pts += [(x, s * sum(UPRIGHT_Y) / 2, 4) for x in UPRIGHT_HOLES_X for s in (1, -1)]
    pts += [(SADDLE[0] + 5, (SADDLE[2] + SADDLE[3]) / 2, 3), (SADDLE[1] - 5, (SADDLE[2] + SADDLE[3]) / 2, 3)]
    pts += [(x, y, 3) for x, y in MOUNT_FOOT_HOLES]
    return pts


# ================================================================= placa base, pared trasera y cubierta
def base_plate_body():
    x0, x1 = BASE_X
    face = bd.Pos((x0 + x1) / 2, 0) * bd.Rectangle(x1 - x0, 2 * BASE_HALF_W)
    face = bd.fillet(face.vertices(), 6.0)
    for x, y in [(-80, 0), (-45, 0), (-20, 0), (-45, 26), (-45, -26), (-20, 26), (-20, -26), (68, 0), (78, -48), (106, -50)]:
        face = face - bd.Pos(x, y) * bd.Circle(10.0)
    for s in (1, -1):
        for x in (-40.0, -10.0):  # ranuras para cinchos de las baterías
            face = face - bd.Pos(x, s * 53.0) * bd.SlotCenterToCenter(16.0, 4.0)
    plate = bd.Pos(0, 0, BASE_Z0) * bd.extrude(face, amount=BASE_T)
    for x, y, d in base_csk_holes():
        plate = plate - place(csk_hole(d, BASE_T + 1), (x, y, BASE_Z0), (0, 0, -1))
    return plate


def rear_wall_body():
    """Pared trasera impresa con los dos interruptores y su pie (entre los motores) para atornillarla."""
    wall = box_min(REAR_X, -BASE_HALF_W + 0.5, BASE_TOP, REAR_X + 4.0, BASE_HALF_W - 0.5, BASE_TOP + 55.0)
    foot = box_min(REAR_X + 4.0, -20.0, BASE_TOP, REAR_X + 15.0, 20.0, BASE_TOP + 4.0)
    body = wall + foot
    for s in (1, -1):
        body = body - place(cyl(8.1, 10, -5), (REAR_X, s * SWITCH_Y, SWITCH_Z), (1, 0, 0))
    for x, y in REAR_FOOT_HOLES:
        body = body - bd.Pos(x, y, BASE_TOP - 1) * cyl(1.7, 6)
    return body


def deck_body():
    x0, x1 = DECK_X
    face = bd.Pos((x0 + x1) / 2, 0) * bd.Rectangle(x1 - x0, 146.0)
    face = bd.fillet(face.vertices(), 5.0)
    for x, y in STANDOFF_XY + FREENOVE_HOLES:
        face = face - bd.Pos(x, y) * bd.Circle(1.7)
    for x in RELAY_HOLES_X:
        face = face - bd.Pos(x, RELAY_C[1]) * bd.Circle(1.7)
    face = face - bd.Pos(-15.0, 0) * bd.SlotCenterToCenter(40.0, 12.0)   # paso de cables
    yb = sum(PULLEY_Y) / 2
    notch = bd.Pos(22.0, yb) * bd.Rectangle(24.0, 20.0)                   # paso de la banda del arma
    face = face - bd.fillet(notch.vertices(), 2.0)
    deck = bd.Pos(0, 0, DECK_Z) * bd.extrude(face, amount=DECK_T)
    csk_pts = FREENOVE_HOLES + [(x, PILA_Y0 + PILA_9V[1] / 2) for x in PILA_SCREWS_X]
    for x, y in csk_pts:   # tornillos avellanados por abajo (el motor del arma y la batería pasan debajo)
        deck = deck - place(csk_hole(3, DECK_T + 1), (x, y, DECK_Z), (0, 0, -1))
    return deck


# ================================================================= electrónica y baterías (volúmenes de referencia)
def battery_pack(spec, z0, label, color):
    """Paquete de celdas 18650 acostadas (eje en X) y lado a lado, con forro termoencogible."""
    x0, x1, w, h = spec
    body = box_min(x0, -w / 2, z0, x1, w / 2, z0 + h)
    body = bd.fillet(body.edges().filter_by(bd.Axis.X), h / 2 - 0.5)
    body = bd.fillet(body.edges().filter_by(bd.Axis.X, reverse=True), 1.5)
    return finish(body, label, color)


def pila_9v_parts():
    """Pila cuadrada de 9 V (alimenta Freenove + ESP32) en un porta pila impreso sobre la cubierta."""
    lx, ly, lz = PILA_9V
    z0 = DECK_Z + DECK_T
    wall, base = 2.0, 4.0
    holder = box_min(PILA_X0 - wall, PILA_Y0 - wall, z0, PILA_X0 + lx + wall, PILA_Y0 + ly + wall, z0 + base + 15.0)
    holder = holder - box_min(PILA_X0 - 0.2, PILA_Y0 - 0.2, z0 + base, PILA_X0 + lx + 0.2, PILA_Y0 + ly + 0.2, z0 + base + 16.0)
    holder = holder - box_min(PILA_X0 + 12, PILA_Y0 - wall - 1, z0 + base + 4.0, PILA_X0 + lx - 12, PILA_Y0 + ly + wall + 1, z0 + base + 10.0)  # paso de cincho
    for x in PILA_SCREWS_X:
        holder = holder - bd.Pos(x, PILA_Y0 + ly / 2, z0 - 1) * cyl(1.5, base)
    cell = box_min(PILA_X0, PILA_Y0, z0 + base, PILA_X0 + lx, PILA_Y0 + ly, z0 + base + lz)
    cell = bd.fillet(cell.edges().filter_by(bd.Axis.X, reverse=True).filter_by(bd.Axis.Y, reverse=True), 1.5)
    terminals = place(cyl(3.0, 3.0), (PILA_X0 + lx - 1.0, PILA_Y0 + ly / 2 - 6.35, z0 + base + lz - 1.0), (0, 0, 1))         + place(bd.extrude(bd.RegularPolygon(4.0, 6), amount=3.0), (PILA_X0 + lx - 1.0, PILA_Y0 + ly / 2 + 6.35, z0 + base + lz - 1.0), (0, 0, 1))
    parts = [finish(holder, "porta_pila_9V", PETG), finish(cell + terminals, "pila_9V_6LR61", "#2b4f9e")]
    for x in PILA_SCREWS_X:
        parts.append(place(countersunk_screw(3, 6), (x, PILA_Y0 + ly / 2, DECK_Z), (0, 0, -1)))
    return parts


def freenove_board():
    x0, x1 = FREENOVE_X
    z = FREENOVE_Z
    xc = (x0 + x1) / 2 + 4
    pcb = box_min(x0, -FREENOVE_W / 2, z, x1, FREENOVE_W / 2, z + 1.6)
    for x, y in FREENOVE_HOLES:
        pcb = pcb - bd.Pos(x, y, z - 1) * cyl(1.6, 4)
    parts = [finish(pcb, "freenove_breakout_pcb", PCB_BLACK)]
    yk = FREENOVE_W / 2 - 5.5
    clamps = box_min(xc - 31, yk - 4.5, z + 1.6, xc + 31, yk + 4.5, z + 11.6) + box_min(xc - 31, -yk - 4.5, z + 1.6, xc + 31, -yk + 4.5, z + 11.6)
    parts.append(finish(clamps, "freenove_clemas", "#3fae49"))
    sockets = box_min(xc - 30.5, 11.4, z + 1.6, xc + 30.5, 14.0, z + 10.1) + box_min(xc - 30.5, -14.0, z + 1.6, xc + 30.5, -11.4, z + 10.1)
    parts.append(finish(sockets, "freenove_sockets", BLACK))
    parts.append(finish(box_min(x0 + 1, 16.0, z + 1.6, x0 + 15, 25.0, z + 12.6), "freenove_jack_dc", BLACK))
    zb = z + 1.6 + 8.5 + 2.5   # ESP32-S3 WROOM (Freenove) enchufado en los sockets
    esp = box_min(xc - 31.5, -14, zb, xc + 31.5, 14, zb + 1.6)
    module = box_min(xc + 5.25, -9, zb + 1.6, xc + 30.75, 9, zb + 4.7)
    usb = box_min(xc - 32.75, -4.5, zb + 1.6, xc - 25.25, 4.5, zb + 4.8)
    parts.append(finish(esp + module + usb, "esp32_s3_wroom", "#20232a"))
    return parts


def l298n_module():
    z = BASE_TOP + 6.0
    cx, cy = L298_C
    pcb = box_min(cx - 21.5, cy - 21.5, z, cx + 21.5, cy + 21.5, z + 1.6)
    for x, y in l298_holes():
        pcb = pcb - bd.Pos(x, y, z - 1) * cyl(1.6, 4)
    sink = box_min(cx - 11.5, cy + 2, z + 1.6, cx + 11.5, cy + 18, z + 26.6)
    for i in range(5):
        sink = sink - box_min(cx - 10.2 + i * 4.6, cy + 1, z + 8.0, cx - 8.2 + i * 4.6, cy + 19, z + 28.0)
    terminals = (
        box_min(cx - 21, cy - 5, z + 1.6, cx - 13, cy + 5, z + 11.6)
        + box_min(cx + 13, cy - 5, z + 1.6, cx + 21, cy + 5, z + 11.6)
        + box_min(cx - 7.5, cy - 21, z + 1.6, cx + 7.5, cy - 13, z + 11.6)
    )
    caps = bd.Pos(cx - 8, cy - 6, z + 1.6) * cyl(4.0, 12.0) + bd.Pos(cx + 8, cy - 6, z + 1.6) * cyl(4.0, 12.0)
    return [
        finish(pcb, "l298n_pcb", PCB_RED),
        finish(sink, "l298n_disipador", BLACK),
        finish(terminals, "l298n_clemas", "#2f6fd0"),
        finish(caps, "l298n_capacitores", "#333a44"),
    ]


def relay_automotive():
    cx, cy = RELAY_C
    z = DECK_Z + DECK_T
    base = box_min(cx - 20, cy - 13, z, cx + 20, cy + 13, z + 4.0)
    for x in RELAY_HOLES_X:
        base = base - bd.Pos(x, cy, z - 1) * cyl(1.7, 6)
    body = box_min(cx - 13, cy - 13, z + 4.0, cx + 13, cy + 13, z + 29.0)
    body = bd.fillet(body.edges().filter_by(bd.Axis.Z), 2.0)
    return [finish(base, "relevador_base", BLACK), finish(body, "relevador_automotriz_12V_40A", "#222222")]


def switch(y, label):
    bezel = place(cyl(11.0, 2.0), (REAR_X, y, SWITCH_Z), (-1, 0, 0))
    body = place(cyl(8.0, 30.0), (REAR_X, y, SWITCH_Z), (1, 0, 0))
    knob = place(bd.Box(14.0, 4.0, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)), (REAR_X - 2.0, y, SWITCH_Z), (-1, 0, 0))
    return finish(bezel + body + knob, label, "#c0392b" if "arma" in label else "#d4a017")


# ================================================================= arma
def blade_body():
    """Hoja de sierra de 6" con 40 dientes, barreno de 20 mm y 2 barrenos de 7 mm para el seguro."""
    pts = []
    pitch = 2 * math.pi / BLADE_TEETH
    for i in range(BLADE_TEETH):
        a = i * pitch
        pts.append((DISC_X + BLADE_R * math.cos(a), DISC_Z + BLADE_R * math.sin(a)))
        for f, r in ((0.15, BLADE_R - 1.0), (0.55, BLADE_R - 4.5), (0.8, BLADE_R - 5.0)):
            pts.append((DISC_X + r * math.cos(a + f * pitch), DISC_Z + r * math.sin(a + f * pitch)))
    face = bd.Polygon(*pts, align=None)
    face = face - bd.Pos(DISC_X, DISC_Z) * bd.Circle(BLADE_BORE / 2)
    for a in (LOCK_ANGLE, LOCK_ANGLE + math.pi):
        face = face - bd.Pos(DISC_X + LOCK_R * math.cos(a), DISC_Z + LOCK_R * math.sin(a)) * bd.Circle(3.5)
    for k in range(4):   # ranuras de expansión típicas de las hojas
        a = math.radians(45 + 90 * k)
        face = face - bd.Pos(DISC_X + 58 * math.cos(a), DISC_Z + 58 * math.sin(a)) * bd.Rot(0, 0, math.degrees(a)) * bd.Rectangle(12.0, 1.2)
    return bd.extrude(xz_plane(BLADE_T / 2) * face, amount=BLADE_T)


def upright_body():
    """Poste izquierdo del eje del arma (aluminio de 10 mm) con alojamiento para 6201."""
    y0, y1 = UPRIGHT_Y
    outline = hull(
        bd.Pos(DISC_X, BASE_TOP + 4) * bd.Rectangle(48.0, 8.0),
        bd.Pos(DISC_X, DISC_Z) * bd.Circle(22.0),
        bd.Pos(LOCK_X, LOCK_Z) * bd.Circle(7.0),
    )
    window = bd.Pos(DISC_X, BASE_TOP + 12.0 + 24.0) * bd.Rectangle(22.0, 48.0)
    window = bd.fillet(window.vertices(), 5.0)
    face = outline - window - bd.Pos(LOCK_X, LOCK_Z) * bd.Circle(3.2) - bd.Pos(DISC_X, DISC_Z) * bd.Circle(11.0)
    body = bd.extrude(xz_plane(y1) * face, amount=y1 - y0)
    body = body - place(cyl(16.0 + 0.01, 9.05), (DISC_X, y0 - 0.02, DISC_Z), (0, 1, 0))
    for x in UPRIGHT_HOLES_X:   # M4 machueleado desde abajo
        body = body - bd.Pos(x, (y0 + y1) / 2, BASE_TOP - 1) * cyl(2.0, 11.0)
    return body


def pulley_body(bore):
    """Polea HTD-5M de 20 dientes con pestañas y maza (local: Z = eje, z = 0 cara interior)."""
    od = PULLEY_PD - 1.14
    width = abs(PULLEY_Y[1] - PULLEY_Y[0])
    body = cyl(od / 2, width)
    for i in range(20):
        body = body - bd.Rot(0, 0, 18 * i) * bd.Pos(od / 2, 0, -1) * cyl(1.5, width + 2)
    body = body + cyl(18.0, 1.0, -1.0) + cyl(18.0, 1.0, width) + cyl(10.0, 8.0, width + 1.0)
    return body - cyl(bore / 2, width + 12, -2)


def weapon_motor_body():
    """Motor 775 de 20 V de la desbrozadora: cara frontal en y = WMOTOR_Y0, cuerpo hacia +Y."""
    yax = (0, 1, 0)
    o = (WMOTOR_X, WMOTOR_Y0, WMOTOR_Z)
    can = place(cyl(WMOTOR_D / 2, WMOTOR_L), o, yax)
    can = bd.fillet(can.edges().filter_by(bd.GeomType.CIRCLE), 2.0)
    for s in (1, -1):
        can = can - place(cyl(2.0, 6.0), (WMOTOR_X + s * WMOTOR_HOLES / 2, WMOTOR_Y0, WMOTOR_Z), yax)
    boss = place(cyl(WMOTOR_BOSS[0] / 2, WMOTOR_BOSS[1]), o, (0, -1, 0))
    shaft = place(cyl(WMOTOR_SHAFT[0] / 2, WMOTOR_SHAFT[1]), (WMOTOR_X, WMOTOR_Y0 - WMOTOR_BOSS[1], WMOTOR_Z), (0, -1, 0))
    rear = place(cyl(WMOTOR_REAR[0] / 2, WMOTOR_REAR[1]), (WMOTOR_X, WMOTOR_Y0 + WMOTOR_L, WMOTOR_Z), yax)
    rear = rear + place(cyl(WMOTOR_REAR[2] / 2, WMOTOR_REAR[3]), (WMOTOR_X, WMOTOR_Y0 + WMOTOR_L + WMOTOR_REAR[1], WMOTOR_Z), yax)
    body = can + boss + shaft + rear
    for s in (1, -1):
        body = body + place(bd.Box(6.0, 1.0, 4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)),
                            (WMOTOR_X + s * 12.0, WMOTOR_Y0 + WMOTOR_L, WMOTOR_Z), yax)
    return body


def weapon_mount_body():
    """Soporte frontal impreso del motor del arma (PETG 6 mm) con pie hacia la polea."""
    x0, x1 = MOUNT_X
    y1 = WMOTOR_Y0
    y0 = y1 - MOUNT_T
    plate = box_min(x0, y0, BASE_TOP, x1, y1, WMOTOR_Z + 20.0)
    plate = bd.fillet(plate.edges().filter_by(bd.Axis.Y).group_by(bd.Axis.Z)[-1], 6.0)
    foot = box_min(x0, y0 - 10.0, BASE_TOP, x1, y0, BASE_TOP + 4.0)
    body = plate + foot
    body = body - place(cyl(WMOTOR_BOSS[0] / 2 + 0.25, MOUNT_T + 2, -1), (WMOTOR_X, y0, WMOTOR_Z), (0, 1, 0))   # 1 mm de pared a los avellanados
    for s in (1, -1):
        body = body - place(csk_hole(4, MOUNT_T + 1), (WMOTOR_X + s * WMOTOR_HOLES / 2, y0, WMOTOR_Z), (0, -1, 0))
    for x, y in MOUNT_FOOT_HOLES:
        body = body - bd.Pos(x, y, BASE_TOP - 1) * cyl(1.7, 6)
    return body


def saddle_body():
    x0, x1, y0, y1 = SADDLE
    blk = box_min(x0, y0, BASE_TOP, x1, y1, WMOTOR_Z)
    blk = blk - place(cyl(WMOTOR_D / 2 + 0.2, y1 - y0 + 2, -1), (WMOTOR_X, y0, WMOTOR_Z), (0, 1, 0))
    for x in (x0 + 5, x1 - 5):
        blk = blk - bd.Pos(x, (y0 + y1) / 2, BASE_TOP - 1) * cyl(1.5, 6.5)
    blk = blk - box_min(x0 - 1, (y0 + y1) / 2 - 2.5, BASE_TOP + 2.0, x1 + 1, (y0 + y1) / 2 + 2.5, BASE_TOP + 3.5)  # paso de cincho
    return blk


def belt_body():
    r_in, r_out = PULLEY_PD / 2 - 0.35, PULLEY_PD / 2 + 2.9
    c1, c2 = (WMOTOR_X, WMOTOR_Z), (DISC_X, DISC_Z)
    band = hull(bd.Pos(*c1) * bd.Circle(r_out), bd.Pos(*c2) * bd.Circle(r_out)) - hull(
        bd.Pos(*c1) * bd.Circle(r_in), bd.Pos(*c2) * bd.Circle(r_in)
    )
    w = 15.0
    yc = sum(PULLEY_Y) / 2
    return bd.extrude(xz_plane(yc + w / 2) * band, amount=w)


def weapon_parts():
    parts = [finish(blade_body(), "hoja_sierra_6in_40T", "#c9ced4")]
    parts.append(finish(place(tube(BLADE_BORE / 2, SHAFT_W_D / 2, BLADE_T), (DISC_X, -BLADE_T / 2, DISC_Z), (0, 1, 0)), "buje_20a12mm", STEEL))
    shaft_y0 = PULLEY_Y[1] - 10.0
    parts.append(finish(place(cyl(SHAFT_W_D / 2, UPRIGHT_Y[1] + 2.0 - shaft_y0), (DISC_X, shaft_y0, DISC_Z), (0, 1, 0)), "eje_arma_12mm", STEEL))
    # bridas de aluminio (Ø36 x 4 + maza Ø20 hasta el rodamiento) que aprietan la hoja; prisionero M5 en la maza
    flange_len = UPRIGHT_Y[0] - 1.0 - BLADE_T / 2 - 0.1
    flange = cyl(18.0, 4.0) + cyl(10.0, flange_len) - cyl(SHAFT_W_D / 2, flange_len + 2, -1)
    flange = bd.fillet(flange.edges().filter_by(bd.GeomType.CIRCLE).filter_by(lambda e: abs(e.radius - 18.0) < 0.01).group_by(bd.Axis.Z)[-1], 1.0)
    parts.append(finish(place(flange, (DISC_X, BLADE_T / 2, DISC_Z), (0, 1, 0)), "brida_hoja_aluminio", ALU))
    parts.append(finish(place(flange, (DISC_X, -BLADE_T / 2, DISC_Z), (0, -1, 0)), "brida_hoja_aluminio", ALU))
    for side in (1, -1):
        up = finish(upright_body(), "poste_eje_arma", ALU)
        brg = place(bearing_6201(), (DISC_X, UPRIGHT_Y[0] - 1.0, DISC_Z), (0, 1, 0))
        screws = [place(countersunk_screw(4, 12), (x, sum(UPRIGHT_Y) / 2, BASE_Z0), (0, 0, -1)) for x in UPRIGHT_HOLES_X]
        group = [up, brg] + screws
        parts += group if side > 0 else [mirror_y(g) for g in group]
    for x, z, bore in ((DISC_X, DISC_Z, SHAFT_W_D), (WMOTOR_X, WMOTOR_Z, WMOTOR_SHAFT[0])):
        parts.append(finish(place(pulley_body(bore), (x, PULLEY_Y[0], z), (0, -1, 0)), "polea_HTD5M_20T", ALU))
    parts.append(finish(belt_body(), "banda_HTD5M_310_15mm", BLACK))
    parts.append(finish(weapon_motor_body(), "motor_arma_desbrozadora", "#5b6b3a"))
    parts.append(finish(weapon_mount_body(), "soporte_motor_arma", PETG))
    for s in (1, -1):
        parts.append(place(countersunk_screw(4, 10), (WMOTOR_X + s * WMOTOR_HOLES / 2, WMOTOR_Y0 - MOUNT_T, WMOTOR_Z), (0, -1, 0)))
    for x, y in MOUNT_FOOT_HOLES:
        parts.append(place(countersunk_screw(3, 10), (x, y, BASE_Z0), (0, 0, -1)))
        parts.append(place(nut(3), (x, y, BASE_TOP + 4.0), (0, 0, 1)))
    parts.append(finish(saddle_body(), "cuna_motor_arma", PETG))
    for x in (SADDLE[0] + 5, SADDLE[1] - 5):
        parts.append(place(countersunk_screw(3, 6), (x, (SADDLE[2] + SADDLE[3]) / 2, BASE_Z0), (0, 0, -1)))
    # seguro mecánico: perno de 6 mm que atraviesa postes y hoja
    pin = place(cyl(3.0, 62.0), (LOCK_X, -31.0, LOCK_Z), (0, 1, 0))
    ring = place(bd.Torus(8.0, 1.5), (LOCK_X, 31.0 + 8.0, LOCK_Z), (1, 0, 0))
    parts.append(finish(pin + ring, "perno_seguro_arma", "#d62828"))
    return parts


# ================================================================= martillo: monito del CETI
def hammer_loc(theta_deg):
    """Giro del martillo alrededor de su eje (a lo ancho); positivo = hacia atrás (lado contrario a la sierra)."""
    return bd.Location((HAMMER_X, 0, HAMMER_Z)) * bd.Location((0, 0, 0), (0, -theta_deg, 0))


def figure_body():
    """Monito del logotipo del CETI parado sobre el eje del martillo (proporciones del STL, escala FIG_SCALE).

    Sistema local: origen en el eje, Z hacia la cabeza (en reposo), Y a lo ancho (brazos), X hacia el frente
    (la cara del logotipo mira al frente; la espalda es la que golpea). Los pies son dos mazas redondas que
    abrazan el eje de 8 mm, cada una con un prisionero M4.
    """
    s = FIG_SCALE

    def zl(v):                      # z del STL (pies en -3.84) -> z local (pies en -FIG_FOOT_R)
        return s * (v + 3.84) - FIG_FOOT_R

    half = bd.Polygon(
        *[(s * u, zl(v)) for u, v in (
            (1.99, -3.84), (10.0, -3.84), (10.0, 30.03), (27.71, 30.03), (27.71, 37.81),
            (3.49, 37.81), (1.99, 36.31))],
        align=None,
    )
    halves = half + bd.mirror(half, bd.Plane.YZ)
    t = s * 4.65                                  # grueso del cuerpo
    body = bd.extrude(bd.Plane.YZ * halves, amount=t / 2, both=True)
    head_z = zl(49.545)
    head = bd.Pos(-s * 0.13, 0, head_z) * bd.Sphere(s * 8.3)
    back = box_min(-t / 2 - BACK_T, -s * 1.99 - 6.0, -FIG_FOOT_R, -t / 2 + 0.01, s * 1.99 + 6.0, head_z)
    leg_y = (s * 1.99, s * 10.0)
    feet = None
    for side in (1, -1):
        foot = place(cyl(FIG_FOOT_R, leg_y[1] - leg_y[0]), (0, side * leg_y[0], 0), (0, side, 0))
        feet = foot if feet is None else feet + foot
    fig = body + head + back + feet
    fig = fig - place(cyl(H_SHAFT_D / 2 + 0.05, 2 * leg_y[1] + 2, -leg_y[1] - 1), (0, 0, 0), (0, 1, 0))
    for side in (1, -1):            # prisionero M4 en cada pie, hacia el plano del eje
        fig = fig - bd.Pos(0, side * sum(leg_y) / 2, -FIG_FOOT_R - 1) * cyl(2.0, FIG_FOOT_R - 2)
    return fig


def spur_gear(teeth, bore, hub=True):
    """Engrane recto de involuta (bd_warehouse, 20°), centrado en z = 0; con maza hacia +Z o prisionero en el cuerpo."""
    from bd_warehouse.gear import SpurGear

    g = SpurGear(module=H_GEAR_M, tooth_count=teeth, pressure_angle=20, root_fillet=0.3, thickness=H_GEAR_W)
    z_grub = 0.0
    if hub:
        g = g + bd.Pos(0, 0, H_GEAR_W / 2) * cyl(bore / 2 + 4.0, 5.0)
        z_grub = H_GEAR_W / 2 + 2.5
    g = g - cyl(bore / 2 + 0.05, H_GEAR_W + 12, -H_GEAR_W)
    return g - bd.Pos(0, 0, z_grub) * bd.Rot(0, 90, 0) * cyl(1.5, bore / 2 + 5)


def servo_gear():
    """Engrane de 20 dientes que se atornilla al cuerno redondo del servo (4 x M2)."""
    g = spur_gear(H_GEAR_TEETH[0], 6.0, hub=False)
    for i in range(4):
        a = math.radians(45 + 90 * i)
        g = g - bd.Pos(7.0 * math.cos(a), 7.0 * math.sin(a), -H_GEAR_W) * cyl(1.1, 2 * H_GEAR_W)
    return g


def mg995_body():
    """Servo MG995 en coordenadas del robot: eje de salida en (H_SERVO_X, *, H_SERVO_Z) apuntando a +Y."""
    x0, x1 = H_SERVO_X - MG995_W / 2, H_SERVO_X + MG995_W / 2
    z0, z1 = H_SERVO_Z - MG995_OUT, H_SERVO_Z - MG995_OUT + MG995_L
    y1 = H_SERVO_TOP_Y
    y0 = y1 - MG995_H
    case = box_min(x0, y0, z0, x1, y1, z1)
    case = bd.fillet(case.edges().filter_by(bd.Axis.Y), 1.0)
    zc = (z0 + z1) / 2
    ear_y1 = y0 + MG995_EARS[2]
    ears = box_min(x0, ear_y1 - MG995_EARS[1], zc - MG995_EARS[0] / 2, x1, ear_y1, zc + MG995_EARS[0] / 2)
    for dz in (-MG995_HOLES[0] / 2, MG995_HOLES[0] / 2):
        for dx in (-MG995_HOLES[1] / 2, MG995_HOLES[1] / 2):
            ears = ears - place(cyl(2.25, 10, -5), (H_SERVO_X + dx, ear_y1, zc + dz), (0, 1, 0))
    top = place(cyl(6.0, 1.5), (H_SERVO_X, y1, H_SERVO_Z), (0, 1, 0))
    spline = place(cyl(MG995_SPLINE[0] / 2, MG995_SPLINE[1]), (H_SERVO_X, y1, H_SERVO_Z), (0, 1, 0))
    horn = place(cyl(MG995_HORN[0] / 2, MG995_HORN[1]), (H_SERVO_X, y1 + MG995_SPLINE[1], H_SERVO_Z), (0, 1, 0))
    cable = box_min(x0 + 4, y0 + 4, z0 - 3, x1 - 4, y0 + 8, z0)
    return case + ears + top + spline + horn + cable


def servo_ear_points():
    zc = H_SERVO_Z - MG995_OUT + MG995_L / 2
    return [(H_SERVO_X + dx, zc + dz) for dz in (-MG995_HOLES[0] / 2, MG995_HOLES[0] / 2) for dx in (-MG995_HOLES[1] / 2, MG995_HOLES[1] / 2)]


def hammer_block_body():
    """Soporte del rodamiento 608 del lado izquierdo (pegado a la placa lateral)."""
    y0, y1 = H_BEARING_Y[0], FRAME_IN
    blk = box_min(HAMMER_X - 16, y0, max(HAMMER_Z - 16, H_BRACKET_ZMIN), HAMMER_X + 16, y1, HAMMER_Z + 16)
    blk = bd.fillet(blk.edges().filter_by(bd.Axis.Y), 3.0)
    blk = blk - place(cyl(11.0 + 0.05, H_BEARING_Y[1] - y0 + 0.02, -0.01), (HAMMER_X, y0, HAMMER_Z), (0, 1, 0))
    blk = blk - place(cyl(H_SHAFT_D / 2 + 1.0, y1 - y0 + 2, -1), (HAMMER_X, y0, HAMMER_Z), (0, 1, 0))
    for x, z in hammer_screw_points():
        blk = blk - place(cyl(1.5, 6.0), (x, y1, z), (0, -1, 0))   # inserto de latón M3
    return blk


def hammer_bracket_left_body():
    """Soporte izquierdo: bloque del 608, puente sobre los engranes, poste y placa donde se atornilla el MG995."""
    blk = hammer_block_body()
    post = (H_SERVO_X + 16.0, H_SERVO_Z + 16.0)
    bridge_y0, bridge_y1 = H_GEAR_Y + H_GEAR_W / 2 + 0.5, H_BEARING_Y[0]
    bridge = hull(bd.Pos(HAMMER_X, HAMMER_Z) * bd.Circle(16.0), bd.Pos(H_SERVO_X, H_SERVO_Z) * bd.Circle(14.0), bd.Pos(*post) * bd.Circle(6.0))
    bridge = bd.extrude(xz_plane(bridge_y1) * bridge, amount=bridge_y1 - bridge_y0)
    plate_y1 = H_SERVO_TOP_Y - MG995_H + MG995_EARS[2] - MG995_EARS[1]   # bajo las orejas del servo
    plate_y0 = plate_y1 - 6.0
    zc = H_SERVO_Z - MG995_OUT + MG995_L / 2
    ear_box = bd.Pos(H_SERVO_X, zc) * bd.Rectangle(MG995_W + 8.0, MG995_EARS[0] + 4.0)
    plate = hull(ear_box, bd.Pos(*post) * bd.Circle(6.0))
    plate = plate - bd.Pos(H_SERVO_X, zc) * bd.Rectangle(MG995_W + 0.6, MG995_L + 0.6)
    plate = bd.extrude(xz_plane(plate_y1) * plate, amount=plate_y1 - plate_y0)
    for x, z in servo_ear_points():   # insertos de latón M3 para las orejas
        plate = plate - place(cyl(1.5, 6.0), (x, plate_y1, z), (0, -1, 0))
    pillar = place(cyl(5.0, bridge_y1 - plate_y0), (post[0], plate_y0, post[1]), (0, 1, 0))
    body = blk + bridge + plate + pillar
    body = body - box_min(-200, 0, 0, 200, 100, H_BRACKET_ZMIN)            # nada debajo de z = 93
    body = body - place(cyl(H_SHAFT_D / 2 + 1.0, 40.0, -20.0), (HAMMER_X, bridge_y0, HAMMER_Z), (0, 1, 0))
    return body


def hammer_parts(theta):
    """Martillo completo; `theta` = giro hacia atrás en grados (0 = parado)."""
    loc = hammer_loc(theta)
    # fase de los engranes: un diente del del martillo apunta al servo y un hueco del del servo al martillo
    # (sistema local de los engranes: X = X del robot, Y = Z del robot)
    alpha = math.degrees(math.atan2(H_SERVO_Z - HAMMER_Z, H_SERVO_X - HAMMER_X))
    leg_mid = FIG_SCALE * (1.99 + 10.0) / 2
    moving = [
        finish(figure_body(), "monito_ceti", "#1f5fae"),
        finish(place(cyl(H_SHAFT_D / 2, H_SHAFT_Y[1] - H_SHAFT_Y[0]), (0, H_SHAFT_Y[0], 0), (0, 1, 0)), "eje_martillo_8mm", ALU),
        finish(place(spur_gear(H_GEAR_TEETH[1], H_SHAFT_D).moved(bd.Location((0, 0, 0), (0, 0, alpha))), (0, H_GEAR_Y, 0), (0, -1, 0)), "engrane_martillo_20T", PETG),
    ]
    for side in (1, -1):
        moving.append(place(set_screw(4, 8), (0, side * leg_mid, -FIG_FOOT_R), (0, 0, -1)))
    moving = [finish(m.moved(loc), m.label, m.color) for m in moving]
    # piezas fijas
    fixed = [finish(hammer_bracket_left_body(), "soporte_martillo_izq", PETG)]
    fixed.append(mirror_y(finish(hammer_block_body(), "soporte_martillo_der", PETG)))
    for side in (1, -1):
        fixed.append(place(bearing(8, 22, 7, "608_2RS"), (HAMMER_X, side * H_BEARING_Y[0], HAMMER_Z), (0, side, 0)))
    fixed.append(finish(mg995_body(), "servo_mg995", "#1b1b1b"))
    gear_a = alpha + 180.0 + 180.0 / H_GEAR_TEETH[0] - theta * H_GEAR_TEETH[1] / H_GEAR_TEETH[0]
    sg = servo_gear().moved(bd.Location((0, 0, 0), (0, 0, gear_a)))
    fixed.append(finish(place(sg, (H_SERVO_X, H_GEAR_Y, H_SERVO_Z), (0, -1, 0)), "engrane_servo_20T", PETG))
    ear_top = H_SERVO_TOP_Y - MG995_H + MG995_EARS[2]
    for x, z in servo_ear_points():
        fixed.append(place(socket_cap_screw(3, 8), (x, ear_top, z), (0, 1, 0)))
    return moving + fixed


@model
def monito_ceti():
    return finish(figure_body(), "monito_ceti", "#1f5fae")


# ================================================================= ensamble
def chassis_parts():
    parts = [finish(base_plate_body(), "placa_base", ALU), finish(rear_wall_body(), "pared_trasera", PETG), finish(deck_body(), "cubierta_electronica", "#4a4f57")]
    for x, y in STANDOFF_XY:
        parts.append(finish(bd.Pos(x, y, BASE_TOP) * hex_standoff(DECK_Z - BASE_TOP), "separador_M3x45", "#c8a24a"))
        parts.append(place(countersunk_screw(3, 8), (x, y, BASE_Z0), (0, 0, -1)))
        parts.append(place(socket_cap_screw(3, 6), (x, y, DECK_Z + DECK_T), (0, 0, 1)))
    for x, y in REAR_FOOT_HOLES:
        parts.append(place(countersunk_screw(3, 10), (x, y, BASE_Z0), (0, 0, -1)))
        parts.append(place(nut(3), (x, y, BASE_TOP + 4.0), (0, 0, 1)))
    return parts


def electronics_parts():
    parts = [
        battery_pack(BAT_3S, BASE_TOP, "bateria_3S_traccion", "#1f9e89"),
        battery_pack(BAT_5S, BASE_TOP + BAT_3S[3], "bateria_5S_arma", "#2d6cdf"),
    ]
    parts += freenove_board()
    for x, y in FREENOVE_HOLES:
        parts.append(finish(bd.Pos(x, y, DECK_Z + DECK_T) * hex_standoff(6.0), "separador_M3x6", "#c8a24a"))
        parts.append(place(socket_cap_screw(3, 4), (x, y, FREENOVE_Z + 1.6), (0, 0, 1)))
        parts.append(place(countersunk_screw(3, 6), (x, y, DECK_Z), (0, 0, -1)))
    parts += l298n_module()
    for x, y in l298_holes():
        parts.append(finish(bd.Pos(x, y, BASE_TOP) * hex_standoff(6.0), "separador_M3x6", "#c8a24a"))
        parts.append(place(countersunk_screw(3, 6), (x, y, BASE_Z0), (0, 0, -1)))
        parts.append(place(socket_cap_screw(3, 4), (x, y, BASE_TOP + 6.0 + 1.6), (0, 0, 1)))
    parts += relay_automotive()
    parts += pila_9v_parts()
    for x in RELAY_HOLES_X:
        parts.append(place(socket_cap_screw(3, 12), (x, RELAY_C[1], DECK_Z + DECK_T + 4.0), (0, 0, 1)))
        parts.append(place(nut(3), (x, RELAY_C[1], DECK_Z), (0, 0, -1)))
    parts.append(switch(SWITCH_Y, "interruptor_general"))
    parts.append(switch(-SWITCH_Y, "interruptor_arma"))
    return parts


def group(label, parts):
    g = bd.Compound(children=parts)
    g.label = label
    return g


@model
def battlebot_ejemplo():
    left, x_front = drive_side_left()
    right = [mirror_y(p) for p in left]
    robot = bd.Compound(
        children=[
            group("chasis", chassis_parts()),
            group("traccion_izquierda", left),
            group("traccion_derecha", right),
            group("arma", weapon_parts()),
            group("electronica", electronics_parts()),
            group("martillo", hammer_parts(0.0)),
        ]
    )
    robot.label = "battlebot_ejemplo"
    size = robot.bounding_box().size
    assert max(size.X, size.Y, size.Z) <= 300.0, size        # reglamento: cubo de 300 mm
    assert FRONT_X_RANGE[0] + 1 < x_front < FRONT_X_RANGE[1] - 1, x_front
    # sin oruga: lo más bajo deben ser las catarinas (O-rings) y las ruedas delanteras
    assert SPROCKET_Z - (ORING_R_IN + ORING_CS) < IDLER_Z - R_IDLER + 0.5
    assert ORING_R_IN + ORING_CS < LINK_IN_SPROCKET, "los O-rings no deben tocar los eslabones"
    drop = SPROCKET_Z - (ORING_R_IN + ORING_CS)
    assert BASE_Z0 - drop > 3.0 and DISC_Z - BLADE_R - drop > 10.0, drop
    return robot


@model
def battlebot_sin_orugas():
    """El mismo robot sin orugas, apoyado en el piso: muestra que sigue sobre las catarinas motrices."""
    drop = SPROCKET_Z - (ORING_R_IN + ORING_CS)
    groups = []
    for g in battlebot_ejemplo().shape.children:
        kids = [k for k in g.children if not k.label.startswith("eslabon")]
        groups.append(group(g.label, [finish(k.moved(bd.Location((0, 0, -drop))), k.label, k.color) for k in kids]))
    floor = finish(box_min(-150, -150, -2.0, 220, 150, 0.0), "piso_referencia", "#d9dde2")
    robot = bd.Compound(children=groups + [floor])
    robot.label = "battlebot_sin_orugas"
    return robot


@model
def battlebot_martillo_golpe():
    """El robot con el martillo al final de su golpe (HAMMER_STRIKE grados hacia atrás)."""
    groups = [g for g in battlebot_ejemplo().shape.children if g.label != "martillo"]
    robot = bd.Compound(children=groups + [group("martillo", hammer_parts(HAMMER_STRIKE))])
    robot.label = "battlebot_martillo_golpe"
    return robot


@model
def placa_lateral():
    x_front, _ = track_layout()
    return finish(frame_plate_body(x_front), "placa_lateral", ALU)


@model
def placa_base():
    return finish(base_plate_body(), "placa_base", ALU)


@model
def poste_eje_arma():
    return finish(upright_body(), "poste_eje_arma", ALU)


@model
def soporte_motor_arma():
    return finish(weapon_mount_body(), "soporte_motor_arma", PETG)


@model
def hoja_sierra():
    return finish(blade_body(), "hoja_sierra_6in_40T", "#c9ced4")


# ================================================================= piezas impresas (una por una y acomodadas para imprimir)
def print_pose(shape, rot=(0, 0, 0)):
    """Gira la pieza a su orientación de impresión y la deja centrada en XY con la base en z = 0."""
    r = bd.Rot(*rot) * shape
    bb = r.bounding_box()
    return bd.Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * r


def printed_parts():
    """(nombre, cantidad, material, cuerpo en orientación de impresión). Ver docs/diseno/impresion-3d.md."""
    return [
        ("eslabon_oruga", 94, TPU, print_pose(track_link_body(), (90, 0, 0))),           # de canto, pernos verticales
        ("cuna_motor_arma", 1, TPU, print_pose(saddle_body())),
        ("catarina", 2, PETG, print_pose(sprocket_body())),
        ("rueda_libre", 4, PETG, print_pose(idler_body())),
        ("soporte_motor_arma", 1, PETG, print_pose(weapon_mount_body())),                 # pie en la cama
        ("pared_trasera", 1, PETG, print_pose(rear_wall_body(), (0, -90, 0))),            # acostada
        ("cubierta_electronica", 1, PETG, print_pose(deck_body())),
        ("porta_pila_9V", 1, PETG, print_pose(pila_9v_parts()[0])),
        ("monito_ceti", 1, PETG, print_pose(figure_body(), (0, -90, 0))),                # acostado sobre la placa trasera
        ("soporte_martillo_izq", 1, PETG, print_pose(hammer_bracket_left_body(), (-90, 0, 0))),   # cara de la placa lateral abajo
        ("soporte_martillo_der", 1, PETG, print_pose(mirror_y(finish(hammer_block_body(), "x", PETG)), (90, 0, 0))),
        ("engrane_martillo_20T", 1, PETG, print_pose(spur_gear(H_GEAR_TEETH[1], H_SHAFT_D))),
        ("engrane_servo_20T", 1, PETG, print_pose(servo_gear())),
    ]


def printed_part(name):
    for n, _, color, body in printed_parts():
        if n == name:
            return finish(body, n, color)
    raise KeyError(name)


@model
def pared_trasera():
    return printed_part("pared_trasera")


@model
def cubierta_electronica():
    return printed_part("cubierta_electronica")


@model
def porta_pila_9v():
    return printed_part("porta_pila_9V")


@model
def cuna_motor_arma():
    return printed_part("cuna_motor_arma")


@model
def soporte_martillo_izq():
    return printed_part("soporte_martillo_izq")


@model
def soporte_martillo_der():
    return printed_part("soporte_martillo_der")


@model
def engrane_martillo():
    return printed_part("engrane_martillo_20T")


@model
def engrane_servo():
    return printed_part("engrane_servo_20T")


@model
def piezas_impresion():
    """Una pieza de cada tipo, en su orientación de impresión y en filas (negro = TPU, naranja = PETG).

    La etiqueta lleva la cantidad a imprimir (p. ej. eslabon_oruga_x94).
    """
    gap, row_w = 15.0, 520.0
    x = y = row_h = 0.0
    parts = []
    for name, qty, color, body in printed_parts():
        bb = body.bounding_box()
        w, d = bb.max.X - bb.min.X, bb.max.Y - bb.min.Y
        if x > 0 and x + w > row_w:
            x, y, row_h = 0.0, y - row_h - gap, 0.0
        parts.append(finish(bd.Pos(x + w / 2, y - d / 2, 0) * body, f"{name}_x{qty}", color))
        x += w + gap
        row_h = max(row_h, d)
    return bd.Compound(children=parts, label="piezas_impresion")


if __name__ == "__main__":
    eslabon_oruga()
    catarina()
    rueda_libre()
    placa_lateral()
    placa_base()
    poste_eje_arma()
    soporte_motor_arma()
    hoja_sierra()
    battlebot_ejemplo()
    battlebot_sin_orugas()
    monito_ceti()
    battlebot_martillo_golpe()
    pared_trasera()
    cubierta_electronica()
    porta_pila_9v()
    cuna_motor_arma()
    soporte_martillo_izq()
    soporte_martillo_der()
    engrane_martillo()
    engrane_servo()
    piezas_impresion()
