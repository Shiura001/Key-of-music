from PySide6 import QtGui
from PySide6 import QtCore
from PySide6.QtGui import QColor, QPalette, QPen,QPixmap,QBrush, Qt
from PySide6.QtWidgets import QFrame
def rezise_1(self):
    self.personaje_item.setScale(0.6) # 343 * 0.5 = 171px (perfecto para 180px)
    self.personaje_item.setPos(0, 50)
    
    #self.available = QtGui.QGuiApplication.primaryScreen().availableGeometry()
    #self.window.resize(self.available.width(), self.available.height())
    #self.graphics_view.setFixedSize(self.available.width(), self.available.height())
    #self.scene.setSceneRect(0, 0, self.available.width(), self.available.height())


def rezise_carriles(self):
    if self.available.width() <= 1366 or self.available.height() <= 768:
        self.ancho_carril = 100-10
        self.alto_carril = 50-10
        tamano = self.graphics_view.size()
        ancho = tamano.width()
        alto = tamano.height()
        self.graphics_view.setFixedSize(ancho, alto+40) 
        x = self.graphics_view.x()
        y = self.graphics_view.y()
        self.graphics_view.move(x, y-30)  

        self.frame_stats = self.window.findChild(QFrame, "frame_6") 

        ancho_antes = self.frame_stats.width()
        alto_antes = self.frame_stats.height() 
        self.frame_stats.setMaximumSize(ancho_antes, alto_antes-30)
        
      

def rezise_notas(self):
    if self.available.width() <= 1366 or self.available.height() <= 768:
        self.alto_nota = 45