import os
import json
import hashlib

class GestorSeguridad:
    SALT = "Mi_Clave_Secreta_Pro_2026"

    @staticmethod
    def guardar(datos, ruta_archivo):
        """Guarda los datos siempre dentro de una LISTA [] para mantener consistencia."""
        try:
            # Si recibimos un solo diccionario, lo envolvemos en una lista
            lista_final = datos if isinstance(datos, list) else [datos]
            
            texto_js = json.dumps(lista_final, indent=4, ensure_ascii=False)
            
            with open(ruta_archivo, "w", encoding='utf-8') as f:
                f.write(texto_js)
            
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
        """Carga la lista y la devuelve tal cual (con sus corchetes)."""
        ruta_hash = os.path.splitext(ruta_archivo)[0] + ".hash"
        if not os.path.exists(ruta_archivo): return None

        try:
            with open(ruta_archivo, "r", encoding='utf-8') as f:
                texto_js = f.read()

            if not os.path.exists(ruta_hash):
                return json.loads(texto_js)

            with open(ruta_hash, "r", encoding='utf-8') as f:
                firma_guardada = f.read().strip()

            if hashlib.sha256((texto_js + GestorSeguridad.SALT).encode('utf-8')).hexdigest() == firma_guardada:
                return json.loads(texto_js) # Retorna la LISTA [...]
            else:
                return "TRAMPA"
        except Exception as e:
            return "TRAMPA"