import json
import os

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QFrame

# Importamos la clase de seguridad que maneja JSON
from Data.Game.game_obs.ofuscar_dat import GestorSeguridad
from modules.inicio import inicio

# Definimos la ruta del archivo JSON
RUTA_PROGRESO = "Data/Game/sj/progreso.js"
RUTA_SHOP = "Data/Game/sj/shop.js"


def login(self):
    """Carga datos iniciales y construye la interfaz de login si es necesario."""
    
    # 1. INTENTO DE CARGA (JSON + HASH)
    datos_recuperados = GestorSeguridad.cargar(RUTA_PROGRESO)
    
    # Lógica de estados
    if datos_recuperados == "TRAMPA":
        print("¡Trampa detectada! Reseteando valores...")
        self.player_name = "none"
        self.money = 0
        self.guitar_patch = None
    elif datos_recuperados is None:
        # El archivo no existe (primera vez)
        self.player_name = "none"
        self.money = 0
        self.guitar_patch = None
    else:
        # Carga exitosa desde el JSON
        self.player_name = datos_recuperados.get("usuario", "none")
        self.money = datos_recuperados.get("monedas", 0)
        self.guitar_patch = datos_recuperados.get("guitarra", None)

    # 2. SALTAR SI YA ESTÁ LOGUEADO
    if self.player_name != "none":
        # Si ya existe el usuario, ejecutamos name_set para ir directo al juego
        name_set(self, self.player_name)
        return

    # 3. CONSTRUCCIÓN DE LA INTERFAZ (Solo si player_name es "none")
    frame_contenedor = self.window.findChild(QFrame, "framecentral2") 
    
    if not frame_contenedor:
        print("Error: No se encontró 'framecentral2'")
        return

    # Limpieza total del contenedor para evitar duplicados
    if frame_contenedor.layout():
        layout_viejo = frame_contenedor.layout()
        while layout_viejo.count():
            item = layout_viejo.takeAt(0)
            widget = item.widget()
            if widget: 
                widget.deleteLater()
        QtWidgets.QWidget().setLayout(layout_viejo) 

    # Layout Principal del Login
    layout = QtWidgets.QVBoxLayout(frame_contenedor)
    layout.setContentsMargins(40, 40, 40, 40)
    layout.setSpacing(20)
    layout.setAlignment(QtCore.Qt.AlignCenter)

    # Etiqueta de Título
    lbl_logo = QtWidgets.QLabel("¿COMO TE LLAMAS?")
    lbl_logo.setStyleSheet("color: #00d2ff; font-size: 24px; font-weight: bold; font-family: 'Segoe UI';")
    lbl_logo.setAlignment(QtCore.Qt.AlignCenter)

    # Campo de Entrada (Nombre)
    self.entry_nombre = QtWidgets.QLineEdit() # Lo guardamos en self para leerlo después
    self.entry_nombre.setPlaceholderText("Escribe tu nombre aquí...")
    self.entry_nombre.setFixedSize(320, 50)
    self.entry_nombre.setStyleSheet("""
        QLineEdit {
            background-color: #1a1a1a; 
            border: 2px solid #00d2ff; 
            border-radius: 15px; 
            color: white; 
            padding-left: 15px;
            font-size: 16px;
        }
        QLineEdit:focus { border: 2px solid #ffffff; }
    """)

    # Botón de Ingreso
    btn_ingresar = QtWidgets.QPushButton("INGRESAR AL JUEGO")
    btn_ingresar.setFixedSize(320, 50)
    btn_ingresar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    btn_ingresar.setStyleSheet("""
        QPushButton {
            background-color: #00d2ff; 
            color: #000; 
            font-weight: bold; 
            font-size: 14px;
            border-radius: 15px;
        }
        QPushButton:hover { background-color: #ffffff; }
    """)
    
    # Conectamos el botón a name_set
    btn_ingresar.clicked.connect(lambda: name_set(self, self.entry_nombre.text()))

    # Armado del Layout
    layout.addStretch()  
    layout.addWidget(lbl_logo)
    layout.addWidget(self.entry_nombre)
    layout.addWidget(btn_ingresar)
    layout.addStretch()

    # Mostrar todo
    frame_contenedor.show()
    frame_contenedor.update()

def name_set(self, user):
    """Guarda el nombre en el JSON y activa el menú principal."""
    # Limpiamos espacios en blanco
    user_clean = user.strip()
    
    if user_clean != "" and user_clean != "none":
        self.player_name = user_clean
        
          
        
        # Mantenemos las monedas si ya tenía, sino empezamos en 0
        monedas_actuales = getattr(self, 'money', 0)
        if self.guitar_patch is None:
            self.guitar_patch = "Picture/Sprites_player/guitar_electric_sprite.png"  # Valor por defecto si no se ha establecido

        # Estructura de DATOS (JSON compatible)
        nuevos_datos = {
            "usuario": self.player_name,
            "monedas": monedas_actuales,
            "guitarra": self.guitar_patch
        }

        # GUARDAR Y FIRMAR EL JSON
        GestorSeguridad.guardar(nuevos_datos, RUTA_PROGRESO)

        ruta_json2 = "Data/Game/sj/shop.js"
    
        if os.path.exists(ruta_json2):
            try:
                with open(ruta_json2, "r", encoding="utf-8") as f:
                    shop = json.load(f)
                    GestorSeguridad.cargar(RUTA_SHOP)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar el archivo de la tienda: {e}")  




        # Cambiar de pantalla en el StackedWidget
        if hasattr(self.window, 'stackedWidget'):
            self.window.stackedWidget.setCurrentIndex(0)
        
        # Iniciar módulos del juego
        inicio(self)
    else:
        print("Nombre no válido")