
import json
from modules.class_songs import GestorMenu
from PySide6.QtGui import QPixmap
import os
from PySide6.QtWidgets import QLabel,QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

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

    self.lbl_player_name = self.window.findChild(QToolButton, "btn_menu") 
    self.icono_hamburguesa = QIcon("Picture/icon_menupng.png") # Cambia por tu ruta
    self.lbl_player_name.setIcon(self.icono_hamburguesa)
    self.lbl_player_name.setIconSize(QSize(32, 32))
    configurar_menu_desplegable(self)




from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QToolButton
from PySide6.QtCore import Qt

def configurar_menu_desplegable(self):
    self.btn_menu = self.window.findChild(QToolButton, "btn_menu")
    
    if self.btn_menu:
        # 1. Crear el contenedor con self.window como padre para que flote
        self.menu_interno = QFrame(self.window)
        self.menu_interno.setObjectName("menu_interno")
        self.menu_interno.setFixedWidth(180) 
        self.menu_interno.setVisible(False)
        
        # 2. Ajuste de Estilo: Añadimos min-height y arreglamos el layout
        self.menu_interno.setStyleSheet("""
            #menu_interno {
                background-color: #000000;
                border: 2px solid #333333;
                border-radius: 10px;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 12px;
                text-align: left;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e1e1e;
                color: #00d2ff;
            }
        """)

        # 3. Layout: Forzamos que los botones ocupen su lugar
        layout_menu = QVBoxLayout(self.menu_interno)
        layout_menu.setContentsMargins(5, 5, 5, 5)
        layout_menu.setSpacing(2)
        
        btn_perfil = QPushButton("Estudio")
        btn_ajustes = QPushButton("Tienda")
        btn_salir = QPushButton("Salir")
        
        # Conexiones corregidas
        btn_perfil.clicked.connect(lambda: [self.mostrar_perfil(), self.menu_interno.hide()])
        btn_ajustes.clicked.connect(lambda: [self.abrir_ajustes(), self.menu_interno.hide()])
        btn_salir.clicked.connect(lambda: [self.cerrar_sesion(), self.menu_interno.hide()])
        
        layout_menu.addWidget(btn_perfil)
        layout_menu.addWidget(btn_ajustes)
        layout_menu.addWidget(btn_salir)

        # Importante: Ajustar el tamaño del frame a su contenido
        self.menu_interno.adjustSize()

        # 4. Conectar el botón
        self.btn_menu.clicked.connect(lambda: alternar_menu_interno(self))

def alternar_menu_interno(self):
    if self.menu_interno.isVisible():
        self.menu_interno.hide()
    else:
        # MAPEO DE POSICIÓN GLOBAL
        # Esto hace que el menú aparezca siempre relativo a la ventana, no al layout
        punto_global = self.btn_menu.mapTo(self.window, self.btn_menu.rect().bottomLeft())
        
        # Ajustamos: x - ancho del menú para que no se corte, y + un pequeño margen
        self.menu_interno.move(punto_global.x() - 140, punto_global.y() + 5)
        
        self.menu_interno.show()
        self.menu_interno.raise_()