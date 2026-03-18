import weakref
from PySide6 import QtWidgets, QtGui, QtCore

from Data.Game.game_obs.ofuscar_dat import GestorSeguridad

class ShopWidget(QtWidgets.QFrame):
    clicked_signal = QtCore.Signal(object)
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked_signal.emit(self)

    """
    Representa una sola carta de producto en la tienda.
    Incluye efectos de hover, animaciones de entrada y lógica de compra.
    """
    

    def __init__(self, tema_dict, instancia_principal, parent=None):
        super().__init__(parent)
        self.instancia_principal = instancia_principal

        
        
        # --- Datos básicos con valores predeterminados ---
        self.titulo = tema_dict.get("titulo", "Producto")
        self.imagen_path = tema_dict.get("img", "")
        self.precio = tema_dict.get("precio", 0)
        self.item_id = tema_dict.get("item_id", 0)

        # --- Configuración visual del Frame ---
        self.setFixedSize(500, 500)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        # Estilo QSS para fondo, borde y hover
        self.style_normal = """
            QFrame { 
                background-color: #1e1e1e; 
                border: 2px solid #333; 
                border-radius: 15px; 
            } 
            QFrame:hover { 
                border: 2px solid #00d2ff; 
                background-color: #252525;
            }
        """
        self.setStyleSheet(self.style_normal)
        
        # --- Diseño de Layout Vertical ---
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 1. Imagen del Item (QLabel con Pixmap)
        self.lbl_img = QtWidgets.QLabel()
        self.lbl_img.setFixedSize(350, 350)
        self.lbl_img.setScaledContents(True)
        self.lbl_img.setStyleSheet("border-radius: 10px; background-color: #000;")
        
        pix = QtGui.QPixmap(self.imagen_path)
        if not pix.isNull():
            self.lbl_img.setPixmap(pix)
        else:
            self.lbl_img.setText("Sin Imagen")
            self.lbl_img.setAlignment(QtCore.Qt.AlignCenter)

        # 2. Nombre / Título
        self.lbl_titulo = QtWidgets.QLabel(self.titulo)
        self.lbl_titulo.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none;")
        self.lbl_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_titulo.setFixedHeight(20)

        # 3. Precio
        self.lbl_precio = QtWidgets.QLabel(f"${self.precio}")
        self.lbl_precio.setStyleSheet("color: #ffcc00; font-size: 18px; font-weight: bold; border: none;")
        self.lbl_precio.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_precio.setFixedHeight(20)
        
        # 4. Botón Comprar
        self.btn_comprar = QtWidgets.QPushButton("COMPRAR")
        self.btn_comprar.setFixedHeight(40)
        self.btn_comprar.setStyleSheet("""
            QPushButton { 
                background-color: #00d2ff; 
                color: black; 
                font-weight: bold; 
                border-radius: 10px; 
                font-size: 13px;
            }
            QPushButton:hover { 
                background-color: #00a0c4; 
            }
            QPushButton:pressed {
                background-color: #007a96;
            }
        """)
        
        # Agregar elementos al layout
        layout.addWidget(self.lbl_img, alignment=QtCore.Qt.AlignCenter)
        layout.addStretch() # Empuja el contenido hacia arriba y abajo
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.lbl_precio)
        layout.addWidget(self.btn_comprar)

        # Conectar botón de compra
        self.btn_comprar.clicked.connect(self.ejecutar_compra)

        # --- LÓGICA DE ANIMACIÓN INICIAL (FADE IN Y SLIDE UP) ---
        # Efecto de opacidad
        self.opacidad_efecto = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacidad_efecto)
        self.opacidad_efecto.setOpacity(0) # Inicia invisible

        # Animación de Opacidad
        self.anim_opacidad = QtCore.QPropertyAnimation(self.opacidad_efecto, b"opacity")
        self.anim_opacidad.setDuration(500)
        self.anim_opacidad.setStartValue(0)
        self.anim_opacidad.setEndValue(1)

        # Animación de Posición (Slide Up)
        self.anim_pos = QtCore.QPropertyAnimation(self, b"pos")
        self.anim_pos.setDuration(600)
        self.anim_pos.setEasingCurve(QtCore.QEasingCurve.OutBack) # Efecto rebote suave

    def aparecer(self, delay=0):
        """Inicia las animaciones de entrada con un retraso incremental."""
        widget_ref = weakref.ref(self)

        def iniciar_animacion():
            widget = widget_ref()
            if widget is None: return

            try:
                widget.show()
                # Para carrusel horizontal, la posición final es la que Qt ya calculó en el layout.
                # Animamos la carta "saliendo" desde un poco más abajo.
                pos_final = widget.pos()
                pos_inicial = QtCore.QPoint(pos_final.x(), pos_final.y() + 40) # 40px más abajo

                widget.move(pos_inicial)

                self.anim_pos.setStartValue(pos_inicial)
                self.anim_pos.setEndValue(pos_final)

                self.anim_opacidad.start()
                self.anim_pos.start()
            except RuntimeError: return

        # Retraso progresivo para efecto cascada (izquierda a derecha)
        QtCore.QTimer.singleShot(delay, lambda: QtCore.QTimer.singleShot(10, iniciar_animacion))

    def ejecutar_compra(self):
        """Lógica de transacción y actualización de UI."""
        if self.instancia_principal.money >= self.precio:
            self.instancia_principal.money -= self.precio
            print(f"Has comprado: {self.titulo}. Saldo actual: ${self.instancia_principal.money}")
            
            # Actualizar monedas en ventana principal
            if hasattr(self.instancia_principal, 'actualizar_ui_monedas'):
                self.instancia_principal.actualizar_ui_monedas()
            self.actualizar_archivo_tienda()
            
            # Feedback de éxito
            self.btn_comprar.setText("¡OBTENIDO!")
            self.btn_comprar.setEnabled(False)
            self.btn_comprar.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")

        else:
            # Feedback de error
            self.btn_comprar.setText("MONEDAS INSUFICIENTE")
            self.btn_comprar.setStyleSheet("background-color: #f44336; color: white; border-radius: 10px;")
            QtCore.QTimer.singleShot(2000, self.restaurar_boton)
    #actualizar el JSON de la tienda
    def actualizar_archivo_tienda(self):
        ruta = "Data/Game/sj/shop.js"
        
        # 1. CARGAR: El Gestor devolverá una LISTA de diccionarios [...]
        datos_tienda = GestorSeguridad.cargar(ruta)
        
        if datos_tienda == "TRAMPA":
            print("🛑 Error de Seguridad: El hash no coincide.")
            return

        if isinstance(datos_tienda, list):
            encontrado = False
            # 2. BUSCAR Y MODIFICAR: Recorremos la lista completa
            for item in datos_tienda:
                # Comparamos IDs (usamos str para evitar errores de tipo)
                if str(item.get("item_id")) == str(self.item_id):
                    item["status"] = "unlocked" # Cambiamos el estado
                    encontrado = True
                    break
            
            if encontrado:
                # 3. GUARDAR: Enviamos la lista completa de nuevo
                # El GestorSeguridad se encargará de poner los [] y generar el .hash
                if GestorSeguridad.guardar(datos_tienda, ruta):
                    print(f"✅ shop.js actualizado: {self.titulo} ahora es 'unlocked'.")
                else:
                    print("❌ Error crítico al escribir el archivo.")
        else:
            print("❌ Error: shop.js no contiene una lista válida.")
            

    def restaurar_boton(self):
        """Restaura el estilo original del botón."""
        self.btn_comprar.setText("COMPRAR")
        self.btn_comprar.setStyleSheet("""
            QPushButton { 
                background-color: #00d2ff; 
                color: black; 
                font-weight: bold; 
                border-radius: 10px; 
            }
            QPushButton:hover { background-color: #00a0c4; }
        """)

    def mousePressEvent(self, event):
        """Emite señal al hacer clic en cualquier parte de la carta."""
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked_signal.emit(self)


# --- Gestor de la Tienda (Implementa el Carrusel con Flechas) ---
class Gestorshop:
    """
    Se encarga de crear el contenedor del carrusel, las flechas de navegación
    y cargar las cartas de productos dinámicamente.
    """
    @staticmethod
    def cargar(instancia_principal, lista_items):
        """
        Configura el carrusel interactivo en el widget contenedor de la UI.
        """
        # 1. Buscar el widget que está DENTRO del QScrollArea de la UI
        # (El layout_shopp debe ser el widget que se desplaza)
        widget_scroll_content = instancia_principal.ui_shop.findChild(QtWidgets.QWidget, "layout_shopp")
        if not widget_scroll_content: 
            print("No se encontró el widget 'layout_shopp'.")
            return

        # 2. Configurar el ScrollArea padre para navegación horizontal suave
        # Buscamos el ScrollArea padre de forma segura.
        scroll_area = widget_scroll_content.parent()
        while scroll_area and not isinstance(scroll_area, QtWidgets.QScrollArea):
            scroll_area = scroll_area.parent()

        if not scroll_area:
            print("Error: El widget 'layout_shopp' no está dentro de un QScrollArea.")
            return

        # Configuración visual del ScrollArea
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # Ocultar barra
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)   # Ocultar barra
        scroll_area.setWidgetResizable(True)                                   # Autoajuste de tamaño

        # 3. Limpiar layout anterior nativamente (Pure Python/Qt)
        if widget_scroll_content.layout():
            layout_viejo = widget_scroll_content.layout()
            while layout_viejo.count():
                child = layout_viejo.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # TRUCO NATIVO: Reparentamos el layout a un widget temporal que se destruye.
            # Esto libera al widget_scroll_content para recibir el nuevo layout.
            QtWidgets.QWidget().setLayout(layout_viejo)

        # 4. Crear el Layout Horizontal (El Carrusel)
        # Este layout alinea las cartas de izquierda a derecha sin límite horizontal.
        layout_carrusel = QtWidgets.QHBoxLayout(widget_scroll_content)
        layout_carrusel.setContentsMargins(50, 20, 50, 20) # Márgenes laterales amplios
        layout_carrusel.setSpacing(30) # Espacio entre cartas
        # Alinear a la izquierda para que empiecen al inicio del scroll
        layout_carrusel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # 5. Cargar las cartas con efecto cascada
        distancia_carta = 280 + 30 # Ancho carta + Spacing para cálculos de navegación
        for i, item_data in enumerate(lista_items):
            carta = ShopWidget(item_data, instancia_principal)
            layout_carrusel.addWidget(carta)
            
            # Ejecutar animación con retraso progresivo
            carta.aparecer(delay=i * 120) 

        # 6. IMPORTANTE: addStretch al final
        # Evita que las cartas se estiren horizontalmente si hay pocos ítems.
        layout_carrusel.addStretch()

        # 7. --- CREAR FLECHAS DE NAVEGACIÓN (Superpuestas) ---
        # Las creamos de forma nativa sobre el ScrollArea
        style_flechas = """
            QPushButton { 
                background-color: rgba(30, 30, 30, 200); 
                color: white; 
                border-radius: 25px; 
                font-size: 24px; 
                font-weight: bold; 
                border: 2px solid #555;
            }
            QPushButton:hover { background-color: rgba(0, 210, 255, 180); border-color: #00d2ff; }
            QPushButton:disabled { background-color: rgba(10, 10, 10, 100); color: #555; border: none; }
        """
        
        # Botón Flecha Izquierda
        btn_izq = QtWidgets.QPushButton("<", scroll_area)
        btn_izq.setFixedSize(50, 50)
        btn_izq.setStyleSheet(style_flechas)
        # Posicionar sobre el scrollarea (coordenadas relativas)
        btn_izq.move(10, scroll_area.height() // 2 - 25)
        btn_izq.show()

        # Botón Flecha Derecha
        btn_der = QtWidgets.QPushButton(">", scroll_area)
        btn_der.setFixedSize(50, 50)
        btn_der.setStyleSheet(style_flechas)
        btn_der.move(scroll_area.width() - 60, scroll_area.height() // 2 - 25)
        btn_der.show()

        # Guardamos referencias en instancia_principal para evitar garbage collection y repotenciar
        instancia_principal._btn_izq = btn_izq
        instancia_principal._btn_der = btn_der

        # 8. --- LÓGICA DE MOVIMIENTO CON ANIMACIÓN (QPropertyAnimation sobre la barra) ---
        # Obtenemos la barra de scroll horizontal real
        barra_horizontal = scroll_area.horizontalScrollBar()

        # Configurar la animación para la barra
        anim_scroll = QtCore.QPropertyAnimation(barra_horizontal, b"value")
        anim_scroll.setDuration(400) # Duración del desplazamiento (ms)
        anim_scroll.setEasingCurve(QtCore.QEasingCurve.OutQuad) # Suavizado al frenar
        
        # Guardar referencia de la animación
        instancia_principal._anim_scroll = anim_scroll

        # Función para actualizar el estado habilitado/deshabilitado de las flechas
        def actualizar_estado_flechas():
            # Deshabilitar izquierda si estamos al principio
            btn_izq.setEnabled(barra_horizontal.value() > barra_horizontal.minimum())
            # Deshabilitar derecha si estamos al final
            btn_der.setEnabled(barra_horizontal.value() < barra_horizontal.maximum())

        # Conectar cambios en el scroll para actualizar flechas
        barra_horizontal.valueChanged.connect(actualizar_estado_flechas)
        # Llamar inicial para configurar estado
        QtCore.QTimer.singleShot(100, actualizar_estado_flechas)

        # --- Slots para las flechas ---
        def mover_izquierda():
            # Evitar animaciones concurrentes
            if anim_scroll.state() == QtCore.QAbstractAnimation.Running: return
            valor_actual = barra_horizontal.value()
            nuevo_valor = max(valor_actual - distancia_carta, barra_horizontal.minimum())
            anim_scroll.setStartValue(valor_actual)
            anim_scroll.setEndValue(nuevo_valor)
            anim_scroll.start()

        def mover_derecha():
            if anim_scroll.state() == QtCore.QAbstractAnimation.Running: return
            valor_actual = barra_horizontal.value()
            # maximum() devuelve el límite de desplazamiento calculado por Qt
            nuevo_valor = min(valor_actual + distancia_carta, barra_horizontal.maximum())
            anim_scroll.setStartValue(valor_actual)
            anim_scroll.setEndValue(nuevo_valor)
            anim_scroll.start()

        # Conectar clics de flechas a la lógica de movimiento
        btn_izq.clicked.connect(mover_izquierda)
        btn_der.clicked.connect(mover_derecha)