
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsRectItem
from PySide6.QtGui import QPen, QRadialGradient, QBrush, QColor
from PySide6.QtCore import Qt, QTimer





#Valida cada pulsacion para cada acción
def validar_pulso(self, carril, carril_key): 
    # carril: 0, 1, 2, 3...
    # carril_key: la lista de notas del carril (self.carril_1, etc.)
    
    num_carril = carril + 1 # Convertimos a 1, 2, 3, 4 para los efectos y diccionarios

    if carril_key:
        # 1. Verificamos colisión con el receptor del carril correspondiente
        if carril_key[0].graphics.collidesWithItem(self.carriles[carril]): 
            
            # CASO NOTA CORTA (Duration 1)
            if carril_key[0].duration == 1:
                efecto_hit(self, num_carril) # Brillo instantáneo con Timer
                self.scene.removeItem(carril_key[0].graphics)
                carril_key.pop(0)

                if self.combo >= 30:
                    self.multiplier = 4
                elif self.combo >= 20:
                    self.multiplier = 3
                elif self.combo >= 10:
                    self.multiplier = 2
                else:
                    self.multiplier = 1

                if self.combo==30:
                    aplicar_temblor(self.label_multi, intensidad=12, duracion=500)
                    aplicar_temblor(self.graphics_view, intensidad=3, duracion=500)
                if self.combo==20:
                    aplicar_temblor(self.label_multi, intensidad=12, duracion=500)
                if self.combo==10:
                    aplicar_temblor(self.label_multi, intensidad=12, duracion=500)



                
                
                self.label_multi.setText(f"x{self.multiplier}")
                self.points += 10 * self.multiplier
                self.label_points.setText(str(self.points))

                self.combo += 1 
                self.label_combo.setText(str(self.combo))
                print(f"Nice en carril {num_carril}")
                self.audio_output_miss.setVolume(100)
            
            # CASO NOTA LARGA (Duration > 1)
            else:
                # Marcamos que este carril específico tiene una nota larga activa
                self.notas_largas_activas[num_carril] = True
                
                # Registramos que la tecla física está siendo presionada
                # (Importante para que slide_key sepa cuándo detenerse)
                self.teclas_pisadas[num_carril] = True 
                
                # Estos se mantienen por si los usas en otra parte, 
                # pero el motor ahora se guiará por 'notas_largas_activas'
                self.key_push = True
                self.carril_activo = carril 
                self.carril_key_activo = carril_key 
                
        else:
            self.combo=0
            self.label_combo.setText(str(self.combo))
            self.multiplier = 1
            self.label_multi.setText(f"x{self.multiplier}")
            print(f"Fallaste en carril {num_carril}: nota fuera de rango")



#animacion de hit

def efecto_hit(self, num_carril, sostenido=False):
    if not hasattr(self, 'brillos_activos'):
        self.brillos_activos = {}

    if num_carril in self.brillos_activos:
        return 

    carril_obj = self.carriles[num_carril - 1]
    colores = ["red", "green", "purple", "yellow"]

    brillo = QGraphicsRectItem(carril_obj.boundingRect())
    brillo.setPos(carril_obj.pos())
    brillo.setBrush(QBrush(QColor(colores[num_carril - 1])))
    brillo.setPen(QPen(QColor("white"), 3))
    brillo.setZValue(10)
    brillo.setOpacity(0.5) 
    
    self.scene.addItem(brillo)
    self.brillos_activos[num_carril] = brillo

    if not sostenido:
        # Aquí usamos la función de abajo pasándole self
        QTimer.singleShot(80, lambda: limpiar_brillo(self, num_carril))

def limpiar_brillo(self, num_carril):
    if hasattr(self, 'brillos_activos'):
        item = self.brillos_activos.pop(num_carril, None)
        if item:
            try:
                self.scene.removeItem(item)
            except:
                pass






from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve

def aplicar_temblor(widget, intensidad=5, duracion=400):
    # Guardamos la posición original para volver a ella al final
    pos_original = widget.pos()
    
    # Creamos la animación para la propiedad 'pos'
    anim = QPropertyAnimation(widget, b"pos")
    anim.setDuration(duracion)
    
    # Definimos puntos intermedios (KeyValues) para el movimiento loco
    # Cuantos más puntos, más "caótico" se ve el temblor
    import random
    for i in range(1, 10):
        offset_x = random.randint(-intensidad, intensidad)
        offset_y = random.randint(-intensidad, intensidad)
        anim.setKeyValueAt(i / 10, pos_original + QPoint(offset_x, offset_y))
    
    # Al final siempre vuelve a la posición original
    anim.setEndValue(pos_original)
    
    # Usamos una curva suave para que no sea tan tosco
    anim.setEasingCurve(QEasingCurve.OutQuad)
    
    # ¡Importante! Guardar una referencia para que no la borre el recolector de basura
    widget.shake_anim = anim 
    anim.start()