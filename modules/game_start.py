from PySide6 import QtGui
from PySide6 import QtCore
from PySide6.QtWidgets import QFrame, QGraphicsLineItem, QGraphicsPixmapItem,QGraphicsView, QGraphicsScene,QGraphicsRectItem,QPushButton,QLabel
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, QPalette, QPen,QPixmap,QBrush
from PySide6.QtCore import Qt

from modules.responsive.responsive import rezise_1, rezise_carriles
from obj.keys import key
from PySide6.QtGui import QShortcut, QKeySequence
from modules.level_1 import actualizar_frame, level_1






def game_start_level(self,nivel):
    self.level_now=nivel
    print(":v",nivel)
    if hasattr(self, 'menu_interno') and self.menu_interno.isVisible():
        self.menu_interno.hide()

    self.points=0
    self.combo=0
    self.multiplier=1
    #self.btn_out = self.window.findChild(QPushButton, "btn_out")
    #self.btn_reset = self.window.findChild(QPushButton, "reset")
    self.label_points = self.window.findChild(QLabel, "label_points")
    self.label_combo = self.window.findChild(QLabel, "label_combo")
    self.label_multi = self.window.findChild(QLabel, "label_multi")
    self.label_special = self.window.findChild(QLabel, "label_special")
    self.label_points.setText(str(self.points))
    self.label_combo.setText(str(self.combo))
    self.label_multi.setText("x"+str(self.multiplier))
    #self.btn_out.clicked.connect(lambda: level_1(self,nivel))
    self.frame_central = self.window.findChild(QFrame, "framecentral")

    
    self.graphics_view = self.window.findChild(QGraphicsView, "graphics01")
    
    self.scene = QGraphicsScene()
    self.scene.setSceneRect(0, 0, 600, 180)
    self.graphics_view.setScene(self.scene)
    

    # 2. ANCLAR LA VISTA: Evita que la cámara "flote" o centre objetos
    self.graphics_view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    
    # 3. ELIMINAR EL DESPLAZAMIENTO AUTOMÁTICO
    self.graphics_view.setTransformationAnchor(QGraphicsView.NoAnchor)


    #keys botones
    y_sumar = 40
    colores = ["red", "green", "yellow", "blue"] # Puedes mantenerlos como respaldo
    imagenes = ["Picture/left_btn.png", "Picture/right_btn.png", "Picture/up_btn.png", "Picture/down_btn.png"]
    self.carriles = []
    self.ancho_carril = 100
    self.alto_carril = 50
    rezise_carriles(self)

    for i in range(4):
        rect = QGraphicsRectItem(0, 0, self.ancho_carril, self.alto_carril)
        rect.setPos(0, y_sumar)

        # Crear el pixmap y aplicarlo como brocha
        pixmap = QPixmap(imagenes[i])
        # Escalamos la imagen para que quepa exactamente en el rectángulo (100x50)
        pixmap = pixmap.scaled(self.ancho_carril, self.alto_carril)
        rect.setBrush(QBrush(pixmap))
    
    # Si no quieres que tenga el borde negro del rectángulo:
        rect.setPen(Qt.PenStyle.NoPen) 

        self.scene.addItem(rect)
        y_sumar += 80
        self.carriles.append(rect)

        




#########
    # --- Lógica para las líneas de tu juego ---
    ancho_total = 1160 
    y_posiciones = [96, 176, 256, 336]  
   # y_posiciones = [90, 170, 250, 330]  

    for y in y_posiciones:
        # --- TODO ESTO DEBE ESTAR INDENTADO (con espacios) ---
        linea = QGraphicsLineItem(0, y, ancho_total, y) 

        color_linea = QColor(60, 60, 60) 
        pen = QPen(color_linea)

        pen.setWidth(10)

        pen.setCapStyle(Qt.RoundCap) 
        pen.setStyle(Qt.SolidLine) 

        linea.setPen(pen)
        linea.setZValue(-1) 
        self.scene.addItem(linea) # Ahora se añadirá una por cada 'y'

        #keys
        self.keys = []
        self.carril_1=[]



    # escena para los sprites
    self.graphics_sprite = self.ui_juego.findChild(QGraphicsView, "graphics_sprites")
    
    
    self.scene2 = QGraphicsScene()
    self.scene2.setSceneRect(0, 0, 900, 300)
    self.graphics_sprite.setScene(self.scene2)
    #fondo = QGraphicsPixmapItem(QPixmap("Picture/fondo_escenario.png"))

# 2. Asegurarte de que esté al fondo de todo (Z-Value bajo)
    #fondo.setZValue(-100) 

    # 3. Agregarlo a la escena
    #self.scene2.addItem(fondo) # Establece el fondo como transparente

    self.graphics_sprite.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    

    # 2. ANCLAR LA VISTA: Evita que la cámara "flote" o centre objetos
    self.graphics_sprite.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    
    # 3. ELIMINAR EL DESPLAZAMIENTO AUTOMÁTICO
    self.graphics_sprite.setTransformationAnchor(QGraphicsView.NoAnchor)
    self.graphics_sprite.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.graphics_sprite.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    self.graphics_sprite.setStyleSheet("background: transparent; border: none;")
    self.graphics_sprite.setStyleSheet("""
    border-image: url('Picture/fondo_escenario.png');
    background-repeat: no-repeat;
    border: none;
    """)

    self.graphics_sprite.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
    self.graphics_sprite.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
    
    
    
    agregar_personaje(self)
    level_1(self,nivel)
    

   

def ajustar_vista_personaje(self):
    if hasattr(self, 'graphics_sprite') and self.graphics_sprite.scene():
        self.graphics_sprite.fitInView(
            self.graphics_sprite.scene().sceneRect(), 
            Qt.AspectRatioMode.KeepAspectRatio
        )


#-------------------Sprites personajes-----------------------------

def agregar_personaje(self):
    self.frame_actual = 0
    self.acumulador_tiempo = 0.0
    self.total_frames = 14  # Aju
    # 1. Cargamos la HOJA COMPLETA (no el item todavía)
    #self.sprite_sheet = QPixmap("Picture/Sprites_player/guitar_electric_sprite.png")
    self.sprite_sheet = QPixmap(self.guitar_patch)
    # Definimos las medidas de cada frame que me diste
    #self.frame_ancho = 239
    #self.frame_alto = 343

    self.frame_ancho = self.sprite_sheet.width() // self.total_frames
    
    # El alto suele ser el mismo que el de la imagen (si es una sola fila)
    self.frame_alto = self.sprite_sheet.height()

    # 2. Creamos el Item vacío o con el primer frame
    self.personaje_item = QGraphicsPixmapItem()
    self.personaje_item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
    
    
    
    
    # 3. Lo metemos a la escena
    self.scene2.addItem(self.personaje_item)
    print(self.scene2)
    
    # 4. Mostramos el primer frame (el 0)
    actualizar_frame(self,0) 

    # 5. Posición y Escala (para que quepa en tus 180px de alto)
    self.personaje_item.setScale(0.7) # 343 * 0.5 = 171px (perfecto para 180px)
    self.personaje_item.setPos(0, 135)
    if self.available.width() <= 1366 or self.available.height() <= 768:
        rezise_1(self)
        rezise_carriles(self)
        #QtCore.QTimer.singleShot(50, lambda: ajustar_vista_personaje(self))  # Ajustamos la vista después de un pequeño retraso

    
    

