import json
import os
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QFrame

# Importamos la clase de seguridad que maneja JSON
from Data.Game.game_obs.ofuscar_dat import GestorSeguridad
from modules.inicio import inicio

# Definimos las rutas
RUTA_PROGRESO = "Data/Game/sj/progreso.js"
RUTA_SHOP = "Data/Game/sj/shop.js"

def login(self):
    """Carga datos iniciales y construye la interfaz de login si es necesario."""
    
    # 1. INTENTO DE CARGA (JSON + HASH)
    datos_recuperados = GestorSeguridad.cargar(RUTA_PROGRESO)
    
    if isinstance(datos_recuperados, list) and len(datos_recuperados) > 0:
        progreso_real = datos_recuperados[0] # Sacamos el objeto de la lista
        self.player_name = progreso_real.get("usuario", "none")
    else:
        # --- LÓGICA DE LISTA DE DICCIONARIOS ---
        # Si es una lista [...], extraemos el primer objeto { }
        if isinstance(datos_recuperados, list) and len(datos_recuperados) > 0:
            progreso_real = datos_recuperados[0]
        else:
            progreso_real = datos_recuperados # Por si acaso fuera un dict directo

        # Ahora podemos usar .get() sin errores
        if isinstance(progreso_real, dict):
            self.player_name = progreso_real.get("usuario", "none")
            self.money = progreso_real.get("monedas", 0)
            self.guitar_patch = progreso_real.get("guitarra", "Picture/Sprites_player/guitar_electric_sprite.png")
        else:
            self.player_name = "none"

    # 2. SALTAR SI YA ESTÁ LOGUEADO
    if self.player_name != "none":
        name_set(self, self.player_name)
        return

    # 3. CONSTRUCCIÓN DE LA INTERFAZ (Si no hay usuario)
    frame_contenedor = self.window.findChild(QFrame, "framecentral2") 
    if not frame_contenedor: return

    # Limpieza del layout anterior
    if frame_contenedor.layout():
        layout_viejo = frame_contenedor.layout()
        while layout_viejo.count():
            item = layout_viejo.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        QtWidgets.QWidget().setLayout(layout_viejo) 

    layout = QtWidgets.QVBoxLayout(frame_contenedor)
    layout.setAlignment(QtCore.Qt.AlignCenter)

    lbl_logo = QtWidgets.QLabel("¿CÓMO TE LLAMAS?")
    lbl_logo.setStyleSheet("color: #00d2ff; font-size: 24px; font-weight: bold;")

    self.entry_nombre = QtWidgets.QLineEdit()
    self.entry_nombre.setPlaceholderText("Escribe tu nombre aquí...")
    self.entry_nombre.setFixedSize(320, 50)
    self.entry_nombre.setStyleSheet("background-color: #1a1a1a; border: 2px solid #00d2ff; border-radius: 15px; color: white; padding-left: 15px;")

    btn_ingresar = QtWidgets.QPushButton("INGRESAR AL JUEGO")
    btn_ingresar.setFixedSize(320, 50)
    btn_ingresar.setStyleSheet("background-color: #00d2ff; color: #000; font-weight: bold; border-radius: 15px;")
    btn_ingresar.clicked.connect(lambda: name_set(self, self.entry_nombre.text()))

    layout.addStretch()  
    layout.addWidget(lbl_logo, alignment=QtCore.Qt.AlignCenter)
    layout.addWidget(self.entry_nombre, alignment=QtCore.Qt.AlignCenter)
    layout.addWidget(btn_ingresar, alignment=QtCore.Qt.AlignCenter)
    layout.addStretch()

def name_set(self, user):
    """Guarda el nombre en formato Lista de Diccionarios y activa el juego."""
    user_clean = user.strip()
    
    if user_clean != "" and user_clean != "none":
        self.player_name = user_clean
        self.money = getattr(self, 'money', 200000)
        
        if not hasattr(self, 'guitar_patch') or self.guitar_patch is None:
            self.guitar_patch = "Picture/Sprites_player/guitar_electric_sprite.png"

        # ESTRUCTURA: Diccionario que irá dentro de la lista
        nuevos_datos = {
            "usuario": self.player_name,
            "monedas": self.money,
            "guitarra": self.guitar_patch
        }

        # GUARDAR: El GestorSeguridad (arreglado) lo envolverá en [ ] automáticamente
        GestorSeguridad.guardar(nuevos_datos, RUTA_PROGRESO)

        # SINCRONIZAR TIENDA: Crear el hash si no existe
        if os.path.exists(RUTA_SHOP):
            datos_shop = GestorSeguridad.cargar(RUTA_SHOP)
            if datos_shop == "TRAMPA" or datos_shop is None:
                # Si no tiene hash o está mal, lo re-firmamos con el contenido actual
                try:
                    with open(RUTA_SHOP, "r", encoding="utf-8") as f:
                        contenido = json.load(f)
                    GestorSeguridad.guardar(contenido, RUTA_SHOP)
                    print("✅ Tienda sincronizada y firmada.")
                except:
                    print("❌ Error crítico en shop.js")

        if hasattr(self.window, 'stackedWidget'):
            self.window.stackedWidget.setCurrentIndex(0)
        
        inicio(self)
    else:
        print("Nombre no válido")