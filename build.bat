@echo off
REM Compila el juego en modo carpeta (onedir) y prepara el instalador profesional
cd /d %~dp0
cd atrapA-las-estrellitas
pyinstaller --clean --noconfirm AtrapaLasEstrellitas.spec
cd ..
echo.
echo Para crear el instalador profesional, abre 'atrapa-las-estrellitas\instalador.iss' con Inno Setup y presiona F9 para previsualizar la pantalla de instalación antes de compilar.
echo El instalador desplegará todos los archivos y dependencias en la ruta que el usuario elija.
echo.
pause
