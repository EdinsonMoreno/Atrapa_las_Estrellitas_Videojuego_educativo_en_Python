import pygame
import random
import json
import os
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla (ahora responsivas)
def ajustar_dimensiones():
    global ANCHO, ALTO, pantalla
    info = pygame.display.Info()
    ANCHO = int(info.current_w * 0.8)
    ALTO = int(info.current_h * 0.8)
    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)

ajustar_dimensiones()
pygame.display.set_caption("Atrapa las Estrellitas")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)

# Reloj
reloj = pygame.time.Clock()

# Fuente
fuente = pygame.font.SysFont("Arial", 30)

# Función para cargar recursos (sonidos, imágenes) correctamente en desarrollo y en EXE
def recurso_path(relpath):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relpath)
    return os.path.join(os.path.dirname(__file__), relpath)

# Cargar sonidos (usar recurso_path)
sonido_estrella = pygame.mixer.Sound(recurso_path('sonido_estrella.wav'))
sonido_bomba = pygame.mixer.Sound(recurso_path('sonido_bomba.wav'))
sonido_fondo = pygame.mixer.Sound(recurso_path('sonido_fondo.wav'))
sonido_gameover = pygame.mixer.Sound(recurso_path('sonido_gameover.wav'))
sonido_disparo = pygame.mixer.Sound(recurso_path('sonido_disparo.wav'))
sonido_explosion = pygame.mixer.Sound(recurso_path('sonido_explosion.wav'))

# Definir colores adicionales
AZUL = (0, 120, 255)
VERDE = (0, 200, 0)
GRIS = (50, 50, 50)

# Jugador (canasta)
canasta = pygame.Rect(350, 500, 100, 20)
velocidad_canasta = 10

# Estrellas
estrellas = []
for _ in range(5):
    x = random.randint(0, ANCHO - 30)
    y = random.randint(-600, -50)
    estrella = pygame.Rect(x, y, 30, 30)
    estrellas.append(estrella)

# Bombas
bombas = []
for _ in range(3):
    x = random.randint(0, ANCHO - 30)
    y = random.randint(-600, -50)
    bomba = pygame.Rect(x, y, 30, 30)
    bombas.append(bomba)

# Puntos y vidas
puntos = 0
vidas = 10  # Ahora la vida máxima es 10
max_vidas = 10

# Monedas y mejoras
monedas = 0
mejoras = {
    'velocidad': 1,      # Nivel de velocidad
    'vida_max': 10,      # Vida máxima
    'recarga': 2000,     # ms
    'municion_max': 9,   # Máx balas
    'escudo': 0,         # Escudos disponibles
    'disparo_ancho': 0,  # 0=normal, 1=ancho
    'penetrante': 0,     # 0=normal, 1=penetrante
    'iman_perm': 0,      # 0=normal, 1=imán permanente
    'auto': 0            # 0=manual, 1=auto
}
precios = {
    'velocidad': 30,
    'vida_max': 50,
    'recarga': 40,
    'municion_max': 40,
    'escudo': 60,
    'disparo_ancho': 50,
    'penetrante': 70,
    'iman_perm': 100,
    'auto': 120
}

# Ruta para guardar progreso
PROGRESO_PATH = os.path.join(os.path.dirname(__file__), 'progreso.json')

def guardar_progreso():
    global monedas, mejoras
    with open(PROGRESO_PATH, 'w', encoding='utf-8') as f:
        json.dump({'monedas': monedas, 'mejoras': mejoras}, f)

def cargar_progreso():
    global monedas, mejoras
    if os.path.exists(PROGRESO_PATH):
        with open(PROGRESO_PATH, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            monedas = datos.get('monedas', 0)
            mejoras.update(datos.get('mejoras', {}))

# Cargar progreso al inicio
cargar_progreso()

# Cargar imagen de fondo
fondo_img = pygame.image.load(recurso_path('Fondo.png'))
def dibujar_fondo():
    fondo_escalado = pygame.transform.scale(fondo_img, (ANCHO, ALTO))
    pantalla.blit(fondo_escalado, (0, 0))

# Powerups
class PowerUp:
    def __init__(self, tipo, x, y):
        self.tipo = tipo  # 'barrido', 'iman', 'triple', 'salud'
        self.rect = pygame.Rect(x, y, 32, 32)
        self.tiempo = pygame.time.get_ticks()
    def dibujar(self, pantalla):
        if self.tipo == 'barrido':
            pygame.draw.rect(pantalla, (255, 128, 0), self.rect)  # naranja
            pygame.draw.line(pantalla, BLANCO, (self.rect.centerx, self.rect.top), (self.rect.centerx, self.rect.bottom), 2)
        elif self.tipo == 'iman':
            pygame.draw.rect(pantalla, (0, 255, 255), self.rect)  # celeste
            pygame.draw.circle(pantalla, (0, 128, 255), self.rect.center, 10, 2)
        elif self.tipo == 'triple':
            pygame.draw.rect(pantalla, (255, 0, 255), self.rect)  # magenta
            pygame.draw.polygon(pantalla, BLANCO, [(self.rect.centerx, self.rect.top+5), (self.rect.left+5, self.rect.bottom-5), (self.rect.right-5, self.rect.bottom-5)])
        elif self.tipo == 'salud':
            pygame.draw.rect(pantalla, (0, 255, 0), self.rect)  # verde
            pygame.draw.line(pantalla, ROJO, (self.rect.centerx, self.rect.top+6), (self.rect.centerx, self.rect.bottom-6), 3)
            pygame.draw.line(pantalla, ROJO, (self.rect.left+6, self.rect.centery), (self.rect.right-6, self.rect.centery), 3)

# Utilidad para calcular proporciones responsivas

def prop_x(p):
    return int(ANCHO * p)

def prop_y(p):
    return int(ALTO * p)

# Botón clase para menús
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color, color_hover, accion=None):
        self.x, self.y, self.ancho, self.alto = x, y, ancho, alto
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.accion = accion
        self.rect = pygame.Rect(x, y, ancho, alto)
    def actualizar(self):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
    def dibujar(self, pantalla, fuente):
        self.actualizar()
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(pantalla, self.color_hover, self.rect, border_radius=10)
        else:
            pygame.draw.rect(pantalla, self.color, self.rect, border_radius=10)
        texto = fuente.render(self.texto, True, BLANCO)
        pantalla.blit(texto, (self.rect.x + (self.rect.width - texto.get_width()) // 2, self.rect.y + (self.rect.height - texto.get_height()) // 2))
    def click(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos):
            if self.accion:
                self.accion()

# Nueva barra segmentada para mejoras

def dibujar_barra_mejora(pantalla, x, y, ancho, alto, nivel, max_nivel, color, color_fondo):
    segmento = (ancho - 2) // max_nivel
    for i in range(max_nivel):
        rect = pygame.Rect(x+1+i*segmento, y+1, segmento-2, alto-2)
        pygame.draw.rect(pantalla, color_fondo, rect)
        if i < nivel:
            pygame.draw.rect(pantalla, color, rect)
    borde = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, BLANCO, borde, 2)

# Menú principal y selección de dificultad

def menu_principal():
    seleccion = ["Fácil", "Medio", "Difícil", "Tienda"]
    dificultad = [5, 8, 12, None]
    seleccionada = 0
    botones = []
    fuente_menu = pygame.font.SysFont("Arial", 40)
    jugando = True
    while jugando:
        dibujar_fondo()
        titulo = fuente_menu.render("Atrapa las Estrellitas", True, AMARILLO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 80))
        botones.clear()
        for i, nivel in enumerate(seleccion):
            x_boton = prop_x(0.5) - prop_x(0.12)
            y_boton = prop_y(0.28) + i*prop_y(0.11)
            ancho_boton = prop_x(0.24)
            alto_boton = prop_y(0.08)
            color = VERDE if i == seleccionada else AZUL
            boton = Boton(x_boton, y_boton, ancho_boton, alto_boton, nivel, color, ROJO, accion=None)
            boton.dibujar(pantalla, fuente_menu)
            botones.append(boton)
        instrucciones = fuente.render("←/→/↑/↓: mover nave | ESPACIO: disparar | Evita bombas", True, BLANCO)
        pantalla.blit(instrucciones, (prop_x(0.5) - instrucciones.get_width()//2, prop_y(0.8)))
        instrucciones2 = fuente.render("Munición limitada, se recarga sola. Haz clic o ENTER para elegir.", True, BLANCO)
        pantalla.blit(instrucciones2, (prop_x(0.5) - instrucciones2.get_width()//2, prop_y(0.85)))
        texto_monedas = fuente.render(f"Monedas: {monedas}", True, AMARILLO)
        pantalla.blit(texto_monedas, (ANCHO-prop_x(0.18), prop_y(0.03)))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccionada = (seleccionada - 1) % len(seleccion)
                if evento.key == pygame.K_DOWN:
                    seleccionada = (seleccionada + 1) % len(seleccion)
                if evento.key == pygame.K_RETURN:
                    if seleccionada == 3:
                        pantalla_tienda()
                    else:
                        return dificultad[seleccionada]
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, boton in enumerate(botones):
                    if boton.rect.collidepoint(evento.pos):
                        if i == 3:
                            pantalla_tienda()
                        else:
                            return dificultad[i]
        pygame.display.flip()
        reloj.tick(30)

# Tienda con botones y barras segmentadas

def pantalla_tienda():
    global mejoras, monedas, max_vidas, max_municiones, recarga_intervalo
    global ANCHO, ALTO, pantalla
    while True:
        dibujar_fondo()
        fuente_tienda = pygame.font.SysFont("Arial", max(18, int(ALTO*0.035)))
        opciones = list(mejoras.keys())
        seleccion = 0
        botones = []
        while True:
            dibujar_fondo()
            titulo = fuente_tienda.render("TIENDA DE MEJORAS", True, AMARILLO)
            pantalla.blit(titulo, (prop_x(0.5) - titulo.get_width()//2, prop_y(0.05)))
            texto_monedas = fuente_tienda.render(f"Monedas: {monedas}", True, BLANCO)
            pantalla.blit(texto_monedas, (prop_x(0.5) - texto_monedas.get_width()//2, prop_y(0.12)))
            botones.clear()
            for i, op in enumerate(opciones):
                y = prop_y(0.18) + i*prop_y(0.08)
                ancho_boton = prop_x(0.18)
                alto_boton = prop_y(0.06)
                x_boton = prop_x(0.12)
                color = VERDE if i == seleccion else AZUL
                boton = Boton(x_boton, y, ancho_boton, alto_boton, "Comprar", color, ROJO)
                boton.dibujar(pantalla, fuente_tienda)
                botones.append(boton)
                # Nombre y descripción
                nombre = op.replace('_', ' ').upper()
                nivel = mejoras[op]
                max_nivel = 10 if op not in ['recarga', 'auto', 'iman_perm', 'disparo_ancho', 'penetrante'] else 1
                precio = precios[op]
                desc = f"Nivel: {nivel}" if max_nivel > 1 else ("Activado" if nivel else "Desactivado")
                txt = fuente_tienda.render(f"{nombre} - {desc} - {precio} monedas", True, BLANCO)
                pantalla.blit(txt, (x_boton + ancho_boton + 20, y + alto_boton//4))
                # Barra de mejora
                dibujar_barra_mejora(pantalla, x_boton + ancho_boton + 350, y + 5, prop_x(0.18), alto_boton-10, nivel, max_nivel, VERDE, GRIS)
            instrucciones = fuente_tienda.render("↑/↓: seleccionar | ENTER/Click: comprar | ESC: salir", True, BLANCO)
            pantalla.blit(instrucciones, (prop_x(0.5) - instrucciones.get_width()//2, prop_y(0.92)))
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.VIDEORESIZE:
                    ANCHO, ALTO = evento.w, evento.h
                    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones)
                    if evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones)
                    if evento.key == pygame.K_RETURN:
                        op = opciones[seleccion]
                        if monedas >= precios[op]:
                            monedas -= precios[op]
                            if op == 'velocidad':
                                mejoras['velocidad'] += 1
                            elif op == 'vida_max':
                                mejoras['vida_max'] += 1
                                max_vidas = mejoras['vida_max']
                            elif op == 'recarga':
                                mejoras['recarga'] = max(500, mejoras['recarga'] - 200)
                                recarga_intervalo = mejoras['recarga']
                            elif op == 'municion_max':
                                mejoras['municion_max'] += 1
                                max_municiones = mejoras['municion_max']
                            elif op == 'escudo':
                                mejoras['escudo'] += 1
                            else:
                                mejoras[op] = 1
                            guardar_progreso()
                    if evento.key == pygame.K_ESCAPE:
                        guardar_progreso()
                        return
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for i, boton in enumerate(botones):
                        if boton.rect.collidepoint(evento.pos):
                            op = opciones[i]
                            if monedas >= precios[op]:
                                monedas -= precios[op]
                                if op == 'velocidad':
                                    mejoras['velocidad'] += 1
                                elif op == 'vida_max':
                                    mejoras['vida_max'] += 1
                                    max_vidas = mejoras['vida_max']
                                elif op == 'recarga':
                                    mejoras['recarga'] = max(500, mejoras['recarga'] - 200)
                                    recarga_intervalo = mejoras['recarga']
                                elif op == 'municion_max':
                                    mejoras['municion_max'] += 1
                                    max_municiones = mejoras['municion_max']
                                elif op == 'escudo':
                                    mejoras['escudo'] += 1
                                else:
                                    mejoras[op] = 1
                                guardar_progreso()
            pygame.display.flip()
            reloj.tick(30)

# Juego principal mejorado

def juego(dificultad):
    global ANCHO, ALTO, pantalla
    global monedas, max_vidas, max_municiones, recarga_intervalo, velocidad_canasta
    # Inicialización de variables
    estrellas = []
    for _ in range(5):
        x = random.randint(0, ANCHO - 30)
        y = random.randint(-600, -50)
        estrella = pygame.Rect(x, y, 30, 30)
        estrellas.append(estrella)
    bombas = []
    for _ in range(3):
        x = random.randint(0, ANCHO - 30)
        y = random.randint(-600, -50)
        bomba = pygame.Rect(x, y, 30, 30)
        bombas.append(bomba)
    puntos = 0
    vidas = 10
    nave = pygame.Rect(ANCHO//2-ANCHO//32, int(ALTO*0.8), ANCHO//16, ALTO//10)
    disparos = []
    municiones = 9
    max_municiones = 9
    tiempo_recarga = 0
    recarga_intervalo = 2000  # ms
    ultimo_recarga = pygame.time.get_ticks()
    powerups = []
    powerup_activo = {'barrido': False, 'iman': False, 'triple': False}
    powerup_tiempo = {'barrido': 0, 'iman': 0, 'triple': 0}
    powerup_duracion = 6000  # ms
    tiempo_ultimo_powerup = pygame.time.get_ticks()
    powerup_intervalo = 7000  # ms
    jugando = True
    pygame.mixer.Sound.play(sonido_fondo, loops=-1)
    velocidad_canasta = 10 * mejoras['velocidad']
    max_vidas = mejoras['vida_max']
    max_municiones = mejoras['municion_max']
    recarga_intervalo = mejoras['recarga']
    while jugando:
        dibujar_fondo()
        ahora = pygame.time.get_ticks()
        # Aparición aleatoria de powerups
        if ahora - tiempo_ultimo_powerup > powerup_intervalo:
            tipo = random.choice(['barrido', 'iman', 'triple', 'salud'])
            x = random.randint(40, ANCHO-72)
            y = random.randint(40, ALTO-200)
            powerups.append(PowerUp(tipo, x, y))
            tiempo_ultimo_powerup = ahora
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.VIDEORESIZE:
                ANCHO, ALTO = evento.w, evento.h
                pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and municiones > 0:
                    if powerup_activo['triple']:
                        for angulo in [-0.3, 0, 0.3]:
                            disparos.append(Disparo(nave.x, nave.y, angulo))
                        municiones -= 1
                    else:
                        disparos.append(Disparo(nave.x, nave.y, 0))
                        municiones -= 1
                    pygame.mixer.Sound.play(sonido_disparo)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave.left > 0:
            nave.x -= velocidad_canasta
        if teclas[pygame.K_RIGHT] and nave.right < ANCHO:
            nave.x += velocidad_canasta
        if teclas[pygame.K_UP] and nave.top > 0:
            nave.y -= velocidad_canasta
        if teclas[pygame.K_DOWN] and nave.bottom < ALTO:
            nave.y += velocidad_canasta
        # Recarga de municiones
        if municiones < max_municiones and ahora - ultimo_recarga > recarga_intervalo:
            municiones += 1
            ultimo_recarga = ahora
        # Powerup: iman
        if powerup_activo['iman'] and ahora - powerup_tiempo['iman'] < powerup_duracion:
            for estrella in estrellas:
                if estrella.y < nave.y:
                    if estrella.x < nave.x:
                        estrella.x += 2
                    elif estrella.x > nave.x:
                        estrella.x -= 2
        else:
            powerup_activo['iman'] = False
        # Mover y dibujar disparos
        for disparo in disparos[:]:
            disparo.mover()
            if disparo.rect.y < -20 or disparo.rect.x < 0 or disparo.rect.x > ANCHO:
                disparos.remove(disparo)
        # Mover estrellas
        for estrella in estrellas:
            estrella.y += dificultad
            if estrella.colliderect(nave):
                puntos += 1
                pygame.mixer.Sound.play(sonido_estrella)
                estrella.y = random.randint(-600, -50)
                estrella.x = random.randint(0, ANCHO - 30)
            elif estrella.y > ALTO:
                estrella.y = random.randint(-600, -50)
                estrella.x = random.randint(0, ANCHO - 30)
        # Mover bombas
        for bomba in bombas[:]:
            bomba.y += dificultad + 1
            if bomba.colliderect(nave):
                vidas -= 1
                pygame.mixer.Sound.play(sonido_bomba)
                bomba.y = random.randint(-600, -50)
                bomba.x = random.randint(0, ANCHO - 30)
            elif bomba.y > ALTO:
                bomba.y = random.randint(-600, -50)
                bomba.x = random.randint(0, ANCHO - 30)
            # Colisión disparo-bomba
            for disparo in disparos[:]:
                if bomba.colliderect(disparo.rect):
                    pygame.mixer.Sound.play(sonido_explosion)
                    if disparo in disparos:
                        disparos.remove(disparo)
                    bomba.y = random.randint(-600, -50)
                    bomba.x = random.randint(0, ANCHO - 30)
        # Powerups: colisión y efectos
        for powerup in powerups[:]:
            if nave.colliderect(powerup.rect):
                if powerup.tipo == 'barrido':
                    powerup_activo['barrido'] = True
                    powerup_tiempo['barrido'] = ahora
                    # Disparos en todas direcciones
                    for ang in range(0, 360, 30):
                        rad = ang * 3.1416 / 180
                        disparos.append(Disparo(nave.x, nave.y, rad, especial=True))
                elif powerup.tipo == 'iman':
                    powerup_activo['iman'] = True
                    powerup_tiempo['iman'] = ahora
                elif powerup.tipo == 'triple':
                    powerup_activo['triple'] = True
                    powerup_tiempo['triple'] = ahora
                elif powerup.tipo == 'salud':
                    suma = random.randint(1, 5)
                    vidas = min(vidas + suma, max_vidas)
                powerups.remove(powerup)
        # Powerup: barrido
        if powerup_activo['barrido'] and ahora - powerup_tiempo['barrido'] < 800:
            # Destruir todas las bombas tocadas por disparos especiales
            for bomba in bombas:
                for disparo in disparos:
                    if hasattr(disparo, 'especial') and disparo.especial and bomba.colliderect(disparo.rect):
                        bomba.y = random.randint(-600, -50)
                        bomba.x = random.randint(0, ANCHO - 30)
        else:
            powerup_activo['barrido'] = False
        # Powerup: triple
        if powerup_activo['triple'] and ahora - powerup_tiempo['triple'] > powerup_duracion:
            powerup_activo['triple'] = False
        # Dibujar nave
        dibujar_nave(pantalla, nave.x, nave.y)
        # Dibujar disparos
        for disparo in disparos:
            disparo.dibujar(pantalla)
        # Dibujar estrellas
        for estrella in estrellas:
            dibujar_estrella(pantalla, estrella.x, estrella.y)
        # Dibujar bombas
        for bomba in bombas:
            dibujar_bomba(pantalla, bomba.x, bomba.y)
        # Dibujar powerups
        for powerup in powerups:
            powerup.dibujar(pantalla)
        # Dibujar barras de vida y munición
        dibujar_barra_segmentada(pantalla, 10, 10, 200, 20, vidas, max_vidas, ROJO, BLANCO, 'VIDA')
        dibujar_barra_segmentada(pantalla, 10, 40, 200, 20, municiones, max_municiones, AZUL, BLANCO, 'BALAS')
        # Dibujar puntuación
        texto = fuente.render(f"Puntos: {puntos}", True, BLANCO)
        pantalla.blit(texto, (10, 70))
        if vidas <= 0:
            jugando = False
        pygame.display.flip()
        reloj.tick(60)
    monedas += puntos  # 1 punto = 1 moneda
    pygame.mixer.Sound.stop(sonido_fondo)
    pygame.mixer.Sound.play(sonido_gameover)
    pantalla_gameover(puntos)

# Nueva pantalla de Game Over

def pantalla_gameover(puntos):
    fuente_over = pygame.font.SysFont("Arial", 50)
    fuente_btn = pygame.font.SysFont("Arial", 30)
    boton_reiniciar = Boton(ANCHO//2-100, 350, 200, 50, "Reintentar", AZUL, VERDE, accion=None)
    boton_salir = Boton(ANCHO//2-100, 420, 200, 50, "Salir", ROJO, AZUL, accion=None)
    while True:
        dibujar_fondo()
        texto = fuente_over.render("GAME OVER", True, ROJO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 120))
        texto_puntos = fuente.render(f"Puntaje: {puntos}", True, BLANCO)
        pantalla.blit(texto_puntos, (ANCHO//2 - texto_puntos.get_width()//2, 220))
        boton_reiniciar.dibujar(pantalla, fuente_btn)
        boton_salir.dibujar(pantalla, fuente_btn)
        texto_info = fuente_btn.render("Haz clic en un botón o usa R para reintentar, ESC para salir", True, AMARILLO)
        pantalla.blit(texto_info, (ANCHO//2 - texto_info.get_width()//2, 300))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    main()
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.rect.collidepoint(evento.pos):
                    main()
                if boton_salir.rect.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        reloj.tick(30)

# Redefinir dibujar_estrella y dibujar_bomba para mejor visual

def dibujar_estrella(pantalla, x, y):
    # Estrella más detallada
    pygame.draw.polygon(pantalla, AMARILLO, [
        (x+15, y), (x+18, y+10), (x+30, y+10), (x+20, y+18),
        (x+24, y+30), (x+15, y+22), (x+6, y+30), (x+10, y+18),
        (x, y+10), (x+12, y+10)
    ])

def dibujar_bomba(pantalla, x, y):
    pygame.draw.circle(pantalla, ROJO, (x + 15, y + 15), 15)
    pygame.draw.line(pantalla, BLANCO, (x + 15, y), (x + 15, y - 10), 3)
    pygame.draw.circle(pantalla, NEGRO, (x + 15, y + 15), 15, 2)

# Nueva función para dibujar la nave espacial

def dibujar_nave(pantalla, x, y):
    # Cuerpo principal
    pygame.draw.polygon(pantalla, AZUL, [(x+25, y), (x+50, y+60), (x, y+60)])
    # Cabina
    pygame.draw.ellipse(pantalla, BLANCO, (x+10, y+30, 30, 20))
    # Detalles
    pygame.draw.rect(pantalla, VERDE, (x+20, y+50, 10, 10))

# Nueva clase para disparos
class Disparo:
    def __init__(self, x, y, angulo=0, especial=False):
        self.rect = pygame.Rect(x+22, y, 6, 18)
        self.vel = -12
        self.angulo = angulo
        self.especial = especial
    def mover(self):
        self.rect.y += int(self.vel * (1 if self.angulo == 0 else abs(1)))
        self.rect.x += int(12 * self.angulo)
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, AMARILLO if not self.especial else (255,128,0), self.rect)

# Nueva función para dibujar barras segmentadas

def dibujar_barra_segmentada(pantalla, x, y, ancho, alto, valor, max_valor, color, color_fondo, texto):
    segmento = (ancho - 2) // max_valor
    for i in range(max_valor):
        rect = pygame.Rect(x+1+i*segmento, y+1, segmento-2, alto-2)
        pygame.draw.rect(pantalla, color_fondo, rect)
        if i < valor:
            pygame.draw.rect(pantalla, color, rect)
    borde = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, BLANCO, borde, 2)
    t = fuente.render(texto, True, BLANCO)
    pantalla.blit(t, (x+ancho+10, y+alto//2-t.get_height()//2))

# Función principal

def main():
    dificultad = menu_principal()
    juego(dificultad)
    guardar_progreso()

if __name__ == "__main__":
    try:
        main()
    finally:
        guardar_progreso()

pygame.quit()