import base64
import json
import hashlib
import hmac
import os
from cryptography.fernet import Fernet


class SaveSystem:
    def __init__(self, base_path="Data/Game/game_obs/"):

        self.base_path = base_path
        self.meta_path = f"{base_path}progress.meta"

        self.BASE_KEY = b'PON_AQUI_TU_CLAVE_FERNET'

        # 🔐 clave base estable
        master = hashlib.sha256(self.BASE_KEY).digest()

        # 🔐 Fernet key
        self.fernet_key = base64.urlsafe_b64encode(master)
        self.fernet = Fernet(self.fernet_key)

        # 🔐 HMAC anti modificación externa
        self.hmac_key = hashlib.sha256(master + b"GAME_SAVE_HMAC").digest()

        os.makedirs(self.base_path, exist_ok=True)

        # 📊 cargar meta (ENCRIPTADA)
        self.meta = self._cargar_meta()

    # =========================================================
    # 📊 META (ENCRIPTADA)
    # =========================================================

    def _cargar_meta(self):
        if not os.path.exists(self.meta_path):
            return {"max_progress": 0}

        try:
            with open(self.meta_path, "rb") as f:
                data = self.fernet.decrypt(f.read())
                return json.loads(data.decode())
        except:
            return {"max_progress": 0}

    def _guardar_meta(self):
        data = json.dumps(self.meta).encode()
        encrypted = self.fernet.encrypt(data)

        with open(self.meta_path, "wb") as f:
            f.write(encrypted)

    # =========================================================
    # 🔐 HASH EXTERNO
    # =========================================================

    def _generar_hash(self, datos):
        return hmac.new(self.hmac_key, datos, hashlib.sha256).hexdigest()

    # =========================================================
    # 💾 GUARDAR
    # =========================================================

    def guardar(self, data, slot=1):

        ruta_dat = f"{self.base_path}save_{slot}.dat"
        ruta_hash = f"{self.base_path}save_{slot}.hash"
        ruta_backup = f"{self.base_path}save_{slot}.bak"

        # 🔥 progreso incremental anti rollback
        data["progress_id"] = self.meta["max_progress"] + 1

        # 🧠 firma interna anti clon/modificación
        temp_copy = dict(data)
        raw_signature = f"{data['progress_id']}:{json.dumps(temp_copy, sort_keys=True)}"
        data["signature"] = hashlib.sha256(raw_signature.encode()).hexdigest()

        # 🔐 serializar + encriptar
        datos_binarios = json.dumps(data).encode()
        datos_encriptados = self.fernet.encrypt(datos_binarios)

        # 💾 backup
        if os.path.exists(ruta_dat):
            os.replace(ruta_dat, ruta_backup)

        # 💾 guardar save
        with open(ruta_dat, "wb") as f:
            f.write(datos_encriptados)

        # 🔐 hash externo
        with open(ruta_hash, "w") as f:
            f.write(self._generar_hash(datos_encriptados))

        # 📊 actualizar meta si corresponde
        if data["progress_id"] > self.meta["max_progress"]:
            self.meta["max_progress"] = data["progress_id"]
            self._guardar_meta()

    # =========================================================
    # 📥 CARGAR
    # =========================================================

    def cargar(self, slot=1):

        ruta_dat = f"{self.base_path}save_{slot}.dat"
        ruta_hash = f"{self.base_path}save_{slot}.hash"
        ruta_backup = f"{self.base_path}save_{slot}.bak"

        if not os.path.exists(ruta_dat):
            return None

        try:
            # 📂 leer archivo
            with open(ruta_dat, "rb") as f:
                datos_encriptados = f.read()

            # 🔐 verificar hash externo
            with open(ruta_hash, "r") as f:
                hash_guardado = f.read()

            if self._generar_hash(datos_encriptados) != hash_guardado:
                raise Exception("Archivo modificado (HMAC falló)")

            # 🔓 decrypt
            datos_binarios = self.fernet.decrypt(datos_encriptados)
            data = json.loads(datos_binarios.decode())

            # 🧠 verificar firma interna
            signature = data.get("signature")
            temp = dict(data)
            temp.pop("signature", None)

            raw_signature = f"{data.get('progress_id', 0)}:{json.dumps(temp, sort_keys=True)}"
            expected = hashlib.sha256(raw_signature.encode()).hexdigest()

            if signature != expected:
                raise Exception("Save manipulado (firma inválida)")

            # ⛔ anti rollback global
            progress_id = data.get("progress_id", 0)

            if progress_id < self.meta["max_progress"]:
                raise Exception("Rollback detectado (save viejo)")

            return data

        except Exception as e:
            print("⚠️ Error:", e)

            # 💾 restore backup automático
            if os.path.exists(ruta_backup):
                os.replace(ruta_backup, ruta_dat)
                return self.cargar(slot)

            return None