import os
import json
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from src.resources.properties import Properties as Props

load_dotenv(".env")

class Credentials: 

    _json_file: str = Props.CREDENTIALS_DIRECTORY
    
    @staticmethod
    def _load_json():
        """
        Loads data from credentials json file.
        """
        try:
            with open(Credentials._json_file, "r") as file:
                return json.load(file)
            
        except FileNotFoundError:
            os.makedirs(os.path.dirname(Credentials._json_file), exist_ok=True)
            with open(Credentials._json_file, "w") as file:
                json.dump({"credentials": []}, file)
            return {"credentials": []}

    @staticmethod
    def _save_json(data):
        """
        Saves credentials data in servers json file.
        """
        with open(Credentials._json_file, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def get_available_users() -> list[str]:
        """
        Lists avaialble users in credentials.
        """
        data = Credentials._load_json()
        return [credential["user"] for credential in data["credentials"]]
    
    @staticmethod
    def get_user_password(user_name: str):
        data = Credentials._load_json()

        for credential in data.get("credentials", []):
            if credential.get("user") == user_name:
                return credential.get("password")
            
        return None

    @staticmethod
    def add_user_and_password(user_name: str, password: str):
        """
        Adds or creates a new user.
        """
        data = Credentials._load_json() 
        data["credentials"].append({"user": user_name, "password": password})
        Credentials._save_json(data)

    @staticmethod
    def remove_user(user_name: str):
        """
        Removes an existing user.
        """
        data = Credentials._load_json() 
        data["credentials"] = [r for r in data["credentials"] if r["user"] != user_name]
        Credentials._save_json(data)

    @staticmethod
    def update_password_in_user(user_name: str, new_password: str):
        """
        Updates the password of the given user.
        """

        data = Credentials._load_json()
        user = next((r for r in data["credentials"] if r["user"] == user_name), None)

        user["password"] = new_password

        Credentials._save_json(data)
    
    @staticmethod
    def update_username_in_user(user_name_old: str, user_name_new: str):
        """
        Updates the username of the given user.
        """

        data = Credentials._load_json()
        user = next((r for r in data["credentials"] if r["user"] == user_name_old), None)

        user["user"] = user_name_new

        Credentials._save_json(data)

    @staticmethod
    def encrypt_password(password: str):
        """
        Encrypt given password
        """
        key = os.getenv('KEY')
        key = key.encode()
        f = Fernet(key)
        encrypted = f.encrypt(password.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt_password(encrypted_password: str) -> str:
        """
        Decrypt given password
        """
        key = os.getenv('KEY')
        key = key.encode()
        f = Fernet(key)
        decrypted = f.decrypt(encrypted_password.encode())
        return decrypted.decode()

    @staticmethod
    def clear_credentials():
        """
        Clears all credentials.
        """
        data = {"credentials": []}
        Credentials._save_json(data)


