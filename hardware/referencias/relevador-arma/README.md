# Relevador del arma

Enciende y apaga el motor de la podadora (24 V nominal) con la batería 5S (18–21 V). Modelo **por
definir**: esta ficha junta lo que tiene que cumplir para no fallar.

## Requisitos

| Requisito | Valor | Por qué |
| --- | --- | --- |
| Contacto | Normalmente abierto (NO) | Sin señal, el arma queda apagada (failsafe) |
| Corriente del contacto | Mayor que el **arranque** del motor del arma, no solo su corriente normal | Un motor de podadora puede pedir decenas de amperes al arrancar; un relevador chico se suelda (queda pegado encendido) |
| Voltaje del contacto | Especificado para **CD** a ≥ 24 V | Los valores de CA (p. ej. "10 A 250 VAC") no aplican a CD: en CD el arco dura más |
| Bobina | 12 V (desde la 3S) o 5 V, activada con transistor o módulo con optoacoplador | El ESP32 da 3.3 V y ~20 mA: no mueve una bobina directo |
| Lógica | Activo en alto, o un módulo que no se active si el pin flota al arrancar | Muchos módulos chinos son activo en bajo y prenden el relevador durante el arranque |
| Diodo | Diodo de rueda libre en la bobina y otro, de potencia, en paralelo con el motor | Protege al transistor y reduce el arco en el contacto |

Opciones típicas: relevador automotriz de 12 V 40 A (tipo Bosch, 4 o 5 terminales) con transistor, o un
contactor de CD. Los módulos azules de 5 V "10 A" (SRD-05VDC-SL-C) **no** son suficientes para este motor.

## Seguridad que exige el reglamento

- Interruptor del arma separado (conector o llave removible) en serie con la batería 5S, antes del relevador.
- Failsafe: si se pierde la señal del control, el firmware apaga el relevador (≈300 ms).
- Fusible en la línea de la 5S.

Ver [arquitectura-electrica.md](../../../docs/electronica/arquitectura-electrica.md) y el
[reglamento](../../../docs/reglamento.md).

## Por recabar

- [ ] Modelo del relevador que tenemos (foto de la etiqueta): corriente y voltaje del contacto, voltaje de bobina.
- [ ] Corriente de arranque del motor del arma (con pinza amperimétrica de CD o estimada con la resistencia del devanado: I ≈ V / R).
