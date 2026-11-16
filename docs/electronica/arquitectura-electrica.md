# Arquitectura eléctrica

Estado: **propuesta para revisar**, armada con las fichas de `hardware/referencias/`. Los valores
marcados con ⚠ dependen de medidas pendientes.

## Diagrama

```
 PILA 9 V            BATERÍA 3S 18650 (10.8–12.6 V)              BATERÍA 5S 18650 (18–21 V)
   │                        │                                           │
   └──[Interruptor general de DOBLE POLO]──┘                 [Interruptor del arma: llave/conector removible]
   │                        │                                           │
   │                  [Fusible 7.5 A ⚠]                          [Fusible ⚠ según el 775]
   │                        │                                           │
   │                        ├──────────► L298N  VS (+12V)               │
   │                        │             │  OUT1/OUT2 ──► Motor JGB37 izq.
   │                        │             │  OUT3/OUT4 ──► Motor JGB37 der.
   │                        │             │  +5V (lógica) ◄── 5 V Freenove
   │                        │             │  ENA IN1 IN2 ENB IN3 IN4 ◄── ESP32
   │                        │                                           │
   │                        └──► Bobina del relevador (12 V) ◄── transistor ◄── ESP32 GPIO 21
   │                                                                    │
   └──► Jack DC de la Freenove Breakout                     Contacto NO del relevador
           ├── 5 V (VC1) ──► ESP32-S3 (pin 5V), lógica L298N            │
           └── 3.3 V (VC2) ──► sensores (si hay)            Motor 775 de 20 V ── diodo de rueda libre
                                                                        │
             GND común: 9 V(−), 3S(−), 5S(−) ⚠, L298N GND, Freenove GND
```

- **El ESP32 se alimenta de una pila de 9 V aparte**: queda aislado del ruido y las caídas de los motores.
  Su negativo se une a la tierra común para que las señales al L298N y al relevador tengan referencia.
- **El interruptor general corta la pila de 9 V y la 3S a la vez** (doble polo), para que un solo
  interruptor apague todo el control y la tracción.
- La tierra de la 5S se une a la tierra común solo si el relevador se maneja con transistor referido a
  GND; con un módulo optoacoplado la 5S puede quedar aislada (mejor para el ruido del motor del arma).
  Decidir al elegir el relevador.
- Las dos baterías 18650 llevan BMS personalizado; ver la ficha de [baterías](../../hardware/referencias/baterias/README.md)
  sobre la corriente de corte del BMS del arma.

## Voltajes y corrientes

| Rama | Voltaje | Corriente esperada | Notas |
| --- | --- | --- | --- |
| Motores de tracción | 3S → 8–10 V en el motor (caída del L298N) | Hasta 2 A por canal continuos, 3 A pico | Corriente de bloqueo del JGB37 por medir ⚠ |
| Freenove + ESP32-S3 | Pila de 9 V → 5 V y 3.3 V | ≈0.1–0.25 A (BLE activo) | Una alcalina dura ≈ 1–2 h: cambiarla antes de cada combate ⚠ |
| Bobina del relevador | 12 V (o 5 V) | ≈0.15 A (automotriz 12 V) | Según el modelo ⚠ |
| Motor del arma (775 de 20 V) | 5S, 18–21 V | Arranque desconocido (posiblemente decenas de A) | Medir; el BMS no debe cortar en el arranque ⚠ |

## Medición de baterías (ADC1)

El ADC del ESP32-S3 mide hasta ≈3.1 V (atenuación de 11 dB). Divisores propuestos:

| Batería | Máximo | Divisor (R arriba / R abajo) | Voltaje en el pin | GPIO |
| --- | --- | --- | --- | --- |
| 3S | 12.6 V | 100 kΩ / 27 kΩ | 2.68 V | 1 |
| 5S | 21.0 V | 100 kΩ / 15 kΩ | 2.74 V | 2 |
| Pila 9 V | 9.6 V | 100 kΩ / 39 kΩ | 2.69 V | 8 |

Agregar un capacitor de 100 nF del pin a GND para filtrar el ruido de los motores.

## Seguridad (reglamento)

| Requisito | Cómo se cumple |
| --- | --- |
| Interruptor general | Interruptor de doble polo que corta la 3S y la pila de 9 V, accesible desde fuera (pared trasera) |
| Interruptor del arma | Conector o llave removible en serie con la 5S, antes del relevador |
| Failsafe | Si no llega señal del control en ≈300 ms: ENA/ENB a bajo (motores libres) y relevador apagado |
| Arranque seguro | GPIO 21 en bajo al arrancar; relevador con contacto NO; el firmware no arma el arma hasta recibir el control |
| Fusibles | Uno por batería de 18650 (la pila de 9 V no lo necesita) |
| Seguro mecánico del arma | Perno de 6 mm que atraviesa los postes y la hoja |

## Calibres de cable sugeridos

| Rama | Calibre |
| --- | --- |
| 3S → L298N → motores | 18 AWG |
| Señales ESP32 → L298N / relevador | 22–26 AWG (jumpers) |
| 5S → relevador → motor del arma | 14 AWG o más grueso, según la corriente de arranque ⚠ |

## Fichas de componentes

- [Placa Freenove Breakout](../../hardware/referencias/placa-breakout-freenove/README.md)
- [ESP32-S3](../../hardware/referencias/esp32-s3/README.md) (pines a evitar y asignación propuesta)
- [Driver L298N](../../hardware/referencias/driver-l298n/README.md)
- [Relevador del arma](../../hardware/referencias/relevador-arma/README.md)
- [Motores JGB37-520](../../hardware/referencias/motor-traccion-jgb37-520/README.md)
- [Baterías](../../hardware/referencias/baterias/README.md)
- [Motor del arma: 775 de 20 V de la desbrozadora](../../hardware/referencias/motor-arma-desbrozadora/README.md)

## Referencias

- [Freenove FNK0101: Breakout Board](https://docs.freenove.com/projects/fnk0101/en/latest/fnk0101/codes/tutorial/1_Freenove_Breakout_Board.html) y [cap. 2: ESP32](https://docs.freenove.com/projects/fnk0101/en/latest/fnk0101/codes/tutorial/2_ESP32.html)
- [STMicroelectronics: hoja de datos del L298 (PDF)](https://www.st.com/resource/en/datasheet/l298.pdf)
- [Last Minute Engineers: L298N](https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/)
- [Espressif: hoja de datos del ESP32-S3 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)
