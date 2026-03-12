
import json
from modules.class_songs import GestorMenu
from PySide6.QtGui import QPixmap
import os
from PySide6.QtWidgets import QFrame, QLabel

# modules/inicio.py


def inicio(self):
    # Definimos la ruta del archivo JSON
    ruta_json = "assets/lista_canciones/list.json"
    
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, "r", encoding="utf-8") as f:
                mis_canciones = json.load(f)
            
            # Pasamos la lista cargada al GestorMenu
            GestorMenu.cargar(self, mis_canciones)
            top_side(self)
            
            
        except Exception as e:
            print(f"Error al leer el JSON: {e}")
    else:
        print("Error: No se encontró el archivo canciones.json")



def top_side(self):

    self.lbl_player_name = self.window.findChild(QLabel, "label_player_name") 
    self.lbl_player_name.setText("Player: "+self.player_name)

    self.lbl_moneda = self.window.findChild(QLabel, "label_img_monedas") 
    self.lbl_moneda.setPixmap(QPixmap('Picture/money.png'))
    self.lbl_moneda.setScaledContents(True)
    self.lbl_moneda.setStyleSheet("max-width: 20px; max-height: 20px; background-color: transparent; border: none;")




        