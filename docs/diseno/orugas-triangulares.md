# Orugas triangulares impresas

Reemplazan al kit de ruedas mecanum. Es una oruga de perfil triangular por lado: la rueda motriz
(catarina) arriba y dos ruedas tensoras abajo, con tracción diferencial (un motor JGB37-520 por lado).
El reglamento permite orugas ("ruedas u orugas, con control direccional efectivo").

> El diseño es propio. Se toma la idea mecánica general de la oruga triangular (común en tanques,
> maquinaria y robots), no la apariencia de ningún personaje.

Estado: **recabando información, sin modelar.**

## Geometría propuesta (punto de partida)

```
            (catarina motriz, eje del JGB37-520)
                     /\
                    /  \
                   /    \
                  /      \
       (tensora) O--------O (tensora, con ranura para tensar)
                 ==========  suelo
```

| Parámetro | Valor inicial | Por qué |
| --- | --- | --- |
| Separación entre tensoras (largo de apoyo) | ≈160 mm | Da estabilidad; deja lugar al arma dentro de 300 mm |
| Altura de la catarina sobre las tensoras | ≈90 mm | Sube el motor, lo aleja del piso y de los golpes bajos |
| Paso del eslabón | 12–15 mm | Rango usado en orugas impresas de este tamaño |
| Catarina | 10–12 dientes, diámetro primitivo ≈45–50 mm | Con menos de ~9 dientes la oruga golpetea (efecto poligonal) |
| Ancho de la oruga | ≈30 mm | Por definir con el peso |
| Largo de la oruga | ≈540 mm (≈36–40 eslabones) | Perímetro del triángulo más el arco de las ruedas |
| Velocidad | ≈0.8 m/s (catarina de 47 mm a 333 RPM, sin carga) | v = π · d · RPM / 60 |
| Rodamientos de las tensoras | 625ZZ (5 × 16 × 5 mm) o 608ZZ (8 × 22 × 7 mm) | 625 es más ligero; 608 es más fácil de conseguir |
| Unión catarina-eje | Barreno en D de 6 mm + prisionero M3 con tuerca embutida, o cubo de aluminio de 6 mm | El eje del motor es de 6 mm con plano a 5.5 mm |
| Tensado | Una tensora en ranura con tornillo de ajuste | Una oruga floja se sale en los giros |

Todas son medidas iniciales para discutir. Se fijan cuando tengamos el motor del arma y el
acomodo general dentro de 300 × 300 × 300 mm.

## Opciones de construcción de la oruga

| Opción | Cómo es | A favor | En contra |
| --- | --- | --- | --- |
| **A. Eslabones rígidos con pernos** (recomendada) | Eslabones de PETG o nylon unidos con pernos (filamento de 1.75 mm, varilla o tornillo M3) y zapatas de TPU para agarre | Resiste golpes; un eslabón roto se cambia solo; no se estira | Más piezas y armado; los pernos de acero pesan |
| B. Banda de una pieza en TPU | Banda flexible con dientes internos | Simple, sin pernos, poco ruido | Se estira y puede saltar dientes con mucho torque; si se corta, se pierde toda |
| C. Eslabones mixtos TPU + PETG | Primeras capas en TPU (agarre) y el resto en PETG (rigidez), en la misma impresión | Buen agarre y buena resistencia | Necesita impresora que cambie de material o pausa manual |

## Riesgos que hay que resolver antes de modelar

1. **Torque del motor.** Girar sobre su eje con orugas exige arrastrar la oruga de lado contra el piso.
   Cálculo rápido: con 3 kg y coeficiente de fricción ≈0.8, cada lado necesita ≈12 N; con una catarina
   de 25 mm de radio son ≈0.29 N·m (≈3 kgf·cm) por motor. La única cifra encontrada para un JGB37-520
   parecido (319 RPM) es ≈1.9 kgf·cm de torque de bloqueo, **insuficiente**. Hay que **medir el torque real**
   del motor (palanca + báscula) antes de diseñar. Si no alcanza: catarina más chica, zapatas con menos
   agarre lateral o un motor con más reducción.
2. **Peso.** Estimación por lado: oruga ≈85 g, catarina ≈15 g, 2 tensoras ≈20 g, rodamientos ≈10 g,
   placa lateral ≈40 g, tornillería ≈10 g, total **≈180 g por lado, ≈360 g los dos**, contra ≈70 g de
   2 ruedas. El presupuesto ya estaba excedido (ver [presupuesto-peso.md](presupuesto-peso.md)).
3. **Descarrilamiento.** Es la falla más común de las orugas, sobre todo en giros sobre su eje y en
   pisos con mucha fricción. Se previene con guías centrales en los eslabones, rebordes en la catarina
   y las tensoras, y tensado ajustable.
4. **Golpes del arma rival.** La oruga queda expuesta a los lados. Conviene que la placa lateral o el
   caparazón la cubran por arriba y que el diseño permita cambiar eslabones rápido entre combates.

## Información que falta

- [x] Impresora: Creality K1 SE, 220 × 220 × 250 mm, imprime TPU 95A; un solo extrusor (ver [impresion-3d.md](impresion-3d.md)).
- [x] Materiales: PLA, PETG, TPU 95A y ABS (sin gabinete, no recomendado). Eslabones en TPU, catarinas y ruedas en PETG.
- [ ] Torque de bloqueo real del JGB37-520 (palanca + báscula) y corriente de bloqueo.
- [ ] Medidas del bracket Talos (de ellas depende dónde queda la catarina).
- [ ] Peso y tamaño del motor del arma (decide cuánto peso queda para las orugas).
- [ ] Qué hacer con las ruedas de goma de 65 mm: descartarlas o reusarlas.
- [ ] Tipo de piso de la arena (afecta el agarre y el material de las zapatas).

## Referencias

Proyectos de orugas impresas consultados (2026-11-15). Solo se tomaron ideas generales y cifras;
no se descargaron sus archivos.

- [How To Mechatronics: tanque 100 % impreso](https://howtomechatronics.com/projects/fully-3d-printed-tank-tracked-robot-platform/)
  y [la misma guía en mfgrobots](https://www.mfgrobots.com/Article/mfg/mpm/51235.html): paso de 11 mm,
  catarina de 12 dientes (≈42 mm), pernos de 2 mm con holgura de 0.3 mm en un extremo.
- [Fermilab, trabajo de E. Wilkinson (PDF)](https://indico.fnal.gov/event/60714/contributions/272516/attachments/170032/228657/Elijah%20Wilkinson%20CCI%20Final%20Paper.pdf):
  TPU agarra mejor pero es débil; PETG es más fuerte; eslabones mixtos TPU + PETG.
- [Cogitation Station: orugas impresas ya ensambladas](https://cogitation-station.atlassian.net/wiki/spaces/FIR/pages/452427779/Pre-Assembled+3D+Printed+Tracks):
  hay que iterar el paso y la holgura con piezas de prueba.
- [MakerWorld: cadena impresa paso ISO 16A](https://makerworld.com/models/1028483): eslabones de PETG con pernos de 6 mm.
- [Printables: orugas de TPU/TPE](https://printables.com/model/613519-tputpe-printed-tank-tracks): banda flexible de una pieza.
- [SuperDroid Robots, wiki de orugas](https://www.superdroidrobots.com/wiki-a/index_php/Tracks): descarrilamiento en giros sobre su eje y pisos con mucha fricción.
- [Game Manual 0: transmisiones tipo tanque](https://game-manual-0.readthedocs.io/en/stable/docs/drivetrains/tank.html): giro por derrape (skid-steer).
