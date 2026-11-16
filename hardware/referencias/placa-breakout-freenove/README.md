# Placa de expansión Freenove Breakout Board (FNK0101)

Placa base donde se enchufa el ESP32-S3. Saca cada GPIO a tres lugares conectados entre sí: un
socket, un pin (amarillo) y una clema de tornillo. Además tiene un LED indicador por GPIO y dos
reguladores para alimentar sensores y módulos.

![Partes de la placa](terceros/freenove-breakout-partes.png)

## Datos (documentación de Freenove)

| Dato | Valor | Notas |
| --- | --- | --- |
| Placas compatibles | ESP32 WROOM/WROVER, ESP32-S3 WROOM y WROOM Lite, ESP8266, Raspberry Pi Pico, otras | Separación entre filas de pines de 600 a 1000 mil (15.2 a 25.4 mm) |
| Filas por lado | 24 posiciones (L1–L24 y R1–R24) | Cada GPIO tiene pin amarillo (señal), rojo (VCC) y negro (GND), más clema |
| Entrada de alimentación | Jack DC005 (centro positivo) | Plano del jack abajo |
| Voltaje de entrada | **5–12 V** según la guía (recomienda 12 V / 3 A); el serigrafiado de la placa dice **6–24 V** | ⚠ Las dos fuentes no coinciden; los capacitores visibles son de 16 V |
| Reguladores | 5 V y 3.3 V; corriente total de salida **3 A** (5 V + 3.3 V juntos), según el serigrafiado | La guía dice 3 A cada uno; tomar 3 A en total para ir a la segura |
| Rieles VC1 y VC2 | Pines rojos de la izquierda (VC1) y de la derecha (VC2); cada uno se pone a 5 V o 3.3 V con un jumper | Freenove sugiere VC1 = 5 V y VC2 = 3.3 V |
| LEDs indicadores | Uno por GPIO, a través de un buffer: encendido = alto, apagado = bajo, parpadea = flotante | El buffer aísla al GPIO, así que el LED no afecta las lecturas del ADC ni el I²C |
| Clemas | Tipo KF128 | Paso por medir |
| USB y fuente externa juntas | Hay que cortar el puente de 5 V para no conectar la fuente externa con el USB de la PC | Ver imagen `freenove-breakout-usb-y-externa.png` |

| Jumpers VC1/VC2 | Jack DC y plano del DC005 |
| --- | --- |
| ![Jumpers](terceros/freenove-breakout-jumpers-vc.png) | ![Jack DC](terceros/freenove-breakout-jack-dc.png) |

## Qué implica para el robot

- **Voltaje de la batería 3S**: con carga completa da 12.6 V, un poco más que los 12 V de la guía
  pero dentro de los 6–24 V del serigrafiado. Hay que confirmar el voltaje máximo de los reguladores
  (leer el número de los chips U1/U11) antes de conectarla directo. Si no se puede, alimentar la placa
  con un regulador reductor de 5 V aparte.
- **Tamaño y peso**: es una placa grande, con clemas en ambos lados. Hay que medirla y pesarla: puede
  costar más espacio y peso del que conviene en un robot de 3 kg.
- **Vibración**: los sockets sujetan el ESP32 solo por fricción. En combate conviene asegurarlo con una
  cinta, un cincho o un tope impreso.
- **Pines rojos**: todos los pines rojos de un lado están al mismo voltaje (VC1 o VC2). No conectar ahí
  módulos que necesiten el voltaje de la batería.

## Por medir

- [ ] Largo, ancho y alto con las clemas; posición y diámetro de los 4 barrenos de montaje.
- [ ] Peso con y sin el ESP32-S3.
- [ ] Número de los reguladores (U1, U11) y su voltaje máximo de entrada.
- [ ] Paso de las clemas.

## Fuentes

Todas descargadas el 2026-11-15.

| Archivo | Página de origen | Imagen original |
| --- | --- | --- |
| `terceros/freenove-breakout-partes.png` | [Freenove FNK0101, cap. 1: Freenove Breakout Board](https://docs.freenove.com/projects/fnk0101/en/latest/fnk0101/codes/tutorial/1_Freenove_Breakout_Board.html) | [Chapter01_00.png](https://docs.freenove.com/projects/fnk0101/en/latest/_images/Chapter01_00.png) |
| `terceros/freenove-breakout-jumpers-vc.png` | [Freenove FNK0101, cap. 1](https://docs.freenove.com/projects/fnk0101/en/latest/fnk0101/codes/tutorial/1_Freenove_Breakout_Board.html) | [Chapter01_06.png](https://docs.freenove.com/projects/fnk0101/en/latest/_images/Chapter01_06.png) |
| `terceros/freenove-breakout-jack-dc.png` | [Freenove FNK0101, cap. 2: ESP32](https://docs.freenove.com/projects/fnk0101/en/latest/fnk0101/codes/tutorial/2_ESP32.html) | [Chapter02_07.png](https://docs.freenove.com/projects/fnk0101/en/latest/_images/Chapter02_07.png) |
| `terceros/freenove-breakout-usb-y-externa.png` | [Freenove FNK0101, cap. 2: ESP32](https://docs.freenove.com/projects/fnk0101/en/latest/fnk0101/codes/tutorial/2_ESP32.html) | [Chapter02_09.png](https://docs.freenove.com/projects/fnk0101/en/latest/_images/Chapter02_09.png) |

Otras páginas consultadas: [Freenove FNK0101, explicación del diseño (buffer de los LEDs)](https://docs.freenove.com/projects/fnk0101/en/latest/fnk0101/codes/tutorial/Design_Explanation.html).
