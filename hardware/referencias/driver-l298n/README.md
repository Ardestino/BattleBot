# Driver de motores L298N (puente H doble)

Módulo con el chip L298N de ST para mover los dos motores de tracción JGB37-520 (canal A = izquierdo,
canal B = derecho).

![Pines del módulo](terceros/l298n-pinout.png)

## Datos del módulo

| Dato | Valor | Fuente |
| --- | --- | --- |
| Tamaño | ≈43 × 43 mm, 23–27 mm de alto con disipador | Varias tiendas; medir ⚠ |
| Barrenos | 4 en las esquinas | Medida y separación por confirmar ⚠ |
| Peso | Por pesar ⚠ | |
| Voltaje de motores (VS, borne "+12V") | 5–35 V en el módulo (el chip aguanta hasta 46 V) | Módulo / hoja de datos de ST |
| Corriente por canal | 2 A continuos, 3 A pico no repetitivo | Hoja de datos de ST |
| Caída de voltaje (total, fuente + sumidero) | 1.8–3.2 V a 1 A; hasta 4.9 V a 2 A | Hoja de datos de ST |
| Regulador de 5 V | 78M05 en la placa, activo con el jumper "5V-EN" | Úsese solo si VS ≤ 12 V |
| Entradas lógicas | ENA, IN1, IN2 (canal A); ENB, IN3, IN4 (canal B) | Nivel alto mínimo 2.3 V: el ESP32-S3 (3.3 V) las maneja directo |
| Diodos de rueda libre | 8 diodos en la placa | |

| Jumper de 5 V y enable | Caída de voltaje |
| --- | --- |
| ![Jumper 5V](terceros/l298n-jumper-5v-y-enable.jpg) | ![Caída de voltaje](terceros/l298n-caida-de-voltaje.png) |

## Cómo se controla

| ENA | IN1 | IN2 | Motor A |
| --- | --- | --- | --- |
| Bajo | x | x | Libre (sin fuerza) |
| PWM | Alto | Bajo | Adelante, velocidad según el PWM |
| PWM | Bajo | Alto | Atrás |
| Alto | Igual | Igual | Freno |

Para usar PWM hay que **quitar los jumpers de ENA y ENB** y conectarlos a pines con PWM del ESP32.

## Qué implica para el robot

- **Pierde voltaje**: con la 3S (11.1 V nominal, 12.6 V cargada) los motores reciben unos 8–10 V.
  A 333 RPM nominales eso da unas 230–280 RPM y menos torque. Esto empeora el riesgo de que las orugas
  no tengan fuerza para girar (ver [orugas-triangulares.md](../../../docs/diseno/orugas-triangulares.md)).
- **Corriente**: si la corriente de bloqueo del JGB37-520 pasa de 2–3 A, el L298N se calienta y se
  apaga por temperatura en un empujón. Hay que **medir la corriente de bloqueo** del motor.
- **Jumper de 5 V**: con la 3S cargada a 12.6 V, se pasa del límite de 12 V del jumper. Recomendado:
  quitar el jumper y alimentar la lógica (borne +5V) desde los 5 V de la placa Freenove.
- **Tierra común**: el GND del L298N, el de la batería y el del ESP32 deben unirse.
- **Alternativas, si no alcanza**: drivers con MOSFET (menos caída y más corriente), por ejemplo módulos
  con DRV8871, VNH5019 o BTS7960. Por ahora se usa el L298N.

## Por medir

- [ ] Medidas y barrenos del módulo que tenemos; peso.
- [ ] Temperatura del disipador después de 2–3 minutos empujando contra una pared.

## Fuentes

Todas descargadas el 2026-11-15.

| Archivo | Página de origen | Imagen original |
| --- | --- | --- |
| `terceros/l298n-pinout.png` | [Last Minute Engineers: L298N con Arduino](https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/) | [L298N-Motor-Driver-Module-Pinout.png](https://lastminuteengineers.com/wp-content/uploads/arduino/L298N-Motor-Driver-Module-Pinout.png) |
| `terceros/l298n-jumper-5v-y-enable.jpg` | [Last Minute Engineers](https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/) | [L298N-Module-5V-Regulator-and-Enable-Jumper.jpg](https://lastminuteengineers.com/wp-content/uploads/arduino/L298N-Module-5V-Regulator-and-Enable-Jumper.jpg) |
| `terceros/l298n-caida-de-voltaje.png` | [Last Minute Engineers](https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/) | [L298N-Motor-Driver-Module-Internal-Voltage-Drop.png](https://lastminuteengineers.com/wp-content/uploads/arduino/L298N-Motor-Driver-Module-Internal-Voltage-Drop.png) |
| `terceros/l298-caida-de-voltaje-datasheet.png` | [Last Minute Engineers](https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/) (recorte de la hoja de datos de ST) | [L298N-Voltage-Drop-Datasheet-Reference.png](https://lastminuteengineers.com/wp-content/uploads/arduino/v2/L298N-Voltage-Drop-Datasheet-Reference.png) |

Otras páginas consultadas:

- [Hoja de datos oficial del L298, STMicroelectronics (PDF)](https://www.st.com/resource/en/datasheet/l298.pdf): el sitio de ST bloquea la descarga automática; abrirla en el navegador.
- [Circuit Rocks: L298N](https://docs.circuit.rocks/motors/l298n/) y [SunFounder: módulo L298N](https://docs.sunfounder.com/projects/sf-components/en/latest/component_l298n_module.html): tamaño y pines del módulo.
