from PySide6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsItem, QGraphicsPixmapItem, QGraphicsRectItem

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QPixmap, QTransform
from PySide6.QtCore import QTimer, QElapsedTimer

from modules.client import submit_score
from modules.keys_pulse import efecto_hit, limpiar_brillo
from obj.keys import key
from PySide6.QtGui import QShortcut, QKeySequence
import json
from PySide6.QtGui import QBrush, QPixmap, QPen
from PySide6.QtCore import Qt

def level_1(self,level):
    self.gamestart=True
    
    
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
    imagenes_carriles_duration = {
    1: "Picture/left_key2.png",
    2: "Picture/right_key2.png",
    3: "Picture/up_key2.png",
    4: "Picture/down_key2.png"
}


# 2from PySide6.QtWidgets import QGraphicsRectItem


# --- DENTRO DE TU FUNCIÓN DONDE ESTÁ EL BUCLE ---
    for i in self.keys:
        # 1. Calculamos la posición vertical según el carril
        pos_carril = 40 + (i.carril - 1) * 80
        
        # 2. Calculamos las dimensiones iniciales
        # Multiplicamos la duración por 100 (o el valor que prefieras para el largo)
        ancho_nota = int(100 + i.duration)
        alto_nota = 50
        
        # 3. CREAMOS EL RECTÁNGULO (En lugar de PixmapItem)
        # Argumentos: x_interno, y_interno, ancho, alto
        rect_item = QGraphicsRectItem(0, 0, ancho_nota, alto_nota)
        
            
        
        # 4. CARGAMOS Y PREPARAMOS LA TEXTURA
        if i.duration > 1:
            ruta_imagen = imagenes_carriles_duration.get(i.carril, "Picture/left_key2.png")
            glow = QGraphicsDropShadowEffect()
            
            # Configuración para que parezca Glow y no Sombra:
            glow.setBlurRadius(20)      # Qué tan "suave" es el brillo
            glow.setOffset(0, 0)        # IMPORTANTE: Centro del brillo (sin desplazamiento)
            
            # Color del brillo (puedes usar el color de la nota o blanco)
            # Ejemplo: Brillo blanco intenso
            glow.setColor(QColor(255, 255, 25, 200)) # 
            
            # Asignamos el efecto al item gráfico
            rect_item.setGraphicsEffect(glow)
            
            # Lo apagamos inicialmente para ahorrar FPS
            glow.setEnabled(False) 
            
            
            # Guardamos una referencia en el objeto 'key' para usarlo luego
            i.glow_effect = glow
            rect_item.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

        else:
            ruta_imagen = imagenes_carriles.get(i.carril, "Picture/left_key.png")
        pixmap = QPixmap(ruta_imagen)
        
        
        # Escalamos la imagen exactamente al tamaño de la nota
        pixmap_escalado = pixmap.scaled(
            ancho_nota, 
            alto_nota, 
            Qt.IgnoreAspectRatio, 
            Qt.SmoothTransformation
        )
        
        # Creamos el pincel (Brush) con la imagen
        brush = QBrush(pixmap_escalado)
        rect_item.setBrush(brush)
        
        # 5. ESTÉTICA: Quitamos el borde de línea del rectángulo
        rect_item.setPen(QPen(Qt.NoPen))
        
        # 6. POSICIONAMOS EL RECTÁNGULO EN LA ESCENA
        # Aquí usamos 1160 como X inicial de aparición
        rect_item.setPos(1160, pos_carril)
        
        # 7. REGISTRAMOS EN LA ESCENA Y EN TU LÓGICA
        self.scene.addItem(rect_item)
        i.graphics = rect_item  # Ahora i.graphics SI TIENE el método .setRect()
        if i.carril==1:
            self.carril_1.append(i)
        elif i.carril==2:
            self.carril_2.append(i)
        elif i.carril==3:
            self.carril_3.append(i)
        elif i.carril==4:
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
        
        rect = nota_actual.graphics.rect()
        # La reducción debe ser proporcional a la velocidad para que coincida con el ritmo
        reduccion = nota_actual.speed * dt
        nuevo_ancho = max(0, rect.width() - reduccion)

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
            nota_actual.graphics.setRect(0, 0, nuevo_ancho, rect.height())
            nota_actual.glow_effect.setEnabled(True)
            self.points += 1
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
    
    self.notas_largas_activas[num_carril] = False
    
    # Intenta llamar a limpiar_brillo solo si existe
    if hasattr(self, 'limpiar_brillo'):
        self.limpiar_brillo(num_carril)