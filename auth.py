import hashlib
import json
import os

class Auth:
    def __init__(self, filepath="usuarios.json"):
        self.filepath = filepath
        self.usuario_actual = None
        self.perfil_actual = None

    def _hash_md5(self, texto: str) -> str:
        """Genera el hash MD5 de una cadena de texto."""
        return hashlib.md5(texto.encode('utf-8')).hexdigest()

    def _cargar_usuarios(self) -> dict:
        """Carga el fichero JSON externo con los usuarios."""
        if not os.path.exists(self.filepath):
            print(f"Error: El archivo '{self.filepath}' no existe.")
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: El archivo de usuarios está corrupto o mal formado.")
            return {}

    def login(self, usuario: str, contrasena: str) -> bool:
        """Autentica al usuario comprobando credenciales y el hash MD5."""
        usuarios = self._cargar_usuarios()
        
        if usuario in usuarios:
            pwd_hash = self._hash_md5(contrasena)
            if usuarios[usuario]["password"] == pwd_hash:
                self.usuario_actual = usuario
                self.perfil_actual = usuarios[usuario]["perfil"]
                print(f"\n¡Bienvenido/a, {self.usuario_actual}! (Perfil: {self.perfil_actual.capitalize()})")
                return True
        
        print("\n[ERROR] Usuario o contraseña incorrectos.")
        return False

    def logout(self):
        """Cierra la sesión del usuario actual."""
        if self.usuario_actual:
            print(f"\nSesión cerrada para el usuario: {self.usuario_actual}")
            self.usuario_actual = None
            self.perfil_actual = None
        else:
            print("\nNo hay ninguna sesión activa.")

    def esta_autenticado(self) -> bool:
        return self.usuario_actual is not None
