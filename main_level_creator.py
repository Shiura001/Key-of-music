import sys
import time
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QObject, QEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# Tus módulos
from modules.create_json_level import guardar_json
from modules.inicio import inicio
from modules.keys_pulse import validar_pulso

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 1. CARGA DE INTERFACES (Optimizada)
        self.loader = QUiLoader()
        
        def load_ui(path):
            f = QFile(path)
            f.open(QFile.ReadOnly)
            ui = self.loader.load(f)
            f.close()
            return ui

        self.window = load_ui("interfaz_main.ui")
        self.ui_juego = load_ui("interfaz.ui")
        self.ui_menu = load_ui("interfaz_menu.ui")

        # Limpiar StackedWidget
        while self.window.stackedWidget.count() > 0:
            self.window.stackedWidget.removeWidget(self.window.stackedWidget.widget(0))

        self.window.stackedWidget.addWidget(self.ui_menu)  # 0
        self.window.stackedWidget.addWidget(self.ui_juego) # 1
        self.window.stackedWidget.setCurrentIndex(0)

        # 2. ESTADOS DE JUEGO (Diccionarios por Carril)
        self.carriles = {1: [], 2: [], 3: [], 4: []} # Acceso rápido: self.carriles[1] es self.carril_1
        self.carril_1 = self.carriles[1]
        self.carril_2 = self.carriles[2]
        self.carril_3 = self.carriles[3]
        self.carril_4 = self.carriles[4]

        self.notas_largas_activas = {1: False, 2: False, 3: False, 4: False}
        self.teclas_pisadas = {1: False, 2: False, 3: False, 4: False}
        
        # 3. VARIABLES DE GRABACIÓN
        self.tiempos_inicio = {} 
        self.mis_notas_grabadas = []
        self.contador_notas = 1
        self.modo_creator=True
        
        # 4. CONFIGURACIÓN GENERAL
        self.gamestart = False
        self.mod_speed = 100
        self.window.setWindowTitle("Key of music")
        self.window.setWindowIcon(QIcon("icon_game.ico"))
        
        # Event Filter
        self.window.installEventFilter(self)
        self.window.setFocusPolicy(Qt.StrongFocus)
        self.window.setFocus()

    def eventFilter(self, obj, event):
        if not self.gamestart:
            return super().eventFilter(obj, event)

        # Mapeo unificado para evitar redundancia
        # Tecla: (Número de Carril, Color, Índice para validar_pulso)
        teclas_config = {
            Qt.Key_Left:  (1, "orange", 0),
            Qt.Key_Right: (2, "green",  1),
            Qt.Key_Up:    (3, "purple", 2),
            Qt.Key_Down:  (4, "yellow", 3)
        }

        # --- AL PRESIONAR ---
        if event.type() == QEvent.KeyPress and not event.isAutoRepeat():
            key = event.key()
            if key in teclas_config:
                num_carril, color, idx_validar = teclas_config[key]
                
                # Estado para el juego
                self.teclas_pisadas[num_carril] = True
                
                # Estado para la grabación (Time Stamp)
                self.tiempos_inicio[key] = self.player.position() / 1000.0
                
                # Ejecutar lógica de hit
                # Pasamos la lista correspondiente según el carril
                lista_actual = getattr(self, f"carril_{num_carril}")
                validar_pulso(self, idx_validar, lista_actual)
                
                print(f"Pulsado Carril {num_carril}")
                return True

        # --- AL SOLTAR ---
        if event.type() == QEvent.KeyRelease and not event.isAutoRepeat():
            key = event.key()
            if key in teclas_config:
                num_carril, color, _ = teclas_config[key]
                
                # 1. Resetear estados de juego
                self.teclas_pisadas[num_carril] = False
                
                # 2. Lógica de grabación de nivel
                if key in self.tiempos_inicio:
                    t_inicio = self.tiempos_inicio.pop(key)
                    t_fin = self.player.position() / 1000.0
                    
                    # Duración en milisegundos (para el JSON)
                    # Si es menor a 150ms, podrías tratarla como nota corta
                    duracion_ms = int((t_fin - t_inicio) * 100)
                    
                    # Ajuste de latencia (opcional)
                    t_ajustado = round(t_inicio - 0.05, 2)
                    
                    # Formato: [Nombre, Color, Velocidad, Duracion_ms, Carril, Tiempo_Inicio]
                    if duracion_ms>11:
                        nueva_nota = [
                            f"k{self.contador_notas}", 
                            color, 
                            300,        # Velocidad base
                            duracion_ms, 
                            num_carril, 
                            t_ajustado
                        ]
                    else:
                        nueva_nota = [
                            f"k{self.contador_notas}", 
                            color, 
                            300,        # Velocidad base
                            1, 
                            num_carril, 
                            t_ajustado
                        ]
                    
                    self.mis_notas_grabadas.append(nueva_nota)
                    self.contador_notas += 1
                    guardar_json(self)
                    print(f"Nota Grabada en Carril {num_carril}: {duracion_ms}ms")
                
                return True

        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.window.show()
    inicio(widget)
    sys.exit(app.exec())