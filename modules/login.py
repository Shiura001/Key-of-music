from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QFrame

from Data.Game.game_obs.ofuscar_dat import cargar_progreso, guardar_progreso
from modules.inicio import inicio

def login(self):
    datos_recuperados = cargar_progreso(password=123)
    nombre_jugador = datos_recuperados["usuario"]
    cantidad_monedas = datos_recuperados["monedas"]
    self.player_name=nombre_jugador
    self.money=cantidad_monedas
    if self.player_name=="none":
        pass
    else:
        name_set(self,self.player_name)

    self.player_name=None
    
    # Buscamos el frame contenedor
    frame_contenedor = self.window.findChild(QFrame, "framecentral2") 
    
    if not frame_contenedor:
        print("Error: No se encontró 'framecentral'")
        return

    # 1. LIMPIEZA TOTAL
    if frame_contenedor.layout():
        layout_viejo = frame_contenedor.layout()
        while layout_viejo.count():
            item = layout_viejo.takeAt(0)
            widget = item.widget()
            if widget: 
                widget.deleteLater()
        
        # Truco para eliminar el layout anterior definitivamente
        QtWidgets.QWidget().setLayout(layout_viejo) 

    # 2. Creamos un QVBoxLayout nuevo
    layout = QtWidgets.QVBoxLayout(frame_contenedor)
    layout.setContentsMargins(40, 40, 40, 40)
    layout.setSpacing(20)
    layout.setAlignment(QtCore.Qt.AlignCenter)

    # 3. Etiqueta de Título
    lbl_logo = QtWidgets.QLabel("Como te llamas?")
    lbl_logo.setStyleSheet("color: #00d2ff; font-size: 22px; font-weight: bold;")
    lbl_logo.setAlignment(QtCore.Qt.AlignCenter)

    # 4. Campo de Entrada
    self_entry_nombre = QtWidgets.QLineEdit()
    self_entry_nombre.setPlaceholderText("Nombre de usuario...")
    self_entry_nombre.setFixedSize(300, 45)
    self_entry_nombre.setStyleSheet("background-color: #1a1a1a; border: 2px solid #333; border-radius: 10px; color: white; padding-left: 15px;")

    # 5. Botón de Ingreso
    self_btn_ingresar = QtWidgets.QPushButton("INGRESAR")
    self_btn_ingresar.setFixedSize(300, 45)
    self_btn_ingresar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    self_btn_ingresar.setStyleSheet("background-color: #00d2ff; color: black; font-weight: bold; border-radius: 10px;")
    self_btn_ingresar.clicked.connect(lambda: name_set(self,self_entry_nombre.text()))

    # 6. ARMADO DEL LAYOUT
    layout.addStretch()  
    layout.addWidget(lbl_logo)
    layout.addWidget(self_entry_nombre)
    layout.addWidget(self_btn_ingresar)
    layout.addStretch()

    # --- LAS LÍNEAS QUE HACEN QUE APAREZCA ---
    lbl_logo.show()
    self_entry_nombre.show()
    self_btn_ingresar.show()
    
    frame_contenedor.show() # Por las dudas si el frame estaba oculto
    frame_contenedor.update() # Refresco visual forzado

    return self_entry_nombre, self_btn_ingresar

def name_set(self,user):
    if user!="":
        self.player_name=user
        nuevos_datos = {
            "usuario": self.player_name,
            "monedas": 0
        }

        # 3. Sobrescribimos el archivo .dat
        guardar_progreso(nuevos_datos, password=123)
        self.window.stackedWidget.setCurrentIndex(0)
        
        inicio(self)
