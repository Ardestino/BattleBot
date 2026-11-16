# Referencias de componentes

Una carpeta por componente que ya tenemos. Antes de modelar una pieza que toque a un componente,
su ficha debe tener las medidas confirmadas con calibrador.

Cada carpeta lleva:

- `README.md`: ficha con medidas, datos eléctricos, fuentes y lista de lo que falta medir.
- `fotos/`: fotos propias (se suben al repositorio). Conviene fotografiar junto a una regla o un calibrador.
- `terceros/`: planos, hojas de datos e imágenes de vendedores. **No se suben** (están en `.gitignore`)
  porque son contenido de terceros. La sección **Fuentes** de cada ficha tiene una tabla con la página
  de origen y el enlace a la imagen original de cada archivo, para poder volver a descargarlos.

## Estado

| Componente | Carpeta | Estado de la información |
| --- | --- | --- |
| Motorreductor de tracción JGB37-520, 12 V 333 RPM | [motor-traccion-jgb37-520](motor-traccion-jgb37-520/README.md) | 2 motores con bracket Talos; plano del motor descargado; falta medir motor y bracket |
| Rueda de goma ~65 mm, rin amarillo | [rueda-goma-65mm](rueda-goma-65mm/README.md) | Posiblemente ya no se use (orugas); por decidir |
| Kit de ruedas mecanum | — | **Descartado**: se usarán orugas triangulares impresas ([diseño](../../docs/diseno/orugas-triangulares.md)) |
| Motor del arma: desbrozadora 21 V + hoja de 6" | [motor-arma-desbrozadora](motor-arma-desbrozadora/README.md) | Motor 775 de 20 V con plano de medidas; falta medir barrenos de la cara y la hoja |
| Motor de podadora 24 V | [motor-arma-podadora](motor-arma-podadora/README.md) | Reemplazado por el de la desbrozadora |
| Baterías 3S y 5S (celdas de taladro) | [baterias](baterias/README.md) | Sin medir |
| Placa ESP32-S3 (Freenove S3 WROOM, por confirmar) | [esp32-s3](esp32-s3/README.md) | Pines a evitar y asignación propuesta; falta confirmar modelo |
| Placa de expansión Freenove Breakout (FNK0101) | [placa-breakout-freenove](placa-breakout-freenove/README.md) | Documentación de Freenove descargada; falta medir y pesar |
| Driver de motores L298N | [driver-l298n](driver-l298n/README.md) | Datos de ST y del módulo; falta medir |
| Relevador del arma | [relevador-arma](relevador-arma/README.md) | Modelo por definir; requisitos listos |
| Rodamientos de la ferretería | [rodamientos](rodamientos/README.md) | Tabla con medidas estándar; elegidos 606 (tensoras) y 6201 (arma) |
| Monito del logotipo del CETI (martillo) | [logo-ceti](logo-ceti/README.md) | STL de referencia del usuario; logotipo del CETI (no publicar sin permiso) |
| Control Xbox Series X | [control-xbox](control-xbox/README.md) | No va en el robot; solo datos de conexión |

Las conexiones entre componentes están en [arquitectura-electrica.md](../../docs/electronica/arquitectura-electrica.md).

## Herramientas para medir

Calibrador (vernier), báscula de cocina con resolución de 1 g, multímetro y, si se puede,
una fuente de laboratorio con limitador de corriente para medir la corriente de bloqueo de los motores.
