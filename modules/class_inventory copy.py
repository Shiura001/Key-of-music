from PySide6 import QtWidgets, QtGui, QtCore

class SongWidget(QtWidgets.QFrame):
    clicked_signal = QtCore.Signal(object) 

    def __init__(self, tema_dict, instancia_principal):
        super().__init__()

        self.instancia_principal = instancia_principal
        
        # Datos según tu estructura exacta
        self.titulo = tema_dict.get("titulo", "S/N")
        self.imagen_path = tema_dict.get("img", "")
        self.item_id = tema_dict.get("item_id", "id_null")
        self.status = tema_dict.get("status", "locked")

        # Configuración visual
        self.setFixedSize(280, 360)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        self.style_normal = """
            QFrame { 
                background-color: #1e1e1e; 
                border: 2px solid #333; 
                border-radius: 15px; 
            } 
            QFrame:hover { border: 2px solid #00d2ff; background-color: #252525; }
        """
        self.style_equipped = """
            QFrame { 
                background-color: #1e1e1e; 
                border: 2px solid #00d2ff; 
                border-radius: 15px; 
            }
        """
        self.setStyleSheet(self.style_normal)
        
        # Efecto de Opacidad para la animación de aparición
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 1. Imagen
        self.lbl_img = QtWidgets.QLabel()
        self.lbl_img.setFixedSize(240, 200)
        self.lbl_img.setScaledContents(True)
        self.lbl_img.setStyleSheet("border-radius: 10px; background-color: #000; border: none;")
        pix = QtGui.QPixmap(self.imagen_path)
        if not pix.isNull(): self.lbl_img.setPixmap(pix)

        # 2. Título
        self.lbl_titulo = QtWidgets.QLabel(self.titulo)
        self.lbl_titulo.setStyleSheet("color: white; font-size: 14px; font-weight: bold; border: none;")
        self.lbl_titulo.setAlignment(QtCore.Qt.AlignCenter)

        # 3. Botón Equipar
        self.btn_equipar = QtWidgets.QPushButton("EQUIPAR")
        self.btn_equipar.setFixedHeight(40)
        self.btn_equipar.setStyleSheet("""
            QPushButton { 
                background-color: #00d2ff; 
                color: black; 
                font-weight: bold; 
                border-radius: 10px; 
            }
            QPushButton:hover { background-color: #00b8e6; }
            QPushButton:disabled { 
                background-color: #2ecc71; 
                color: white; 
                border: none;
            }
        """)
        
        layout.addWidget(self.lbl_img, alignment=QtCore.Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.btn_equipar)

        self.btn_equipar.clicked.connect(self.click_equipar)
        self.actualizar_estado_visual()

    def aparecer(self, delay):
        """Fade-in suave"""
        self.anim = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        QtCore.QTimer.singleShot(delay, self.anim.start)

    def click_equipar(self):
        self.instancia_principal.guitar = self.item_id
        self.cambiar_sprite()
        Gestor_invertory.refrescar_interfaz()

    def cambiar_sprite(self):
        ide=self.instancia_principal.guitar
        if ide=="p1":#guitarra morad
            self.guitar_patch="Picture/Sprites_player/guitar_electric_sprite_morad.png"
        elif ide=="a_03": #peavy raptor de Dylan
            self.guitar_patch="Picture/Sprites_player/guitar_electric_sprite_dylan.png"
        elif ide=="basic":
            self.guitar_patch="Picture/Sprites_player/guitar_electric_sprite.png"
        elif ide=="a_04":
            self.guitar_patch="Picture/Sprites_player/guitar_electric_bluelight.png"
        else:
            self.guitar_patch="Picture/Sprites_player/guitar_electric_sprite.png"
        actualizar_datos(self)

    def actualizar_estado_visual(self):
        es_seleccionado = (getattr(self.instancia_principal, 'guitar', None) == self.item_id)
        if es_seleccionado:
            self.btn_equipar.setText("✔ EQUIPADO")
            self.btn_equipar.setEnabled(False)
            self.setStyleSheet(self.style_equipped)
        else:
            self.btn_equipar.setText("EQUIPAR")
            self.btn_equipar.setEnabled(True)
            self.setStyleSheet(self.style_normal)

class Gestor_invertory:
    widgets_cargados = []

    @staticmethod
    def cargar(instancia_principal, lista_datos):
        Gestor_invertory.widgets_cargados = []
        widget_contenedor = instancia_principal.ui_perfil.findChild(QtWidgets.QWidget, "layout_canciones")
        if not widget_contenedor: return

        # Limpiar layout
        if widget_contenedor.layout():
            layout_viejo = widget_contenedor.layout()
            while layout_viejo.count():
                child = layout_viejo.takeAt(0)
                if child.widget(): child.widget().deleteLater()
            grid = layout_viejo
        else:
            grid = QtWidgets.QGridLayout(widget_contenedor)
            widget_contenedor.setLayout(grid)

        grid.setSpacing(25)
        grid.setContentsMargins(20, 20, 20, 80)
        grid.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        # --- FILTRO CRÍTICO ---
        # Solo cargamos items que NO tengan status "locked"
        items_desbloqueados = [d for d in lista_datos if d.get("status") != "locked"]

        max_cols = 3
        for i, data_item in enumerate(items_desbloqueados):
            fila, col = i // max_cols, i % max_cols
            carta = SongWidget(data_item, instancia_principal)
            grid.addWidget(carta, fila, col)
            Gestor_invertory.widgets_cargados.append(carta)

        # Lanzar animaciones escalonadas
        QtWidgets.QApplication.processEvents()
        for i, carta in enumerate(Gestor_invertory.widgets_cargados):
            carta.aparecer(i * 80)

    @staticmethod
    def refrescar_interfaz():
        for carta in Gestor_invertory.widgets_cargados:
            carta.actualizar_estado_visual()


    
    



def actualizar_datos(self):
    # 'self' aquí es el SongWidget (la carta de la guitarra)
    # Necesitamos sacar los datos de la instancia_principal que guardaste en el __init__
    
    principal = self.instancia_principal 
    
    # Verificamos que los datos existan en la instancia principal antes de usarlos
    nombre_jugador = getattr(principal, 'player_name', "Jugador")
    cantidad_monedas = getattr(principal, 'money', 0)
    
    # El patch de la guitarra lo acabamos de definir en cambiar_sprite
    guitarra_seleccionada = self.guitar_patch
    self.instancia_principal.guitar_patch = guitarra_seleccionada

    nuevos_datos = {
        "usuario": nombre_jugador,
        "monedas": cantidad_monedas,
        "guitarra": guitarra_seleccionada            
    }

    # GUARDAR Y FIRMAR EL JSON
    from modules.login import RUTA_PROGRESO
    from Data.Game.game_obs.ofuscar_dat import GestorSeguridad
    
    GestorSeguridad.guardar(nuevos_datos, RUTA_PROGRESO)
    print(f"Progreso guardado: {nombre_jugador} ahora usa {guitarra_seleccionada}")