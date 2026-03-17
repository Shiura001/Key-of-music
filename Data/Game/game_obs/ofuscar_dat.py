import os
import json
import hashlib

class GestorSeguridad:
    SALT = "Mi_Clave_Secreta_Pro_2026"

    @staticmethod
    def guardar(datos_dict, ruta_archivo):
        """Guarda el diccionario dentro de una LISTA en formato .js"""
        try:
            # 1. Crear carpetas si no existen
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            # 2. Convertimos el diccionario en una LISTA []
            lista_para_guardar = [datos_dict]

            # 3. Serializar a texto JSON
            texto_js = json.dumps(lista_para_guardar, indent=4, ensure_ascii=False)
            
            # 4. Escribir archivo .js
            with open(ruta_archivo, "w", encoding='utf-8') as f:
                f.write(texto_js)
            
            # 5. Firma Digital
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
        """Lee la lista del .js y devuelve el primer diccionario"""
        ruta_hash = os.path.splitext(ruta_archivo)[0] + ".hash"

        if not os.path.exists(ruta_archivo):
            return None

        try:
            with open(ruta_archivo, "r", encoding='utf-8') as f:
                texto_js = f.read()

            if not os.path.exists(ruta_hash):
                return "TRAMPA"

            with open(ruta_hash, "r", encoding='utf-8') as f:
                firma_guardada = f.read().strip()

            firma_actual = hashlib.sha256((texto_js + GestorSeguridad.SALT).encode('utf-8')).hexdigest()

            if firma_actual == firma_guardada:
                data = json.loads(texto_js)
                # Como es una lista [{}], devolvemos solo el primer elemento
                return data[0] if isinstance(data, list) and len(data) > 0 else data
            else:
                return "TRAMPA"
        except Exception as e:
            print(f"Error al cargar: {e}")
            return "TRAMPA"