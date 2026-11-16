# Impresión 3D

## Impresora y materiales

| Dato | Valor |
| --- | --- |
| Impresora | Creality K1 SE (CoreXY, marco abierto, extrusor directo) |
| Volumen de impresión | 220 × 220 × 250 mm |
| Temperaturas máximas | Boquilla 300 °C, cama 100 °C |
| Materiales disponibles | PLA, PETG, TPU (95A) y ABS (sin probar) |

**ABS: no usarlo por ahora.** Sin gabinete se deforma (warping) y se despega de la cama. Si más adelante
hace falta, primero hay que cerrar la impresora con un gabinete (una caja o un mueble tipo Lack con
paneles). Para este robot, el PETG cubre lo que daría el ABS.

**PLA: solo para pruebas de ajuste.** Es barato y preciso, pero se quiebra con los golpes.

## Material de cada pieza

| Pieza | Cant. | Material | Orientación recomendada | Notas |
| --- | --- | --- | --- | --- |
| Eslabón de oruga | 86 + 8 de repuesto | **TPU 95A** | De canto: pernos verticales | Barrenos redondos y la tensión de la oruga queda a lo largo de las capas. Imprimir primero 8 de prueba |
| Catarina motriz | 2 | **PETG** | Cara exterior en la cama, maza hacia arriba | 5–6 perímetros, relleno ≥ 50 %; probar el ajuste del eje en D y de los O-rings |
| Rueda libre | 4 | **PETG** | Plana | La ranura central necesita soporte (o imprimir la rueda en dos mitades) |
| Soporte del motor del arma | 1 | **PETG** | Pie en la cama | 5 perímetros; el motor 775 se calienta y el PETG aguanta más que el PLA |
| Cuna del motor del arma | 1 | **TPU 95A** | Plana | Amortigua la vibración del motor |
| Pared trasera | 1 | **PETG** | Acostada (cara grande en la cama) | |
| Cubierta de electrónica | 1 | **PETG** | Plana | |
| Placa lateral (opcional) | 2 | PETG | Plana | Cabe (200 × 118 mm). En PETG de 5 mm pesa ≈ 76 g contra 162 g en aluminio: ahorra ≈ 170 g. Conviene subirla a 6–8 mm y probarla |
| Placa base | 1 | Aluminio 3 mm | — | No cabe plana en la cama (245 × 149 mm); impresa tendría que ir en dos mitades |
| Postes del eje del arma | 2 | Aluminio | — | Sostienen los rodamientos del arma; en PETG solo para pruebas |

## Ajustes de inicio (afinar con pruebas)

| | PETG | TPU 95A |
| --- | --- | --- |
| Boquilla | 240–250 °C | 220–230 °C |
| Cama | 70–80 °C | 40–50 °C |
| Velocidad | normal del perfil | ≤ 40–50 mm/s, retracción corta |
| Perímetros | 4–6 | 3–4 |
| Relleno | 40–60 % gyroid | 30–50 % |

## Revisión de fabricabilidad

Revisión de impresión FDM con text-to-cad (`cad model dfm --process printing --technology fdm`,
boquilla de 0.4 mm, capas de 0.2 mm, volumen de 220 × 220 × 250 mm), 2026-11-16:

| Pieza | Resultado | Qué se corrigió / qué queda |
| --- | --- | --- |
| Eslabón (TPU) | OK, 5 avisos | Voladizos; desaparecen casi todos imprimiéndolo de canto |
| Catarina (PETG) | OK tras corregir | Había paredes de 0.2 mm entre los aligeramientos y los huecos de los dientes y una capa de 0.08 mm sobre el prisionero: se movieron los aligeramientos (Ø4.4 a radio 10) y el prisionero (z = 6.5) |
| Rueda libre (PETG) | OK, 2 avisos | Voladizo y puente de 9 mm en la ranura central: usar soporte |
| Soporte motor del arma (PETG) | OK tras corregir | Había una pared de 0.77 mm entre el buje y los avellanados: el barreno del buje bajó a Ø18 mm |
| Placa lateral (PETG) | OK, 12 avisos | Barrenos horizontales grandes y voladizos si se imprime de pie; plana no los tiene |
| Poste del arma (PETG) | OK, 5 avisos | Solo como prototipo |

## Orden sugerido

1. **8 eslabones en TPU y uno en PETG**, con 2 tramos de hilo de nylon de 3 mm: revisar que giren sin trabarse.
2. **Una catarina** con sus O-rings, para probar el ajuste en el eje del JGB37-520.
3. **Una rueda libre** con dos 606, para probar el apriete de los rodamientos.
4. Ajustar holguras en el modelo y luego imprimir todo.
