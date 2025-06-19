# Atrapa las Estrellitas

Atrapa las Estrellitas es un juego arcade avanzado en Python (Pygame) donde controlas una nave espacial para atrapar estrellas, evitar bombas y dispararles. Incluye tienda, mejoras, powerups, sistema de monedas, guardado de progreso y una interfaz visual responsiva y profesional.

## Características principales
- Menú principal con botones y selección de dificultad (Fácil, Medio, Difícil)
- Tienda de mejoras con monedas y niveles (ver tabla de mejoras abajo)
- Powerups aleatorios: disparo barrido, imán temporal, triple disparo, caja de salud
- Sistema de monedas: los puntos se convierten en monedas para comprar mejoras
- Guardado automático de progreso (monedas y mejoras) en `progreso.json`
- Interfaz y HUD completamente responsivos al tamaño de ventana
- Sonidos de 8 bits para todos los eventos clave
- Fondo animado y visuales atractivos
- Pantalla de Game Over con opciones y botones

## Tabla de mejoras disponibles en la tienda

| Mejora           | Efecto principal                                      | Nivel máximo | Precio inicial |
|------------------|------------------------------------------------------|--------------|---------------|
| Velocidad        | Aumenta la velocidad de la nave                      | 10           | 30            |
| Vida máxima      | Aumenta la cantidad máxima de vidas                  | 10           | 50            |
| Recarga          | Disminuye el tiempo de recarga de munición           | 1 (mejora única) | 40        |
| Munición máxima  | Aumenta la cantidad máxima de balas                  | 10           | 40            |
| Escudo           | Añade escudos para protegerte de bombas              | 10           | 60            |
| Disparo ancho    | Permite disparos más anchos                          | 1            | 50            |
| Penetrante       | Disparos atraviesan bombas                           | 1            | 70            |
| Imán permanente  | Las estrellas se acercan automáticamente             | 1            | 100           |
| Auto-disparo     | Dispara automáticamente                              | 1            | 120           |

## Powerups aleatorios
- **Disparo barrido**: Dispara en todas las direcciones por un instante.
- **Imán temporal**: Las estrellas se acercan a la nave durante unos segundos.
- **Triple disparo**: Permite disparar tres balas a la vez temporalmente.
- **Caja de salud**: Recupera vidas al recogerla.

## Guardado de progreso
El juego guarda automáticamente tus monedas y mejoras en `src/progreso.json` al comprar, salir o cerrar el juego. ¡No perderás tu avance!

## Estructura del proyecto
```
atrapa-las-estrellitas/
├── README.md
├── tutorial.md
├── src/
│   ├── juego.py
│   ├── Fondo.png
│   ├── sonido_estrella.wav
│   ├── sonido_bomba.wav
│   ├── sonido_fondo.wav
│   ├── sonido_gameover.wav
│   ├── sonido_disparo.wav
│   ├── sonido_explosion.wav
│   └── progreso.json
├── Ico/
│   └── a.png
├── Logo/
│   └── Logo.png
├── AtrapaLasEstrellitas.spec
└── build.bat
```

## Requisitos
- Python 3.8+
- Pygame (`pip install pygame`)

## Compilación para Windows
1. Instala PyInstaller: `pip install pyinstaller`
2. Ejecuta `build.bat` para generar el instalador ejecutable.

## Créditos
- Código y arte: GitHub Copilot + usuario
- Sonidos: libres de derechos o incluidos