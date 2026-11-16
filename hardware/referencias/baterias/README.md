# Baterías

Tres fuentes separadas (decisión del 2026-11-16):

| Fuente | Celdas | Voltaje | Alimenta |
| --- | --- | --- | --- |
| Paquete 3S | 3 × 18650 en serie (3S1P), BMS personalizado | 11.1 V nominal, 12.6 V cargada, ≈ 9 V vacía | L298N y motores de tracción; bobina del relevador |
| Paquete 5S | 5 × 18650 en serie (5S1P), BMS personalizado | 18.5 V nominal, 21 V cargada, ≈ 15 V vacía | Motor 775 de 20 V del arma (a través del relevador) |
| Pila cuadrada de 9 V | 6LR61 (alcalina) o recargable de 9 V | 9 V | Freenove Breakout → ESP32-S3, lógica del L298N |

## Medidas y peso usados en el CAD

| | Medidas | Peso | Cómo se calculó |
| --- | --- | --- | --- |
| Celda 18650 | Ø18.6 × 65.2 mm (con forro) | ≈ 46 g | Típico de celdas de alta descarga |
| Paquete 3S1P | 68 × 58 × 21 mm (celdas acostadas, lado a lado) | ≈ 155 g | 3 celdas + BMS, níquel, cables y forro |
| Paquete 5S1P | 68 × 95 × 21 mm | ≈ 250 g | 5 celdas + BMS, níquel, cables y forro |
| Pila de 9 V | 48.5 × 26.5 × 17.5 mm | ≈ 45 g (alcalina), ≈ 30 g (recargable) | Medidas estándar 6LR61 |

En el robot van apiladas al centro (la 3S abajo, la 5S arriba), entre los motores de tracción y el motor del
arma; la pila de 9 V va en un porta pila impreso sobre la cubierta de electrónica.

## Puntos a revisar

- **Celdas**: confirmar modelo y corriente máxima de descarga (viene impreso en el forro; las de taladro
  suelen ser de 15–30 A). El arranque del 775 puede pedir varias decenas de amperes por un instante.
- **BMS del arma**: si el BMS corta por sobrecorriente en el arranque del 775, el arma se apaga sola.
  En robots de combate es común que el BMS solo balancee y proteja la carga, y que la descarga vaya
  directa con un fusible. Definir la corriente de corte del BMS personalizado.
- **Pila de 9 V para el ESP32**:
  - Ventaja: el ESP32 queda aislado del ruido y de las caídas de voltaje de los motores.
  - Duración: el ESP32-S3 con Bluetooth y la Freenove consumen ≈ 100–250 mA; una alcalina de 9 V da
    ≈ 250–400 mAh a esa corriente: ≈ 1–2 h. Alcanza para varios combates de 3 min, pero hay que llevar
    pilas de repuesto y cambiarla antes de cada combate (o usar una recargable de 9 V).
  - El broche de la pila puede soltarse con un golpe y reiniciar el ESP32 (el robot se detiene por el
    failsafe). El porta pila del CAD la sujeta con un cincho; usar un broche de buena calidad.
  - La Freenove acepta 9 V en su jack (rango de 5–12 V según la guía).
- **Interruptor general**: con dos fuentes en el lado de control (3S y 9 V), el interruptor general debe
  cortar las dos a la vez: usar un interruptor de doble polo (DPST) o un conector de seguridad con dos
  circuitos. El de la 5S (arma) sigue siendo independiente.
- **Tierra común**: unir el negativo de la pila de 9 V con el de la 3S, para que el ESP32 pueda mandar
  señales al L298N y al relevador.

## Por medir

- [ ] Modelo, capacidad (mAh) y corriente de descarga de las celdas.
- [ ] Medidas y peso de cada paquete armado.
- [ ] Corriente de corte del BMS personalizado (carga y descarga).
- [ ] Tipo de conector de cada paquete.
- [ ] Consumo real del ESP32 + Freenove con el control conectado (multímetro en serie con la pila).
