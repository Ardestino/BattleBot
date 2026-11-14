# Instrucciones para el asistente

Robot de combate de 3 kg para BotCrash CETI 2026A. El reglamento resumido está en `docs/reglamento.md`:
todo diseño debe cumplirlo (≤ 3 kg, ≤ 300 mm por lado, interruptor general, interruptor del arma,
failsafe y seguro mecánico del arma).

- Documentación y mensajes de commit en español.
- CAD: originales en `hardware/cad/source/`, exportados STEP en `hardware/cad/step/`, conceptos en
  `hardware/cad/concepts/`, imágenes en `hardware/cad/renders/`. Cada pieza nueva va en `hardware/bom/bom.csv` con su peso.
- Diseña piezas mecánicas reales (placas aligeradas, soportes de motor, rodamientos, tornillería, redondeos),
  no figuras de prueba hechas con primitivas.
- Firmware: PlatformIO para ESP32-S3 en `firmware/`. Los secretos van en `firmware/include/secrets.h`, que no se sube.
- No publiques contenido de terceros sin permiso (por ejemplo el PDF del reglamento) ni personajes con derechos de autor.
