# Firmware

Firmware del ESP32-S3 con [PlatformIO](https://platformio.org/).

## Requisitos de seguridad (reglamento)

- **Failsafe:** si se pierde el control o pasan más de ~300 ms sin datos, motores a cero y arma apagada.
- **Arranque seguro:** el pin del relevador del arma debe quedar en bajo al encender
  (resistencia de 10 kΩ a tierra; evita GPIO 0, 3, 45 y 46).
- **Arma armada por software:** combinación de botones para armar; al reconectar el control queda desarmada.
- **Watchdog:** si el programa se cuelga, el ESP32 se reinicia con todo apagado.

## Primeros pasos

1. Copia `include/secrets.example.h` como `include/secrets.h` y pon la MAC de tu control.
2. `pio run` para compilar y `pio run -t upload` para subirlo.
