"""Soporte para motorreductor JGA25-370 (Ø25 mm) del BattleBot.

Placa en L con dos nervios. El motor se atornilla por la cara del reductor con 2 tornillos
M3 de cabeza avellanada (quedan al ras del lado de la rueda) y el soporte se fija al chasis
con 4 tornillos M3 desde abajo, apretados contra tuercas embutidas en la base.

Sirve para impresión 3D (PETG o nylon) o para fresar en aluminio; todavía no se eligió proceso.
Las medidas del motor son las típicas del JGA25-370: confírmalas con calibrador antes de fabricar.

Sistema de coordenadas: el eje del motor va a lo largo de +Y, la cara de montaje está en y = 0
(rueda del lado -Y, cuerpo del motor del lado +Y) y la base apoya en z = 0 sobre el chasis.
"""
import build123d as bd
from cad import model

# --- Motor JGA25-370 (valores típicos; verificar) ---
MOTOR_D = 25.0          # diámetro del reductor y del motor
MOTOR_LEN = 52.0        # largo aproximado reductor + motor (sin el eje)
BOSS_D = 7.0            # buje del eje en la cara del reductor
BOSS_H = 2.5            # cuánto sobresale el buje
SHAFT_D = 4.0           # eje en D
SHAFT_LEN = 12.0
FACE_HOLE_SPACING = 17.0  # 2 x M3 en la cara del reductor

# --- Tornillería M3 ---
M3_CLEAR_D = 3.4        # barreno de paso
M3_CSK_D = 6.4          # avellanado a 90° para cabeza plana M3
M3_NUT_AF = 5.7         # tuerca M3 (5.5 entre caras + holgura)
M3_NUT_DEPTH = 2.7


def motor_mount_body(
    width=36.0,           # ancho del soporte (diámetro del remate redondo)
    face_t=5.0,           # espesor de la placa de montaje
    base_t=5.0,           # espesor de la base
    base_depth=30.0,      # cuánto se extiende la base bajo el motor (desde la cara)
    motor_clearance=1.0,  # aire entre el motor y la base
    motor_gap=0.5,        # aire radial alrededor del motor en el redondeo interior
    bore_clearance=1.0,   # holgura diametral alrededor del buje
    rib_t=3.0,            # espesor de los nervios
    rib_len=16.0,         # largo del nervio sobre la base
    rib_h=18.0,           # alto del nervio sobre la base
    inner_fillet=3.0,     # redondeo interior base-placa
    corner_fillet=4.0,    # redondeo de las esquinas traseras de la base
    base_holes=((-10.0, 12.0), (10.0, 12.0), (-10.0, 25.0), (10.0, 25.0)),
):
    axis_h = base_t + motor_clearance + MOTOR_D / 2  # altura del eje sobre el chasis

    # Placa vertical: rectángulo hasta el eje y remate semicircular concéntrico con el motor.
    profile = bd.Rectangle(width, axis_h, align=(bd.Align.CENTER, bd.Align.MIN)) + bd.Pos(
        0, axis_h
    ) * bd.Circle(width / 2)
    face = bd.extrude(bd.Plane.XZ * profile, amount=face_t)  # Plane.XZ extruye hacia -Y

    # Base: de la cara de la rueda (y = -face_t) hacia atrás, bajo el motor.
    base = bd.Pos(0, (base_depth - face_t) / 2, 0) * bd.Box(
        width, base_depth + face_t, base_t, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    body = base + face

    # Redondeo interior entre la base y la placa (lado del motor) y esquinas traseras.
    inner = (
        body.edges()
        .filter_by(bd.Axis.X)
        .filter_by(lambda e: abs(e.center().Y) < 1e-6 and abs(e.center().Z - base_t) < 1e-6)
    )
    body = bd.fillet(inner, inner_fillet)
    back_corners = (
        body.edges()
        .filter_by(bd.Axis.Z)
        .filter_by(lambda e: abs(e.center().Y - base_depth) < 1e-6)
    )
    body = bd.fillet(back_corners, corner_fillet)

    # Espacio libre para el cuerpo del motor (el redondeo interior queda solo a los lados).
    body = body - bd.Pos(0, 0, axis_h) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        MOTOR_D / 2 + motor_gap, base_depth + 1, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )

    # Nervios a los lados, fuera del cuerpo del motor.
    rib_x = MOTOR_D / 2 + 1.5  # cara interior del nervio
    rib_profile = bd.Polygon((0, base_t), (rib_len, base_t), (0, base_t + rib_h), align=None)
    rib = bd.extrude(bd.Plane.YZ.offset(rib_x) * rib_profile, amount=rib_t)
    body = body + rib + bd.mirror(rib, bd.Plane.YZ)

    # Barreno para el buje del eje.
    bore_d = BOSS_D + bore_clearance
    body = body - bd.Pos(0, -face_t - 1, axis_h) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        bore_d / 2, face_t + 2, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )

    # 2 x M3 avellanados desde el lado de la rueda.
    csk_depth = (M3_CSK_D - M3_CLEAR_D) / 2  # 90°: la profundidad es igual a la diferencia de radios
    for x in (-FACE_HOLE_SPACING / 2, FACE_HOLE_SPACING / 2):
        body = body - bd.Pos(x, -face_t - 1, axis_h) * bd.Rot(-90, 0, 0) * bd.Cylinder(
            M3_CLEAR_D / 2, face_t + 2, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        body = body - bd.Pos(x, -face_t, axis_h) * bd.Rot(-90, 0, 0) * bd.Cone(
            M3_CSK_D / 2, M3_CLEAR_D / 2, csk_depth, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )

    # 4 x M3 hacia el chasis, con tuerca hexagonal embutida desde arriba.
    nut_r = M3_NUT_AF / 3**0.5  # radio circunscrito del hexágono
    for x, y in base_holes:
        body = body - bd.Pos(x, y, -1) * bd.Cylinder(
            M3_CLEAR_D / 2, base_t + 2, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        body = body - bd.extrude(
            bd.Pos(x, y, base_t - M3_NUT_DEPTH) * bd.RegularPolygon(nut_r, 6), amount=M3_NUT_DEPTH + 1
        )

    body.label = "soporte_motor"
    body.color = "#3d5a80"
    return body


def motor_reference(axis_h):
    """Motor de referencia (solo para revisar holguras; no se fabrica)."""
    can = bd.Pos(0, 0, axis_h) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        MOTOR_D / 2, MOTOR_LEN, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    boss = bd.Pos(0, -BOSS_H, axis_h) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        BOSS_D / 2, BOSS_H, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    shaft = bd.Pos(0, -SHAFT_LEN, axis_h) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        SHAFT_D / 2, SHAFT_LEN - BOSS_H, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    motor = can + boss + shaft
    motor.label = "motor_jga25"
    motor.color = "#9aa0a6"
    return motor


@model
def soporte_motor_jga25():
    body = motor_mount_body()
    size = body.bounding_box().size
    assert abs(size.X - 36.0) < 0.01, size
    assert abs(size.Y - 35.0) < 0.01, size
    assert abs(size.Z - 36.5) < 0.01, size  # eje a 18.5 mm + radio de 18 mm
    return body


@model
def soporte_motor_jga25_con_motor():
    mount = soporte_motor_jga25().shape
    motor = motor_reference(axis_h=5.0 + 1.0 + MOTOR_D / 2)
    kit = bd.Compound(children=[mount, motor])
    kit.label = "soporte_con_motor"
    return kit


if __name__ == "__main__":
    soporte_motor_jga25()
    soporte_motor_jga25_con_motor()
