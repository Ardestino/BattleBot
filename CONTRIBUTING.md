# Cómo contribuir

## Flujo de trabajo

1. Crea una rama desde `main` con un nombre descriptivo: `cad/soporte-motor`, `firmware/failsafe`, `docs/ensamble`.
2. Haz commits pequeños con mensajes claros en español: `cad: aligera placa base a 3 mm`.
3. Abre un pull request y describe qué cambiaste y cómo lo probaste.

## Convenciones por carpeta

### CAD (`hardware/cad/`)
- Los archivos originales van en `source/`; cada pieza terminada se exporta también a STEP en `step/`.
- Nombres en minúsculas con guiones y número de versión: `placa-base-v2.SLDPRT`, `placa-base-v2.step`.
- Cada pieza nueva se agrega a `hardware/bom/bom.csv` con su peso.

### Impresión y corte (`hardware/print/`, `hardware/cut/`)
- Junto a cada STL/3MF anota material, relleno, paredes y orientación en `hardware/print/README.md`.
- Los DXF de corte indican material y espesor en el nombre: `placa-base-al6061-3mm.dxf`.

### Firmware (`firmware/`)
- Proyecto PlatformIO. Antes de abrir un PR, compila con `pio run`.
- Nunca subas la MAC de tu control ni contraseñas: usa `firmware/include/secrets.h` (ignorado por git)
  a partir de `secrets.example.h`.
- Cualquier cambio en el control del arma debe conservar el failsafe y el arranque con el arma apagada.

## Archivos pesados

Los formatos CAD, STL y video se guardan con **Git LFS** (ver `.gitattributes`).
Instálalo una vez con `git lfs install` antes de clonar o hacer commits.
