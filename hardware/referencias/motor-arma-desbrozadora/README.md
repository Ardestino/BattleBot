# Motor del arma: desbrozadora inalámbrica de 21 V con hoja de sierra de 6"

Reemplaza al motor de podadora de 24 V. Se usará el motor de la cabeza de la desbrozadora y la hoja de
sierra de 6" que trae.

![Instalación de la hoja (imagen de la publicación)](terceros/temu-desbrozadora-instalacion-hoja.jpg)

## Datos de la publicación

| Dato | Valor |
| --- | --- |
| Producto | Desbrozadora / cortadora de césped eléctrica inalámbrica de 21 V, 2 baterías, 2 cargadores, barra ajustable (código del vendedor xbmxf210bk) |
| Precio visto | MX$473.19 (2026-11-16) |
| Batería | 21 V (5S Li-ion); trae 2 |
| Hoja | Sierra circular de 6" (≈152 mm), dientes de carburo (≈40) |
| Montaje de la hoja | Directa sobre el eje del motor, con rondana y tornillo |

La publicación **no da** potencia real, RPM, tipo de motor, medidas ni peso.

## Motor: 775 de 20 V (confirmado)

![Dimensiones del motor 775](terceros/motor-775-20V-dimensiones.webp)

| Dato | Valor | Fuente |
| --- | --- | --- |
| Tipo | Motor de escobillas **775**, 20 V | Usuario (2026-11-16) |
| Diámetro de la lata | 42 mm (medido: **41.81 mm**) | Plano / medido |
| Diámetro máximo | 45 mm (incluye terminales) | Plano |
| Largo del cuerpo | 67 mm (la lata sola: **60.40 mm**, medido) | Plano / medido |
| Largo total | 98 mm, de punta a punta del eje | Plano |
| Eje frontal | Ø5 × 17 mm | Plano |
| Eje trasero | Sale una punta corta detrás (≈ 10 mm con su buje) | Plano |
| Barrenos frontales | 2 × M4 a 29 mm (típico del 775; **por medir**) | Supuesto |
| Peso | ≈ 350 g (típico; **por pesar**) | Supuesto |

## Hoja (supuesta hasta medirla)

| Dato | Valor |
| --- | --- |
| Diámetro | 152.4 mm (6") |
| Espesor | 1.8 mm |
| Barreno | 20 mm |
| Peso | ≈ 230 g (calculado en el CAD) |

## Qué implica para el robot

- **Batería**: el voltaje (21 V) coincide con la batería 5S del arma. Las baterías de la desbrozadora
  podrían servir de repuesto si caben (medirlas).
- **Hoja de sierra delgada**: corta bien, pero los dientes de carburo se pueden desprender con los golpes
  y lanzarse. Revisar con los jueces si la permiten. Es más ligera que un disco de acero de 6 mm.
- **Montaje**: en la desbrozadora la hoja va directa al eje del motor. En el robot conviene montarla en
  un eje propio con rodamientos (6201) y mover ese eje con banda, para que los golpes no lleguen a los
  baleros del motor.
- **Seguro mecánico**: hay que hacer un barreno de 7 mm en la hoja para el perno del seguro.

## Por medir al recibirla

- [x] Modelo y medidas del motor: 775 de 20 V, Ø41.81 × 60.40 mm de lata (2026-11-16).
- [ ] Barrenos de la cara del motor (¿2 × M4 a 29 mm?).
- [ ] Peso del motor sin la carcasa.
- [ ] Hoja: diámetro, espesor, barreno central, peso.
- [ ] Corriente sin carga y de arranque a 21 V (para el relevador y el fusible).
- [ ] Medidas y peso de las baterías de 21 V.

## Fuentes

| Archivo | Página de origen | Imagen original |
| --- | --- | --- |
| `terceros/motor-775-20V-dimensiones.webp` | Imagen guardada por el usuario de una publicación del motor 775 (2026-11-16) | — |
| `terceros/temu-desbrozadora-instalacion-hoja.jpg` | [Temu: desbrozadora eléctrica inalámbrica 21 V](https://www.temu.com/mx/goods.html?goods_id=604907939674207) | [8180e237…_1200x1200.jpeg](https://img.kwcdn.com/local-goods-image-g/2066d919cc/8180e237-d4c1-4c8c-ae63-3393d37bec6a_1200x1200.jpeg.format.jpg) |

La página de Temu se carga con JavaScript y no muestra la ficha técnica a descargas automáticas.
