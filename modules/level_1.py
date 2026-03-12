import math
import time

from PySide6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsItem, QGraphicsItemGroup, QGraphicsPixmapItem, QGraphicsRectItem

from PySide6.QtCore import QEasingCurve, QTimer, QVariantAnimation, Qt
from PySide6.QtGui import QColor, QLinearGradient, QPalette, QPixmap, QTransform
from PySide6.QtCore import QTimer, QElapsedTimer

from modules.client import submit_score
from modules.keys_pulse import efecto_hit, limpiar_brillo
from obj.keys import key
from PySide6.QtGui import QShortcut, QKeySequence
import json
from PySide6.QtGui import QBrush, QPixmap, QPen
from PySide6.QtCore import Qt


COLORES_ESTELA = {
    1: QColor(255, 37, 0, 140),   # Carril 1: Rojo
    2: QColor(50, 255, 50, 150),   # Carril 2: Verde
    3: QColor(160, 50, 255, 150),  # Carril 3: Morado
    4: QColor(255, 255, 50, 150)   # Carril 4: Amarillo
}


def level_1(self,level):
    self.gamestart=True
    self.modo_especial = False
    self.brillo_20_hecho = False
    self.special_listo = False # Añade esto también
    self.estilo_combo = ""
    
    
    
    #crea las teclas que necesites para el nivel en el JSON
    #objeto key: nombre,color,velocidad,duracion,carril,tiempo en spawnear
    # para el spaw cada 10 son 0.16 segundos, 62=1seg, 125=2seg etc...
    with open("levels/"+level+".json", 'r') as f:
        partitura = json.load(f)
        for datos in partitura:
            self.keys.append(key(*datos))


   ###################################

   # Añade cada tecla en su respectivo carril y la dibuja
  
    pos_carril=None
    imagenes_carriles = {
    1: "Picture/left_key.png",
    2: "Picture/right_key.png",
    3: "Picture/up_key.png",
    4: "Picture/down_key.png"
}
    pos_carril=None
    
    setup_neon_lanes(self)
    
    #activa el efecto glow neon en el especial

# 2from PySide6.QtWidgets import QGraphicsRectItem


# --- DENTRO DE TU FUNCIÓN DONDE ESTÁ EL BUCLE ---
    for i in self.keys:
        # 1. Calculamos la posición vertical según el carril
        pos_carril = 40 + (i.carril - 1) * 80
        
        # 2. Calculamos las dimensiones iniciales
        # Multiplicamos la duración por 100 (o el valor que prefieras para el largo)
        ancho_nota = int(100 + i.duration)
        alto_nota = 50

        # Creamos un grupo para contener la estela y la cabeza
        grupo_nota = QGraphicsItemGroup()
        i.alto_grafico = alto_nota

        # --- A. CREAR LA ESTELA (TRAIL) ---
        # El ancho de la estela es proporcional a la duración
        ancho_estela = int(i.duration) # Ajusta este factor si necesitas estelas más largas

        rect_estela = QGraphicsRectItem(0, 0, ancho_estela, alto_nota-5)
        if i.duration <= 1: # Ajusta este número según tus notas del JSON
            rect_estela.setVisible(False)



        color_carril = COLORES_ESTELA.get(i.carril, QColor(255, 255, 255, 180))

        rect_estela.setBrush(QBrush(color_carril))
        rect_estela.setPen(QPen(Qt.NoPen))
        rect_estela.setPos(30, 3)

        
        
        # 3. CREAMOS EL RECTÁNGULO (En lugar de PixmapItem)
        # Argumentos: x_interno, y_interno, ancho, alto
        
        
            
        
        # 4. CARGAMOS Y PREPARAMOS LA TEXTURA
        if i.duration > 1:
            glow = QGraphicsDropShadowEffect()
            glow.setBlurRadius(25) # Un poco más de blur para la estela
            glow.setOffset(0, 0)

            # Usamos el mismo color de la estela para el glow pero más intenso
            color_glow = QColor(color_carril)
            color_glow.setAlpha(255) 
            glow.setColor(color_glow)

            rect_estela.setGraphicsEffect(glow)
            glow.setEnabled(False) # Apagado inicialmente
            i.glow_effect = glow # Guardamos referencia
        
        
        # --- B. CREAR LA CABEZA (HEAD) ---
    # Obtenemos la ruta de imagen normal (la que no se estira)
        ruta_imagen_cabeza = imagenes_carriles.get(i.carril, "Picture/left_key.png")
        pixmap_cabeza = QPixmap(ruta_imagen_cabeza)
        
    
    # Escalamos la cabeza SOLO para que coincida con el alto del carril,
    # manteniendo su aspecto original (KeepAspectRatio)
        pixmap_escalado = pixmap_cabeza.scaledToHeight(
        alto_nota, 
        Qt.SmoothTransformation
        )
        img_cabeza = QGraphicsPixmapItem(pixmap_escalado)

        grupo_nota.addToGroup(rect_estela)
        grupo_nota.addToGroup(img_cabeza)

        i.grafico_estela = rect_estela # El rectángulo que se encoje
        i.grafico_cabeza = img_cabeza

        grupo_nota.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        grupo_nota.setPos(1160, pos_carril)

        self.scene.addItem(grupo_nota)
        i.graphics = grupo_nota

        if i.carril == 1:
            self.carril_1.append(i)
        elif i.carril == 2:
            self.carril_2.append(i)
        elif i.carril == 3:
            self.carril_3.append(i)
        elif i.carril == 4:
            self.carril_4.append(i)
        
    
        
        
    ###########################################################


   


    ############################################################

   

    #Inicia el nivel
    iniciar(self)
    inicializar_musica(self)

##################################################################
# inicia el timer
def iniciar(self):
    from PySide6.QtCore import Qt
    #cronometro para el delta time
    self.window.installEventFilter(self)
    
        
        # Forzamos foco total
    self.window.setFocusPolicy(Qt.StrongFocus)
    self.window.setFocus()
    self.cronometro = QElapsedTimer()
    self.cronometro.start()

    self.count=0
    self.timer = QTimer()
    self.timer.timeout.connect(lambda: comprobar(self))#conecta a la funcion
    self.timer.start(16)# inicia el evento 
    


############################################################
# toda animacion y evento con tiempo va aqui
def comprobar(self):
    # 1. Calcular Delta Time (dt)
    dt = self.cronometro.nsecsElapsed() / 1000000000.0
    self.cronometro.restart() 

    # 2. Mapeo de carriles
    mapeo_listas = {
        1: self.carril_1,
        2: self.carril_2,
        3: self.carril_3,
        4: self.carril_4
    }
    # --- Dentro de def comprobar(self): ---

# 1. ACTIVACIÓN: Solo entra si el combo es 20+ Y el brillo NO se ha hecho todavía
    if self.combo == 1 and not self.brillo_20_hecho and not self.modo_especial:
        print("¡HITO ALCANZADO: COMBO 20!") # Esto ahora saldrá UNA sola vez

        self.special_listo = True
        self.brillo_20_hecho = True # <--- EL CERROJO: Cerramos la puerta de inmediato

        self.estilo_combo = self.label_special.styleSheet()
        animar_reflejo_label(self.label_special)

    # 2. DESACTIVACIÓN: Cuando activas el especial
    if self.modo_especial and self.special_listo:
        print("¡MODO PANTHER ACTIVADO!")

        # Usamos getattr por seguridad para evitar el AttributeError si no existe
        estilo = getattr(self, 'estilo_combo', "color: white;")
        detener_reflejo_label(self.label_special, estilo)

        self.special_listo = False # Marcamos que ya se usó el especial

    # Aquí puedes añadir un efecto nuevo para el modo especial si quieres
    # self.label_special.setText("¡MODO PANTHER!")

    
        
        # 2. Marcamos como hecho para que no se repita en el siguiente frame
        

    if self.modo_especial:
        actualizar_pulso_neon(self)

    # 3. Mover objetos y verificar fin de nivel (PRIMERO MOVER)
    todos_vacios = True
    for num, lista in mapeo_listas.items():
        if lista:
            todos_vacios = False
            for i in lista[:]: # Copia de la lista para evitar errores al eliminar
                # Una nota frena si es la primera y está activa
                debe_frenar = (i == lista[0] and self.notas_largas_activas.get(num, False))
                mover_objeto(self, i, dt, lista, frenar=debe_frenar)

    # 4. Procesar Notas Largas (DESPUÉS DE MOVER)
    # Hacemos esto después para que si la nota se elimina en slide_key, 
    # mover_objeto no intente procesarla de nuevo en el mismo frame.
    for num in [1, 2, 3, 4]:
        if self.notas_largas_activas.get(num, False):
            # IMPORTANTE: Asegúrate que tu slide_key use 'mapeo_listas[num]'
            slide_key(self, dt, mapeo_listas[num], num)

    # 5. Animación del personaje y tiempos
    self.acumulador_tiempo += dt
    if self.acumulador_tiempo >= 0.1: 
        self.frame_actual = (self.frame_actual + 1) % self.total_frames
        actualizar_frame(self, self.frame_actual)
        self.acumulador_tiempo = 0
    
    times(self, dt)

    # 6. Comprobación de nivel terminado
    if self.modo_creator==False:
        if todos_vacios and self.gamestart:
            self.timer.stop()
            self.gamestart = False
            print("Nivel terminado con éxito")
            self.keys = []
            self.brillos_activos = {}
            try:
                submit_score(self.player_name, self.level_now, self.combo,self.points)
            except:
                print("error de red al subir puntaje")
    self.scene.update()

    
        
###################################################################
       
# mueve cada key en su respectivo tiempo
# Mueve cada key en su respectivo tiempo
# mueve cada key en su respectivo tiempo
# Asegúrate de agregar ', frenar=False' aquí:
def mover_objeto(self, key, dt, carril_key, frenar=False):
    if not key or not key.graphics:
        return

    meta_x = 100
    spawn_x = 1160
    distancia = spawn_x - meta_x
    velocidad = key.speed + self.mod_speed
    
    tiempo_cancion = self.player.position() / 1000.0
    tiempo_vuelo = distancia / velocidad

    if tiempo_cancion < (key.timing - tiempo_vuelo):
        key.graphics.setVisible(False)
        key.graphics.setPos(spawn_x, key.graphics.y())
        return

    key.graphics.setVisible(True)

    # --- LÓGICA ANTI-RETROCESO ---
    if frenar:
        # IMPORTANTE: No hacemos nada. 
        # Al no llamar a setPos o setX, la nota se queda 
        # exactamente en la X que tenía el frame anterior.
        pass 
    else:
        # Solo movemos la nota si NO está frenada
        x_ideal = meta_x + (velocidad * (key.timing - tiempo_cancion))
        x_actual = key.graphics.x()
        
        if abs(x_actual - x_ideal) > 50: 
            nueva_x = x_ideal
        else:
            nueva_x = x_actual - (velocidad * dt)
            nueva_x = nueva_x + (x_ideal - nueva_x) * 0.1 
        
        key.graphics.setPos(nueva_x, key.graphics.y())

    # Lógica de Miss
    if not frenar:
        # Si es nota larga, el límite es el final de su duración
        margen_extra = 0.4
        duracion_nota = key.duration / key.speed if key.duration > 1 else 0
        limite = key.timing + duracion_nota + margen_extra

        if tiempo_cancion > limite:
            if key in carril_key:
                print(f"MISS por tiempo en carril")
                self.combo=0
                self.label_combo.setText(str(self.combo))
                self.audio_output_miss.setVolume(0)
                if key.graphics.scene():
                    self.scene.removeItem(key.graphics)
                carril_key.remove(key)

#valida cada pulsacion del teclado



#Mide el tiempo
def times(self,dt):
    self.dt=dt
    self.count = round(self.count + dt, 2)
    #print("timing",self.count)


# Aqui va la musica

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
def inicializar_musica(self):
    # --- PISTA 1: LA CANCIÓN PRINCIPAL ---
    self.audio_output = QAudioOutput()
    self.audio_output.setVolume(50)
    cancion_a_reproducir = self.audio_actual
    self.player = QMediaPlayer()
    self.player.setAudioOutput(self.audio_output)
    self.player.setSource(QUrl.fromLocalFile(self.audio_actual))

    # --- PISTA 2: EFECTO DE ERROR (Miss) ---
    
    self.audio_output_miss = QAudioOutput()
    self.audio_output_miss.setVolume(100)
    self.player_miss = QMediaPlayer()
    self.player_miss.setAudioOutput(self.audio_output_miss)
    self.player_miss.setSource(QUrl.fromLocalFile(self.instrumento_actual))
    # --- REPRODUCIR ---
    self.player.play()
    self.player_miss.play() # La canción empieza
    if self.modo_creator==True:
        self.audio_output2 = QAudioOutput()
        self.audio_output2.setVolume(50)

        self.player_miss2 = QMediaPlayer()
        self.player_miss2.setAudioOutput(self.audio_output2)
        self.player_miss2.setSource(QUrl.fromLocalFile(self.instrumento_actual))

        # --- REPRODUCIR ---
        self.player.play()
        self.player_miss2.play() # La canción empieza



#Actualiza el moviemiento para sprites
def actualizar_frame(self, indice_columna):
    # Calculamos dónde empieza el recorte en la imagen grande
    x = indice_columna * self.frame_ancho
    y = 0 # Si solo hay una fila de frames
    
    # RECORTAMOS un pedazo de 239x343
    frame_recortado = self.sprite_sheet.copy(x, y, self.frame_ancho, self.frame_alto)
    
    # Lo ponemos en el item que ya está en la escena
    self.personaje_item.setPixmap(frame_recortado)
    self.graphics_sprite.setFocusPolicy(Qt.FocusPolicy.NoFocus)







#Logica para nota tipo slide

def slide_key(self, dt, carril_key, num_carril):
    if not carril_key or not carril_key[0]:
        self.notas_largas_activas[num_carril] = False
        return

    nota_actual = carril_key[0]
    
    if self.teclas_pisadas.get(num_carril, False):
        efecto_hit(self, num_carril, sostenido=True)



        rect_estela = nota_actual.grafico_estela.rect()
        
        
        # La reducción debe ser proporcional a la velocidad para que coincida con el ritmo
        reduccion = nota_actual.speed * dt
        nuevo_ancho = max(0, rect_estela.width() - reduccion)

        if nuevo_ancho <= 0:
            print(f"Carril {num_carril}: Nice completo")
            self.combo+=1
            self.label_combo.setText(str(self.combo))
            limpiar_brillo(self, num_carril)
            self.scene.removeItem(nota_actual.graphics)

            carril_key.pop(0)
            self.notas_largas_activas[num_carril] = False
        else:
            # Seteamos el nuevo rect SIN mover la posición X del item en la escena
            nota_actual.grafico_estela.setRect(0, 0, nuevo_ancho, nota_actual.alto_grafico)
            
            if hasattr(nota_actual, 'glow_effect'):
                nota_actual.glow_effect.setEnabled(True)

            self.points += 1
            if self.points % 10 == 0:
                self.label_points.setText(str(self.points))
        self.audio_output_miss.setVolume(50)
    else:
        area_afectada = nota_actual.graphics.sceneBoundingRect()
        nota_actual.glow_effect.setEnabled(False)
        nota_actual.graphics.setGraphicsEffect(None)
        self.scene.update(area_afectada)
        # Si suelta, limpiamos
        limpiar_brillo(self, num_carril)
        self.notas_largas_activas[num_carril] = False
        

        self.scene.removeItem(nota_actual.graphics)
        carril_key.pop(0)
        limpiar_nota_total(self,nota_actual, carril_key, num_carril)
        



# --- COLÓCALA AQUÍ ---
from shiboken6 import isValid # <--- IMPORTANTE: Agrega esta importación arriba de todo

def limpiar_nota_total(self, nota, carril_key, num_carril):
    if not nota or not nota.graphics:
        return

    # 1. Obtener área antes de cualquier borrado
    try:
        if isValid(nota.graphics):
            rect_sucio = nota.graphics.sceneBoundingRect()
        else:
            rect_sucio = None
    except:
        rect_sucio = None

    # 2. Limpieza del efecto con VALIDACIÓN DOBLE
    if hasattr(nota, 'glow_effect') and nota.glow_effect is not None:
        # isValid comprueba si el objeto C++ sigue existiendo
        if isValid(nota.glow_effect):
            try:
                nota.glow_effect.setEnabled(False)
                if isValid(nota.graphics):
                    nota.graphics.setGraphicsEffect(None)
            except RuntimeError:
                pass # Si justo se borró en este microsegundo, ignoramos
        
        # Matamos la referencia en Python para seguridad
        nota.glow_effect = None

    # 3. Borrado físico del item gráfico
    if isValid(nota.graphics):
        try:
            nota.graphics.setVisible(False)
            if nota.graphics.scene():
                self.scene.removeItem(nota.graphics)
            
            # 4. Forzar repintado solo si tenemos el área
            if rect_sucio:
                self.scene.update(rect_sucio)
        except RuntimeError:
            pass

    # 5. Limpieza de listas (siempre se hace)
    if nota in carril_key:
        carril_key.remove(nota)
        nota.grafico_estela = None
        nota.grafico_cabeza = None
    
    self.notas_largas_activas[num_carril] = False
    
    # Intenta llamar a limpiar_brillo solo si existe
    if hasattr(self, 'limpiar_brillo'):
        self.limpiar_brillo(num_carril)



def setup_neon_lanes(self):
    """Crea los carriles neón con un degradado de opacidad horizontal"""
    self.luces_carriles = {}
    
    # Definimos los colores Neón base (RGBA)
    # Usaremos Alpha 200 para que el inicio sea bastante visible
    colores_base = {
        1: QColor(255, 0, 0, 120),    # Rojo
        2: QColor(0, 255, 0, 120),    # Verde
        3: QColor(180, 0, 255, 120),  # Morado
        4: QColor(255, 255, 0, 120)   # Amarillo
    }

    # Posiciones Y y dimensiones (con los ajustes que hicimos antes)
    y_posiciones = [37, 117, 210, 290] 
    alto_carril = 50
    ancho_pista = 500 # Cubre toda la pantalla

    for i, y_base in enumerate(y_posiciones, 1):
        # 1. Crear el rectángulo base
        rect = QGraphicsRectItem(0, 0, ancho_pista, alto_carril)
        rect.setPos(0, y_base)
        rect.setPen(QPen(Qt.NoPen)) # Sin borde

        # --- AQUÍ ESTÁ LA MAGIA DEL DEGRADADO (Fade-out espacial) ---
        
        # Creamos el degradado lineal horizontal
        # Comienza en X=0, Y=0 (izquierda) y termina en X=ancho_pista, Y=0 (derecha)
        gradient = QLinearGradient(0, 0, ancho_pista, 0)
        
        # Definimos los puntos de parada (stops)
        # 0.0 es el inicio, 1.0 es el final de la pista.
        
        # Stop 1 (X=0): Color base con opacidad total (RGBA=200)
        color_inicio = QColor(colores_base[i])
        gradient.setColorAt(0.0, color_inicio)
        
        # Stop 2 (X=ancho_pista/3): Se mantiene sólido por un tercio de la pista
        gradient.setColorAt(0.33, color_inicio)
        
        # Stop 3 (X=ancho_pista): Totalmente transparente (Alpha=0)
        color_fin = QColor(colores_base[i])
        color_fin.setAlpha(0) # Niebla invisible al final
        gradient.setColorAt(1.0, color_fin)
        
        # Aplicamos el degradado como brush al rectángulo
        rect.setBrush(QBrush(gradient))
        
        # -----------------------------------------------------------

        # 2. Configurar el Glow (Brillo)
        # El Glow también se beneficiará del degradado
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(60)
        glow.setOffset(0, 0)
        
        # Color del brillo igual al carril pero intenso
        color_glow = QColor(colores_base[i])
        color_glow.setAlpha(255) 
        glow.setColor(color_glow)
        
        rect.setGraphicsEffect(glow)
        rect.setZValue(-1) # DETRÁS de las notas
        rect.setVisible(False) # Oculto inicialmente
        glow.setEnabled(False) # Apagado inicialmente
        
        # 3. Guardar y añadir a la escena
        self.scene.addItem(rect)
        self.luces_carriles[i] = {
            "item": rect,
            "effect": glow
        }


def toggle_neon_special(self, activar=True):
    """Enciende o apaga el efecto neón completo"""
    if hasattr(self, 'luces_carriles'):
        for data in self.luces_carriles.values():
            item = data["item"]
            effect = data["effect"]
            
            if isValid(item):
                item.setVisible(activar)
                effect.setEnabled(activar) # Esto es clave para el rendimiento


def animar_neon_especial(self, encender=True):
    """Anima la opacidad de los carriles neón (Fade In / Fade Out)"""
    if not hasattr(self, 'luces_carriles'):
        return

    # 1. Preparación inicial
    inicio = 0.0 if encender else 1.0
    fin = 1.0 if encender else 0.0

    if encender:
        for data in self.luces_carriles.values():
            data["item"].setVisible(True)
            data["effect"].setEnabled(True)
            data["item"].setOpacity(0)

    # 2. Configuración de la animación de Qt
    self.anim_neon = QVariantAnimation(self)
    self.anim_neon.setDuration(400) # 400ms es un tiempo ideal para juegos de ritmo
    self.anim_neon.setStartValue(inicio)
    self.anim_neon.setEndValue(fin)
    self.anim_neon.setEasingCurve(QEasingCurve.OutQuad)

    # 3. Conexión para actualizar la opacidad en cada paso
    def actualizar(valor):
        for data in self.luces_carriles.values():
            data["item"].setOpacity(valor)

    self.anim_neon.valueChanged.connect(actualizar)

    # 4. Limpieza al terminar si estamos apagando
    if not encender:
        self.anim_neon.finished.connect(lambda: toggle_neon_special(self,False))

    self.anim_neon.start()




def actualizar_pulso_neon(self):
    """Hace que los carriles neón 'respiren' de forma lenta y suave"""
    if hasattr(self, 'luces_carriles') and self.modo_especial:
        # --- AJUSTES PARA SUAVIDAD ---
        # Bajamos la frecuencia de 10 a 3 para que sea mucho más lento
        frecuencia = 3.5 
        
        # Bajamos la amplitud de 0.25 a 0.15 para que el cambio de brillo no sea brusco
        amplitud = 0.15
        
        # Subimos la base a 0.85 para que siempre esté bastante iluminado
        base = 0.80
        
        # Calculamos la opacidad rítmica
        opacidad = base + amplitud * math.sin(time.time() * frecuencia)
        
        for data in self.luces_carriles.values():
            # Usamos isValid para evitar errores si algo se borró
            if isValid(data["item"]) and data["item"].isVisible():
                data["item"].setOpacity(opacidad)




def desactivar_especial(self):
    """Limpia el estado del especial y resetea los valores visuales"""
    self.modo_especial = False
    
    # 1. Llamamos a la animación de salida (Fade Out)
    # Esta función ya tiene el lambda que pone setVisible(False) al terminar
    animar_neon_especial(self, False)
    
    # 2. Resetear opacidad de los carriles
    # Lo hacemos con un pequeño delay o después de la animación 
    # para que no se vea un "salto" visual
    if hasattr(self, 'luces_carriles'):
        for data in self.luces_carriles.values():
            # Volvemos a la opacidad base
            data["item"].setOpacity(1.0)
            # Opcional: Desactivamos el efecto de sombra para ahorrar recursos
            data["effect"].setEnabled(False)





def animar_reflejo_label(label):
    if not label or not isValid(label):
        return
        
    # 1. Guardamos el estilo completo
    estilo_original = label.styleSheet()
    
    # 2. Extraemos solo lo que NO es color del estilo original
    # Para asegurar que el tamaño NO cambie, mantenemos el estilo pero 
    # quitamos cualquier propiedad de 'color' que bloquee al Palette.
    # Si tienes un tamaño fijo (ej: font-size: 20px), esto lo mantendrá.
    estilo_temporal = estilo_original.replace("color:", "x-color:") # "Anulamos" el color CSS
    
    label.setStyleSheet(estilo_temporal + "; background: transparent;")

    animacion = QVariantAnimation(label)
    animacion.setDuration(1200)
    animacion.setStartValue(-0.5) 
    animacion.setEndValue(1.5)
    animacion.setEasingCurve(QEasingCurve.Linear)
    animacion.setLoopCount(-1)

    def aplicar_gradiente(progreso):
        if not isValid(label): return
        
        ancho = label.width()
        if ancho <= 0: ancho = 150
        
        gradient = QLinearGradient(0, 0, ancho, 0)
        azul_m = QColor(0, 160, 180)
        azul_b = QColor(82, 165, 255)
        blanco = QColor(255, 255, 255)

        gradient.setColorAt(max(0.0, min(1.0, progreso - 0.2)), azul_m)
        gradient.setColorAt(max(0.0, min(1.0, progreso - 0.1)), azul_b)
        gradient.setColorAt(max(0.0, min(1.0, progreso)), blanco)
        gradient.setColorAt(max(0.0, min(1.0, progreso + 0.1)), azul_b)
        gradient.setColorAt(max(0.0, min(1.0, progreso + 0.2)), azul_m)

        palette = label.palette()
        palette.setBrush(QPalette.WindowText, QBrush(gradient))
        label.setPalette(palette)
        label.update()

    animacion.valueChanged.connect(aplicar_gradiente)
    
    def restaurar():
        if isValid(label):
            label.setPalette(label.style().standardPalette())
            label.setStyleSheet(estilo_original)

    animacion.finished.connect(restaurar)
    animacion.start()
    label._anim_reflejo = animacion


def detener_reflejo_label(label, estilo_original):
    # 1. Verificamos que el label exista y sea válido
    if not label or not isValid(label):
        return

    # 2. Buscamos la animación que guardamos con el nombre '_anim_reflejo'
    if hasattr(label, '_anim_reflejo'):
        # Al llamar a stop(), se dispara automáticamente la función 'restaurar'
        # que definimos dentro de la animación original.
        label._anim_reflejo.stop()
        
        # 3. Limpiamos la referencia para liberar memoria
        del label._anim_reflejo
    
    # 4. Por seguridad, nos aseguramos de que el estilo y la paleta vuelvan al original
    label.setPalette(label.style().standardPalette())
    label.setStyleSheet(estilo_original)
    label.update()