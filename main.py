import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer, Qt, QObject, QEvent
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtGui import QIcon
from modules.inicio import inicio
from modules.keys_pulse import validar_pulso
from modules.level_1 import animar_neon_especial, desactivar_especial
from modules.login import login

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()



        # ----------------------------
        # LIMPIAR STACKEDWIDGET
        # ----------------------------
        
        #interfaz main
        self.loader = QUiLoader()
        self.main_file = QFile("interfaz_main.ui")
        self.main_file.open(QFile.ReadOnly)
        self.window = self.loader.load(self.main_file)
        self.main_file.close()
        self.window.setFixedSize(1200, 900) 

        while self.window.stackedWidget.count() > 0:
            widget_to_remove = self.window.stackedWidget.widget(0)
            self.window.stackedWidget.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()


        #interfaz level
        self.game_file = QFile("interfaz.ui")
        self.game_file.open(QFile.ReadOnly)
        self.ui_juego = self.loader.load(self.game_file)
        self.game_file.close()

        # 3. Interfaz menu
        self.menu_file = QFile("interfaz_menu.ui") # Debes crear este .ui
        self.menu_file.open(QFile.ReadOnly)
        self.ui_menu = self.loader.load(self.menu_file)
        self.menu_file.close()

        self.login_file = QFile("login.ui") # Debes crear este .ui
        self.login_file.open(QFile.ReadOnly)
        self.ui_login = self.loader.load(self.login_file)
        self.login_file.close()

        #agrega lista para las keys de cada carril
        self.carril_1=[]
        self.carril_2=[]
        self.carril_3=[]
        self.carril_4=[]

        self.modo_creator=False
        # para saber si estas en modo creador de nivel

        #modo especial
        
        self.modo_especial: False


        #agregar interfaces al principal
        self.window.stackedWidget.addWidget(self.ui_menu)  # Índice 0
        self.window.stackedWidget.addWidget(self.ui_juego)#Índice 1
        self.window.stackedWidget.addWidget(self.ui_login) # Índice 2
        self.window.stackedWidget.setCurrentIndex(2)

        #-------------------------------------------------
        self.window.setWindowTitle("Key of music")
        self.window.setWindowIcon(QIcon("icon_game.ico"))
        self.carril_activo = None
        self.presionando = False
        self.gamestart=False
        self.notas_largas_activas = {1: False, 2: False, 3: False, 4: False}
        self.teclas_pisadas = {1: False, 2: False, 3: False, 4: False} #cuando se esta ejecutando una key larga
        self.duracion_inicio_nota=None
        #########################################
        import time #probando
        self.last_audio_pos = 0
        self.last_sys_time = time.time()

        ################################
        #velocidad modificada
        self.mod_speed=50
        ###################################
        # --- LA SOLUCIÓN DEFINITIVA: EVENT FILTER ---
        # Instalamos un filtro que vigila TODO lo que pasa en la ventana
        self.window.installEventFilter(self)
        
        # Forzamos foco total
        self.window.setFocusPolicy(Qt.StrongFocus)
        self.window.setFocus()
########################################################################################################


#       Configuracion de botones
#       Acciones al presionar teclas
#
#               |      |
#               |      |
#               |      |
#               |      |
#         ______|      |______
#         \                  /
#          \                /
#           \              /
#            \            /
#             \          /
#              \        /
#               \      /
#                \    /
#                 \  /
#                  \/



    def eventFilter(self, obj, event):
        if self.gamestart:
            # --- PRESIONAR TECLA ---
            if event.type() == QEvent.KeyPress:
                if not event.isAutoRepeat():
                    key = event.key()
                    if key == Qt.Key_Space:
                        if self.special_listo == True:
                            if not self.modo_especial: # Solo si no está ya activo
                                self.audio_output_esp = QAudioOutput()
                                self.audio_output_esp.setVolume(100)
                                self.player_esp = QMediaPlayer()
                                self.player_esp.setAudioOutput(self.audio_output_esp)
                                audio_special="assets/sound_effect/special.wav"
                                self.player_esp.setSource(QUrl.fromLocalFile(audio_special))
                                self.player_esp.play()

                                self.modo_especial = True
                                animar_neon_especial(self, True)


                                # Programamos el apagado automático tras 10 segundos
                                # Asegúrate de que 'desactivar_especial' sea accesible
                                QTimer.singleShot(10000, lambda: desactivar_especial(self))

                                print("¡MODO PANTHER ACTIVADO!")
                        return True # Consumimos el evento
                    # Diccionario para mapear teclas a índices de carril (0-3) y listas
                    mapeo = {
                        Qt.Key_Left:  (0, self.carril_1),
                        Qt.Key_Right: (1, self.carril_2),
                        Qt.Key_Up:    (2, self.carril_3),
                        Qt.Key_Down:  (3, self.carril_4)
                    }
    
                    if key in mapeo:
                        idx, lista = mapeo[key]
                        num_carril = idx + 1
                        
                        # 1. Marcamos ESTA tecla como pisada
                        self.teclas_pisadas[num_carril] = True
                        
                        # 2. Validamos el pulso inicial
                        validar_pulso(self, idx, lista)
                        
                        print(f"DEBUG: Carril {num_carril} PISADO")
                        return True
    
            # --- SOLTAR TECLA ---
            if event.type() == QEvent.KeyRelease:
                if not event.isAutoRepeat():
                    key = event.key()
                    mapeo_soltar = {
                        Qt.Key_Left:  1,
                        Qt.Key_Right: 2,
                        Qt.Key_Up:    3,
                        Qt.Key_Down:  4
                    }
    
                    if key in mapeo_soltar:
                        num_carril = mapeo_soltar[key]
                        
                        # 1. Marcamos solo ESTA tecla como suelta
                        self.teclas_pisadas[num_carril] = False
                        
                        print(f"DEBUG: Carril {num_carril} SOLTADO")
                        return True
        
        return super().eventFilter(obj, event)
#########################################################################################################






#########################################################################################################




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.window.show()
    
    
    # Iniciamos el juego
    login(widget)
    #inicio(widget)

    sys.exit(app.exec())
    