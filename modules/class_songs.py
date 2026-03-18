from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from modules.client import get_leaderboard
from modules.game_start import game_start_level
from shiboken6 import isValid

class SongWidget(QtWidgets.QFrame):
    clicked_signal = QtCore.Signal(object) 

    def __init__(self, titulo, imagen_path, audio_present_path, audio_path, nivel_recibido, instrument_path, status, index, callback_jugar, instancia_principal):
        super().__init__()
        self.instancia_principal = instancia_principal
        self.status = status 
        self.costo = 500

        self.index = index
        self.audio_present = audio_present_path
        self.audio_path = audio_path
        self.callback_jugar = callback_jugar
        self.instrument_path = instrument_path
        
        self.setFixedSize(300, 370)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        self.style_normal = "QFrame { background-color: #1e1e1e; border: 2px solid #333; border-radius: 15px; } QFrame:hover { border: 2px solid #555; }"
        self.style_selected = "QFrame { background-color: #252525; border: 2px solid #00d2ff; border-radius: 15px; }"
        self.setStyleSheet(self.style_normal)
        
        layout = QtWidgets.QVBoxLayout(self)
        self.lbl_img = QtWidgets.QLabel()
        self.lbl_img.setFixedSize(260, 240)
        self.lbl_img.setScaledContents(True)
        self.lbl_img.setStyleSheet("border: none; border-radius: 10px; background-color: #000;")
        
        pix = QtGui.QPixmap(imagen_path)
        if not pix.isNull(): self.lbl_img.setPixmap(pix)

        self.lbl_titulo = QtWidgets.QLabel(titulo)
        self.lbl_titulo.setStyleSheet("color: white; font-size: 14px; font-weight: bold; border: none;")
        self.lbl_titulo.setAlignment(QtCore.Qt.AlignCenter)

        self.label_leaderboards=QtWidgets.QLabel("")
        self.label_leaderboards.setStyleSheet("color: white; font-size: 13px; font-weight: bold; border: none;")
        self.label_leaderboards.setAlignment(QtCore.Qt.AlignCenter)
        self.label_leaderboards.setVisible(False) 
        self.label_leaderboards.setFixedHeight(50)
        
        self.btn_jugar = QtWidgets.QPushButton("JUGAR")
        self.btn_jugar.setFixedHeight(35)
        self.btn_jugar.setVisible(False) 
        self.btn_jugar.setStyleSheet("QPushButton { background-color: #00d2ff; color: black; font-weight: bold; border-radius: 5px; }")
        self.level_data = nivel_recibido 
        
        self.btn_jugar.clicked.connect(lambda: self.callback_jugar(self))
        
        layout.addWidget(self.lbl_img, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.label_leaderboards)
        layout.addWidget(self.btn_jugar)

        # --- CAPA DE BLOQUEO (OVERLAY) ---
        self.overlay_bloqueo = QtWidgets.QFrame(self)
        self.overlay_bloqueo.setGeometry(0, 0, 300, 370)
        self.overlay_bloqueo.setStyleSheet("background-color: rgba(0, 0, 0, 180); border-radius: 15px;")
        
        layout_overlay = QtWidgets.QVBoxLayout(self.overlay_bloqueo)
        
        self.icon_candado = QtWidgets.QLabel("🔒")
        self.icon_candado.setStyleSheet("font-size: 50px; background: transparent; border: none;")
        self.icon_candado.setAlignment(QtCore.Qt.AlignCenter)
        
        self.btn_comprar = QtWidgets.QPushButton("COMPRAR")
        self.btn_comprar.setFixedSize(120, 40)
        self.btn_comprar.setStyleSheet("""
            QPushButton { background-color: #ffcc00; color: black; font-weight: bold; border-radius: 20px; }
            QPushButton:hover { background-color: #ffe066; }
        """)
        
        layout_overlay.addStretch()
        layout_overlay.addWidget(self.icon_candado, alignment=QtCore.Qt.AlignCenter)
        layout_overlay.addWidget(self.btn_comprar, alignment=QtCore.Qt.AlignCenter)
        layout_overlay.addStretch()

        self.btn_comprar.clicked.connect(self.intentar_compra)
        self.actualizar_estado_bloqueo()

    def intentar_compra(self):
        if self.instancia_principal.money >= self.costo:
            self.instancia_principal.money -= self.costo
            self.status = "disponible" 
            self.actualizar_estado_bloqueo()
            print(f"Compra exitosa de {self.index}")
        else:
            print("No tienes suficiente dinero")

    def actualizar_estado_bloqueo(self):
        bloqueado = self.status == "locked"
        self.overlay_bloqueo.setVisible(bloqueado)
        self.btn_jugar.setEnabled(not bloqueado)

    def set_active(self, active):
     # Importación local por seguridad

    # 1. Verificamos que los botones y labels existan en C++ antes de usarlos
        if hasattr(self, 'btn_jugar') and isValid(self.btn_jugar):
            if self.status != "locked":
                self.btn_jugar.setVisible(active)
            else:
                self.btn_jugar.setVisible(False)
    
        if hasattr(self, 'label_leaderboards') and isValid(self.label_leaderboards):
            if self.status != "locked":
                self.label_leaderboards.setVisible(active)
            else:
                self.label_leaderboards.setVisible(True) # Mensaje de bloqueo
    
        # 2. El setStyleSheet se aplica al objeto 'self' (la carta)
        # Solo lo aplicamos si la carta misma sigue siendo válida
        if isValid(self):
            self.setStyleSheet(self.style_selected if active else self.style_normal)
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked_signal.emit(self)

class GestorMenu:
    carta_activa = None 
    player = None
    audio_output = None
    
    fade_timer = None
    stop_timer = None 
    
    volumen_actual = 0.0
    es_fade_in = True 

    @staticmethod
    def cargar(instancia_principal, lista_canciones):
        if GestorMenu.player is None:
            GestorMenu.player = QMediaPlayer()
            GestorMenu.audio_output = QAudioOutput()
            GestorMenu.player.setAudioOutput(GestorMenu.audio_output)
            
            GestorMenu.fade_timer = QtCore.QTimer()
            GestorMenu.fade_timer.timeout.connect(GestorMenu.procesar_fade)
            
            GestorMenu.stop_timer = QtCore.QTimer()
            GestorMenu.stop_timer.setSingleShot(True)
            GestorMenu.stop_timer.timeout.connect(GestorMenu.iniciar_fade_out)

        widget_contenedor = instancia_principal.ui_menu.findChild(QtWidgets.QWidget, "layout_canciones")
        if not widget_contenedor: return

        if widget_contenedor.layout():
            layout_viejo = widget_contenedor.layout()
            while layout_viejo.count():
                child = layout_viejo.takeAt(0)
                if child.widget(): child.widget().deleteLater()
            QtWidgets.QWidget().setLayout(layout_viejo)

        grid = QtWidgets.QGridLayout(widget_contenedor)
        grid.setSpacing(20)

        def manejar_seleccion(carta_clic):
            # Reset total al cambiar de carta
            GestorMenu.player.stop()
            GestorMenu.fade_timer.stop()
            GestorMenu.stop_timer.stop()
            
            GestorMenu.volumen_actual = 0.0
            GestorMenu.audio_output.setVolume(0.0)
            GestorMenu.es_fade_in = True

            if GestorMenu.carta_activa and GestorMenu.carta_activa != carta_clic:
                GestorMenu.carta_activa.set_active(False)
            
            carta_clic.set_active(True)
            GestorMenu.carta_activa = carta_clic

            # --- CORRECCIÓN: Solo reproducir si NO está bloqueada ---
            if carta_clic.status != "locked":
                upadate_leaderboards(carta_clic.level_data, carta_clic)
                if carta_clic.audio_present:
                    GestorMenu.player.setSource(QtCore.QUrl.fromLocalFile(carta_clic.audio_present))
                    # Damos 200ms para asegurar que el buffer cargue la duración del archivo
                    QtCore.QTimer.singleShot(200, lambda: GestorMenu.reproducir_con_limite())
            else:
                carta_clic.label_leaderboards.setText("Contenido Bloqueado")
                carta_clic.label_leaderboards.setVisible(True)

        def ejecutar_juego(carta_seleccionada):
            if GestorMenu.carta_activa:
                instancia_principal.audio_actual = GestorMenu.carta_activa.audio_path
                instancia_principal.level_actual = carta_seleccionada.level_data
                instancia_principal.instrumento_actual = carta_seleccionada.instrument_path 
                instancia_principal.status = carta_seleccionada.status 

            GestorMenu.player.stop()
            GestorMenu.fade_timer.stop()
            GestorMenu.stop_timer.stop()
            instancia_principal.window.stackedWidget.setCurrentIndex(1)
            game_start_level(instancia_principal, carta_seleccionada.level_data)

        max_cols = 3
        for i, tema in enumerate(lista_canciones):
            fila, col = i // max_cols, i % max_cols
            carta = SongWidget(tema["titulo"], tema["img"], tema["audio_present"], tema["pista"], tema["level"], tema["instrument"], tema["status"], i, ejecutar_juego, instancia_principal)
            carta.clicked_signal.connect(manejar_seleccion)
            grid.addWidget(carta, fila, col)

    @staticmethod
    def reproducir_con_limite():
        # Primero posición, luego Play
        GestorMenu.player.setPosition(30000) # 30 segundos
        GestorMenu.player.play()
        
        GestorMenu.es_fade_in = True
        GestorMenu.fade_timer.start(50)
        GestorMenu.stop_timer.start(15000) # Duración de 15 segundos

    @staticmethod
    def iniciar_fade_out():
        GestorMenu.es_fade_in = False
        GestorMenu.fade_timer.start(50)

    @staticmethod
    def procesar_fade():
        if GestorMenu.es_fade_in:
            if GestorMenu.volumen_actual < 0.6:
                GestorMenu.volumen_actual += 0.04
                GestorMenu.audio_output.setVolume(GestorMenu.volumen_actual)
            else:
                GestorMenu.fade_timer.stop()
        else:
            if GestorMenu.volumen_actual > 0.01:
                GestorMenu.volumen_actual -= 0.04
                GestorMenu.audio_output.setVolume(GestorMenu.volumen_actual)
            else:
                GestorMenu.fade_timer.stop()
                GestorMenu.player.stop()

def upadate_leaderboards(id_cancion, carta):
    carta.label_leaderboards.setText("Conectando al servidor...")
    carta.label_leaderboards.setVisible(True)

    try:
        result = get_leaderboard(id_cancion)
        if result and isinstance(result, list):
            top_3 = result[:3] 
            texto_final = ""
            iconos = {1: "🥇", 2: "🥈", 3: "🥉"}
            for i, jugador in enumerate(top_3, 1):
                icono = iconos.get(i, "")
                texto_final += f"{icono} {jugador['player']} - {jugador['score']}\n"
            carta.label_leaderboards.setText(texto_final)
        else:
            carta.label_leaderboards.setText("Sin puntajes aún")
    except Exception as e:
        carta.label_leaderboards.setText("⚠️ Servidor Offline")