import os
import json
import hashlib

class GestorSeguridad:
    SALT = "Mi_Clave_Secreta_Pro_2026"

    @staticmethod
    @staticmethod
    def guardar(datos, ruta_archivo):
        """Guarda los datos SIEMPRE como una Lista [{}]."""
        try:
            # --- ESTA ES LA CLAVE ---
            # Si 'datos' es un diccionario {}, lo metemos en una lista []
            # Si ya es una lista [], lo dejamos como está.
            if isinstance(datos, dict):
                datos_para_guardar = [datos]
            else:
                datos_para_guardar = datos

            # Ahora serializamos 'datos_para_guardar'
            texto_js = json.dumps(datos_para_guardar, indent=4, ensure_ascii=False)
            
            with open(ruta_archivo, "w", encoding='utf-8') as f:
                f.write(texto_js)
            
            # Firma .hash
            ruta_hash = os.path.splitext(ruta_archivo)[0] + ".hash"
            firma = hashlib.sha256((texto_js + GestorSeguridad.SALT).encode('utf-8')).hexdigest()
            
            with open(ruta_hash, "w", encoding='utf-8') as f:
                f.write(firma)
            
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    @staticmethod
    def cargar(ruta_archivo):
        """Carga el archivo y devuelve el contenido tal cual es."""
        ruta_hash = os.path.splitext(ruta_archivo)[0] + ".hash"

        if not os.path.exists(ruta_archivo):
            return None

        try:
            with open(ruta_archivo, "r", encoding='utf-8') as f:
                texto_js = f.read()

            # Si no existe el hash (primera vez), permitimos la carga para firmarlo luego
            if not os.path.exists(ruta_hash):
                return json.loads(texto_js)

            with open(ruta_hash, "r", encoding='utf-8') as f:
                firma_guardada = f.read().strip()

            firma_actual = hashlib.sha256((texto_js + GestorSeguridad.SALT).encode('utf-8')).hexdigest()

            if firma_actual == firma_guardada:
                # Devolvemos el JSON completo (sea lista o dict)
                return json.loads(texto_js)
            else:
                # Si el hash no coincide, detectamos cambio manual
                print(f"DEBUG - Datos cargados: TRAMPA en {ruta_archivo}")
                return "TRAMPA"
        except Exception as e:
            print(f"Error al cargar {ruta_archivo}: {e}")
            return "TRAMPA"