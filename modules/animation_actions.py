from PySide6.QtWidgets import QGraphicsTextItem
from PySide6.QtCore import QPropertyAnimation, QPointF, QEasingCurve, QTimer, QVariantAnimation
from PySide6.QtGui import QFont, QColor, Qt
from shiboken6 import isValid



# animacion en el momento de jugar
def mostrar_texto_flotante(self, texto, color=Qt.white, y_offset=0):
    # 1. Crear el item de texto
    item = QGraphicsTextItem(texto)
    fuente = QFont("Arial", 28, QFont.Bold)
    item.setFont(fuente)
    item.setDefaultTextColor(QColor(color))
    item.setZValue(200) # Por encima de las notas
    
    # 2. Posición inicial (Centro de la pantalla o sobre el personaje)
    # Ajusta estas coordenadas según tu layout
    pos_x = 450 
    pos_y = 100 + y_offset
    item.setPos(pos_x, pos_y)
    self.scene.addItem(item)

    # 3. Animación de Movimiento (Hacia arriba)
    anim_subir = QVariantAnimation(self)
    anim_subir.setDuration(1000)
    anim_subir.setStartValue(QPointF(pos_x, pos_y))
    anim_subir.setEndValue(QPointF(pos_x, pos_y - 100)) # Sube 100 pixeles
    anim_subir.setEasingCurve(QEasingCurve.OutExpo)
    anim_subir.valueChanged.connect(item.setPos)

    # 4. Animación de Opacidad (Fade Out)
    anim_fade = QVariantAnimation(self)
    anim_fade.setDuration(2000)
    anim_fade.setStartValue(1.0)
    anim_fade.setEndValue(0.0)
    anim_fade.valueChanged.connect(item.setOpacity)

    # 5. Limpieza automática al terminar
    anim_fade.finished.connect(lambda: self.scene.removeItem(item) if isValid(item) else None)

    # Iniciar ambas
    anim_subir.start()
    anim_fade.start()