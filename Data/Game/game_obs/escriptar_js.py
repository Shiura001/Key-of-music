import hashlib
import json
import os

class ProteccionDatos:
    # Una palabra secreta que solo tú conoces. 
    # Si el usuario cambia el JSON, no sabrá qué "salt" usaste para el hash.
    _SALT = "MiProyectoCyberpunk_2026_Secreto"

    @staticmethod
    def _generar_hash(contenido_texto):
        """Crea una huella digital única mezclada con la palabra secreta"""
        datos_con_salt = contenido_texto + ProteccionDatos._SALT
        return hashlib.sha256(datos_con_salt.encode('utf-8')).hexdigest()

    @staticmethod
    def guardar(datos, ruta_json):
        """Guarda cualquier dato en una ruta específica y genera su firma .hash"""
        try:
            # 1. Convertir a texto JSON
            texto_json = json.dumps(datos, indent=4, ensure_ascii=False)
            
            # 2. Guardar el archivo de datos
            with open(ruta_json, "w", encoding='utf-8') as f:
                f.write(texto_json)
            
            # 3. Guardar la firma (misma ruta pero con extensión .hash)
            ruta_hash = ruta_json.rsplit('.', 1)[0] + ".hash"
            firma = ProteccionDatos._generar_hash(texto_json)
            
            with open(ruta_hash, "w", encoding='utf-8') as f:
                f.write(firma)
                
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    @staticmethod
    def cargar(ruta_json):
        """Carga datos de cualquier ruta verificando su firma .hash"""
        ruta_hash = ruta_json.rsplit('.', 1)[0] + ".hash"

        # Verificar si existen los archivos
        if not os.path.exists(ruta_json):
            return None # El archivo no existe
            
        if not os.path.exists(ruta_hash):
            print(f"ALERTA: Falta archivo de firma para {ruta_json}")
            return "TRAMPA"

        try:
            # Leer contenido
            with open(ruta_json, "r", encoding='utf-8') as f:
                texto_json = f.read()

            with open(ruta_hash, "r", encoding='utf-8') as f:
                firma_guardada = f.read().strip()

            # Validar integridad
            if ProteccionDatos._generar_hash(texto_json) == firma_guardada:
                return json.loads(texto_json)
            else:
                print(f"ALERTA: {ruta_json} ha sido modificado externamente.")
                return "TRAMPA"
        except Exception as e:
            print(f"Error al cargar: {e}")
            return "TRAMPA"