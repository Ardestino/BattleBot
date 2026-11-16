# Control Xbox Series X

No va montado en el robot, así que no se modela. Se registra para el firmware.

- Se conecta por Bluetooth LE al ESP32-S3 (el S3 no tiene Bluetooth clásico).
- Biblioteca prevista: Bluepad32, con lista de direcciones MAC permitidas.
- Failsafe: si se pierde la señal ~300 ms, se detienen motores y se apaga el arma.

## Por recabar

- [ ] Número de modelo (en la etiqueta dentro del compartimento de pilas; el Series X|S es el 1914).
- [ ] Dirección MAC del control (para la lista de permitidos; va en `firmware/include/secrets.h`).
- [ ] Versión de firmware del control (actualizar desde la app Xbox Accessories si falla el emparejamiento).
