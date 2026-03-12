from PySide6.QtWidgets import QFrame, QGraphicsLineItem, QGraphicsPixmapItem,QGraphicsView, QGraphicsScene,QGraphicsRectItem,QPushButton,QLabel
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, QPen,QPixmap,QBrush
from PySide6.QtCore import Qt

from obj.keys import key
from PySide6.QtGui import QShortcut, QKeySequence
from modules.level_1 import actualizar_frame, level_1






def game_start_level(self,nivel):
    self.level_now=nivel
    print(":v",nivel)

    self.points=0
    self.combo=0
    self.multiplier=1
    self.btn_out = self.window.findChild(QPushButton, "btn_out")
    self.btn_reset = self.window.findChild(QPushButton, "reset")
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

    for i in range(4):
        rect = QGraphicsRectItem(0, 0, 100, 50)
        rect.setPos(0, y_sumar)

        # Crear el pixmap y aplicarlo como brocha
        pixmap = QPixmap(imagenes[i])
        # Escalamos la imagen para que quepa exactamente en el rectángulo (100x50)
        pixmap = pixmap.scaled(100, 50) 
        rect.setBrush(QBrush(pixmap))
    
    # Si no quieres que tenga el borde negro del rectángulo:
        rect.setPen(Qt.PenStyle.NoPen) 

        self.scene.addItem(rect)
        y_sumar += 80
        self.carriles.append(rect)

        




#########
    # --- Lógica para las líneas de tu juego ---
    ancho_total = 1160 
    y_posiciones = [90, 170, 250, 330]  

    for y in y_posiciones:
        # --- TODO ESTO DEBE ESTAR INDENTADO (con espacios) ---
        linea = QGraphicsLineItem(0, y, ancho_total, y) 

        color_linea = QColor(80, 80, 80) 
        pen = QPen(color_linea)

        pen.setWidth(6) 

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
    self.scene2.setSceneRect(0, 0, 600, 289)
    self.graphics_sprite.setScene(self.scene2)

    self.graphics_sprite.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    

    # 2. ANCLAR LA VISTA: Evita que la cámara "flote" o centre objetos
    self.graphics_sprite.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    
    # 3. ELIMINAR EL DESPLAZAMIENTO AUTOMÁTICO
    self.graphics_sprite.setTransformationAnchor(QGraphicsView.NoAnchor)
    self.graphics_sprite.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.graphics_sprite.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    self.graphics_sprite.setStyleSheet("background: transparent; border: none;")

    

    agregar_personaje(self)
    level_1(self,nivel)




#-------------------Sprites personajes-----------------------------

def agregar_personaje(self):
    self.frame_actual = 0
    self.acumulador_tiempo = 0.0
    self.total_frames = 13  # Aju
    # 1. Cargamos la HOJA COMPLETA (no el item todavía)
    self.sprite_sheet = QPixmap("Picture/Sprites_player/guitar_electric_sprite.png")
    
    # Definimos las medidas de cada frame que me diste
    self.frame_ancho = 239
    self.frame_alto = 343

    # 2. Creamos el Item vacío o con el primer frame
    self.personaje_item = QGraphicsPixmapItem()
    self.personaje_item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
    
    
    
    
    # 3. Lo metemos a la escena
    self.scene2.addItem(self.personaje_item)
    print(self.scene2)
    
    # 4. Mostramos el primer frame (el 0)
    actualizar_frame(self,0) 

    # 5. Posición y Escala (para que quepa en tus 180px de alto)
    self.personaje_item.setScale(0.5) # 343 * 0.5 = 171px (perfecto para 180px)
    self.personaje_item.setPos(0, 100)
    

