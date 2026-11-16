# Placa ESP32-S3 (Freenove ESP32-S3 WROOM, por confirmar)

Va enchufada en la [placa Freenove Breakout](../placa-breakout-freenove/README.md). Freenove muestra dos
placas S3 compatibles: **ESP32-S3 WROOM** (con conector de cámara y dos USB-C) y **ESP32-S3 WROOM Lite**.
Falta confirmar cuál tenemos y su memoria (p. ej. N8R8 o N16R8, viene grabado en el módulo).

| ESP32-S3 WROOM | ESP32-S3 WROOM Lite |
| --- | --- |
| ![S3 WROOM](terceros/freenove-esp32-s3-wroom-en-breakout.png) | ![S3 WROOM Lite](terceros/freenove-esp32-s3-wroom-lite-en-breakout.png) |

## Pines a evitar (ESP32-S3 en general)

| GPIO | Por qué |
| --- | --- |
| 0, 3, 45, 46 | Pines de arranque (strapping): definen el modo de arranque |
| 19, 20 | USB nativo (D− / D+) |
| 26–32 | Memoria flash interna |
| 33–37 | PSRAM octal en módulos R8 (N8R8, N16R8): **no usar** aunque salgan en la placa |
| 43, 44 | UART0 (TX/RX del monitor serie) |
| 48 | LED RGB de la placa Freenove |
| 4–18 | Bus de la cámara en la Freenove WROOM: libres solo si no se conecta cámara (el robot no la usa) |

Para leer voltajes de batería usar **ADC1** (GPIO 1–10): el ADC2 se bloquea con el radio activo.

## Asignación propuesta (por confirmar con la placa real)

| Función | GPIO | Notas |
| --- | --- | --- |
| L298N ENA (PWM motor izquierdo) | 4 | PWM con LEDC |
| L298N IN1 | 5 | |
| L298N IN2 | 6 | |
| L298N ENB (PWM motor derecho) | 7 | PWM con LEDC |
| L298N IN3 | 15 | |
| L298N IN4 | 16 | |
| Relevador del arma | 21 | No es de arranque; arranca en bajo (arma apagada) |
| Voltaje batería 3S (divisor) | 1 | ADC1 |
| Voltaje batería 5S (divisor) | 2 | ADC1 |
| Voltaje pila 9 V (divisor) | 8 | ADC1 |
| Servo del martillo (MG995) | 9 | PWM de 50 Hz con LEDC |

Detalle de conexiones en [arquitectura-electrica.md](../../../docs/electronica/arquitectura-electrica.md).

## Por recabar

- [ ] Modelo exacto de la placa y memoria (foto de ambas caras).
- [ ] Peso.
- [ ] Confirmar en la placa real que el GPIO 21 queda en bajo al arrancar (medir con multímetro).

## Fuentes

Todas descargadas el 2026-11-15.

| Archivo | Página de origen | Imagen original |
| --- | --- | --- |
| `terceros/freenove-esp32-s3-wroom-en-breakout.png` | [Freenove FNK0101, cap. 2: ESP32](https://docs.freenove.com/projects/fnk0101/en/latest/fnk0101/codes/tutorial/2_ESP32.html) | [Chapter02_03.png](https://docs.freenove.com/projects/fnk0101/en/latest/_images/Chapter02_03.png) |
| `terceros/freenove-esp32-s3-wroom-lite-en-breakout.png` | [Freenove FNK0101, cap. 2: ESP32](https://docs.freenove.com/projects/fnk0101/en/latest/fnk0101/codes/tutorial/2_ESP32.html) | [Chapter02_02.png](https://docs.freenove.com/projects/fnk0101/en/latest/_images/Chapter02_02.png) |

Otras páginas consultadas: [Espressif, hoja de datos del ESP32-S3 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)
(pines de arranque, flash/PSRAM, USB y ADC).
