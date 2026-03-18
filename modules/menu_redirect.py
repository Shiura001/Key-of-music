from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize
import json
import os

from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QToolButton, QVBoxLayout, QMenu

from modules.class_inventory import Gestor_invertory
from modules.class_shop import Gestorshop
from modules.class_songs import GestorMenu

# reconfiguramos el boton menu para que se cambie de interfaz
def menu_red(self,menu):
#############acceder al menu estudio->
    if menu=="studio" and self.menu_actual!="studio":
        self.menu_actual="studio"
        self.window.stackedWidget.setCurrentIndex(0)
        
        estudio_interfaz(self)
############# acceder al menu shop->
    if menu=="shop" and self.menu_actual!="shop":
        self.menu_actual="shop"
        self.window.stackedWidget.setCurrentIndex(3)
        
        shop_interfaz(self)

    if menu=="perfil" and self.menu_actual!="perfil":
        self.menu_actual="perfil"
        self.window.stackedWidget.setCurrentIndex(4)
        
        perfil_interfaz(self)






def estudio_interfaz(self):
    ruta_json = "assets/lista_canciones/list.json"
    
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, "r", encoding="utf-8") as f:
                mis_canciones = json.load(f)

             # Pasamos la lista cargada al GestorMenu
            GestorMenu.cargar(self, mis_canciones)
            top_side(self,"studio")


        except Exception as e:
            print(f"Error al leer el JSON: {e}")
    else:
        print("Error: No se encontró el archivo canciones.json")


        
def shop_interfaz(self):
    ruta_json2 = "Data/Game/sj/shop.js"
    
    if os.path.exists(ruta_json2):
        try:
            with open(ruta_json2, "r", encoding="utf-8") as f:
                shop = json.load(f)
                
                Gestorshop.cargar(self,shop)     
                top_side(self,"shop")

                
            # Pasamos la lista cargada al GestorMenu
            
        except Exception as e:
            print(f"Error al leer el JSON: {e}")
    else:
        print("Error: No se encontró el archivo canciones.json")   

def perfil_interfaz(self): 
    ruta_json2 = "Data/Game/sj/shop.js"
    if os.path.exists(ruta_json2):
        try:
            with open(ruta_json2, "r", encoding="utf-8") as f:
                inventario = json.load(f)
                Gestor_invertory.cargar(self, inventario)
                top_side(self,"perfil")
                
            
        except Exception as e:
            print(f"Error al leer el JSON: {e}")

    
    






    
#menu desplegable
def configurar_menu_desplegable(self, ui):
    if hasattr(self, 'menu_interno'):
        self.menu_interno.hide()
    if ui == "studio":
        self.lbl_menu = self.ui_menu.findChild(QToolButton, "btn_menu")
        self.btn_menu = self.ui_menu.findChild(QToolButton, "btn_menu")
        

    if ui == "shop":
        self.lbl_menu = self.ui_shop.findChild(QToolButton, "btn_menu") 
        self.btn_menu = self.ui_shop.findChild(QToolButton, "btn_menu")
    if ui == "perfil":
        self.lbl_menu = self.ui_perfil.findChild(QToolButton, "btn_menu") 
        self.btn_menu = self.ui_perfil.findChild(QToolButton, "btn_menu")

    

    
    self.icono_hamburguesa = QIcon("Picture/icon_menu.png") # Cambia por tu ruta
    self.lbl_menu.setIcon(self.icono_hamburguesa)
    self.lbl_menu.setIconSize(QSize(32, 32))
        
    
        
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
            
            btn_studio = QPushButton("Estudio")
            btn_shop = QPushButton("Tienda")
            btn_perfil = QPushButton("Perfil")
            
            # Conexiones corregidas
            btn_studio.clicked.connect(lambda: [menu_red(self,"studio"), self.menu_interno.hide()])
            btn_shop.clicked.connect(lambda: [menu_red(self,"shop"), self.menu_interno.hide()])
            btn_perfil.clicked.connect(lambda: [menu_red(self,"perfil"), self.menu_interno.hide()])
            
            layout_menu.addWidget(btn_studio)       
            layout_menu.addWidget(btn_shop)
            layout_menu.addWidget(btn_perfil)
    
            # Importante: Ajustar el tamaño del frame a su contenido
            self.menu_interno.adjustSize()
    
            # 4. Conectar el botón (evitar múltiples conexiones)
            try:
                self.btn_menu.clicked.disconnect()
            except Exception:
                pass
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


#configurar el topside monedas perfil, menu
def top_side(self,ui):
    if ui == "studio":
        self.lbl_player_name = self.ui_menu.findChild(QLabel, "label_player_name") 
        self.lbl_player_name.setText("Player: " + str(self.player_name))
        self.lbl_moneda = self.ui_menu.findChild(QLabel, "label_img_monedas")
        self.lbl_money = self.ui_menu.findChild(QLabel, "label_money") 
        self.lbl_money.setText("Monedas: " + str(self.money))

        
    if ui == "shop":
        self.lbl_player_name = self.ui_shop.findChild(QLabel, "label_player_name") 
        self.lbl_player_name.setText("Player: " + str(self.player_name or "Unknown"))
        self.lbl_moneda = self.ui_shop.findChild(QLabel, "label_img_monedas")
    if ui == "perfil":
        self.lbl_player_name = self.ui_perfil.findChild(QLabel, "label_player_name") 
        self.lbl_player_name.setText("Player: " + str(self.player_name or "Unknown"))
        self.lbl_moneda = self.ui_perfil.findChild(QLabel, "label_img_monedas")

    
    self.lbl_moneda.setPixmap(QPixmap('Picture/money.png'))
    self.lbl_moneda.setScaledContents(True)
    self.lbl_moneda.setStyleSheet("max-width: 20px; max-height: 20px; background-color: transparent; border: none;")
        

    
    configurar_menu_desplegable(self, ui)