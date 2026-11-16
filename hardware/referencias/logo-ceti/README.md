# Monito del logotipo del CETI

Referencia para el martillo del robot: el monito del logotipo del CETI, parado a la mitad del robot.

- `terceros/logo_ceti.stl`: modelo de referencia hecho por el usuario en Blender (2026-11-16). Queda solo
  local (las carpetas `terceros/` están en `.gitignore`).
- El logotipo es del CETI. El repositorio es local; **si algún día se publica, hay que pedir permiso al CETI**
  para incluir el logotipo (o quitar `figure_body()` del modelo).

## Medidas del STL

| Elemento | Medida |
| --- | --- |
| Total | 55.4 (ancho) × 61.75 (alto) mm |
| Cuerpo | Dos mitades en L separadas 4 mm: piernas de 8 mm, brazos hasta ±27.7 mm, 7.8 mm de alto |
| Grueso del cuerpo | 4.65 mm |
| Cabeza | Esfera de ≈ 16.5 mm, separada 3.4 mm de los brazos |

## En el robot

`figure_body()` en `hardware/cad/source/battlebot_ejemplo.py` reproduce esas proporciones a escala 2
(111 × 123.5 mm, 9.3 mm de grueso) y agrega una placa trasera de 3 mm que une las dos mitades y la cabeza,
para que se imprima en una sola pieza y se atornille al tubo del martillo. La placa no se ve de frente.
