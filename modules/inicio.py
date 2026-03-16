
import json
from modules.class_shop import Gestorshop
from modules.class_songs import GestorMenu
from PySide6.QtGui import QPixmap
import os
from PySide6.QtWidgets import QLabel,QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from modules.menu_redirect import configurar_menu_desplegable, menu_red

# modules/inicio.py


def inicio(self):
    #llamamos para iniciar el menu studio
    self.menu_actual=None
    menu_red(self,"studio")
    
    
    











