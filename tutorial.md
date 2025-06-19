# Tutorial: Crea tu propio juego "Atrapa las Estrellitas" en Python

Este tutorial te guía paso a paso para crear un juego arcade avanzado con nave, disparos, tienda, mejoras, powerups, monedas y guardado de progreso. ¡Ideal para principiantes y quienes quieren aprender a hacer un juego completo y profesional!

## 1. Instalación de Python y Pygame

1. Descarga e instala Python desde [python.org](https://www.python.org/downloads/).
2. Abre la terminal (CMD) y ejecuta:
   ```sh
   pip install pygame
   ```

## 2. Descarga los archivos del juego

- Descarga los archivos de este repositorio o crea la siguiente estructura:

```
atrapa-las-estrellitas/
├── tutorial.md
├── README.md
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

## 3. Explicación del juego y mecánicas

- El archivo `juego.py` contiene todo el código del juego.
- El juego inicia con un menú donde eliges la dificultad o entras a la tienda.
- Controlas una nave espacial con las flechas y disparas con ESPACIO.
- Puedes comprar mejoras permanentes en la tienda usando monedas (que ganas jugando).
- Hay powerups aleatorios: disparo barrido, imán, triple disparo, caja de salud.
- El progreso (monedas y mejoras) se guarda automáticamente en `progreso.json`.
- El HUD y la interfaz se adaptan al tamaño de la ventana.
- El fondo es una imagen espacial atractiva.
- Pantalla de Game Over con botones para reintentar o salir.

### Tabla de mejoras disponibles en la tienda

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

### Powerups aleatorios
- **Disparo barrido**: Dispara en todas las direcciones por un instante.
- **Imán temporal**: Las estrellas se acercan a la nave durante unos segundos.
- **Triple disparo**: Permite disparar tres balas a la vez temporalmente.
- **Caja de salud**: Recupera vidas al recogerla.

### Notas adicionales
- El progreso se guarda automáticamente al comprar, salir o cerrar el juego.
- Los puntos obtenidos en cada partida se suman como monedas para gastar en la tienda.
- El HUD y la interfaz se adaptan automáticamente al tamaño de la ventana.
- Puedes usar el teclado o el mouse para navegar por los menús y la tienda.

## 4. Ejecutar el juego

1. Abre una terminal en la carpeta `src`.
2. Ejecuta:
   ```sh
   python juego.py
   ```
3. Selecciona dificultad o tienda con flechas/mouse y presiona Enter o haz clic.
4. ¡Juega, mejora tu nave y no pierdas tu progreso!

## 5. Compilar un instalador para Windows

1. Instala PyInstaller: `pip install pyinstaller`
2. Ejecuta el archivo `build.bat` en la raíz del proyecto.
3. El ejecutable estará en la carpeta `dist`.

## 6. Personaliza tu juego

- Cambia los sonidos reemplazando los archivos `.wav`.
- Modifica colores, velocidad, cantidad de estrellas/bombas, o agrega nuevos powerups en el código.
- Cambia la imagen de fondo por otra espacial si lo deseas.

## 7. Solución de problemas

- Si el juego no inicia, asegúrate de tener Python y Pygame instalados.
- Si no hay sonido, revisa que los archivos `.wav` estén en la carpeta `src`.
- Si tienes dudas, revisa el archivo `README.md` para más detalles.

---
¡Listo! Ahora tienes un juego arcade profesional en Python, con tienda, mejoras, guardado y todo lo necesario para aprender y divertirte.