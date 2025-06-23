import os
import json
from src.resources.properties import Properties as Props

class Servers: 

    _json_file: str = Props.SERVERS_DIRECTORY
    
    @staticmethod
    def _load_json():
        """
        Loads data from servers json file.
        """
        try:
            with open(Servers._json_file, "r") as file:
                return json.load(file)
            
        except FileNotFoundError:
            os.makedirs(os.path.dirname(Servers._json_file), exist_ok=True)
            with open(Servers._json_file, "w") as file:
                json.dump({"servers": []}, file)
            return {"servers": []}

    @staticmethod
    def _save_json(data):
        """
        Saves servers data in servers json file.
        """
        with open(Servers._json_file, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def get_available_servers() -> list[str]:
        """
        Lists avaialble Servers.
        """
        data = Servers._load_json()
        return [server["displayName"] for server in data["servers"]]
    
    @staticmethod
    def get_paths_in_server(server_name: str) -> list[str]:
        """
        Returns all the avaialble paths in given server.
        """
        data = Servers._load_json()

        for server in data.get("servers", []):
            if server.get("displayName") == server_name:
                return server.get("paths", [])
            
        return []
    
    @staticmethod
    def get_server_ip(display_name: str):
        data = Servers._load_json()

        for server in data.get("servers", []):
            if server.get("displayName") == display_name:
                return server.get("hostName")
            
        return None

    @staticmethod
    def add_server(display_name: str, host_name: str, paths: list[str]):
        """
        Adds or creates a new server.
        """
        data = Servers._load_json() 
        data["servers"].append({"displayName": display_name, "hostName": host_name, "paths": paths})
        Servers._save_json(data)

    @staticmethod
    def remove_server(display_name: str):
        """
        Removes an existing server.
        """
        data = Servers._load_json() 
        data["servers"] = [r for r in data["servers"] if r["displayName"] != display_name]
        Servers._save_json(data)
    
    @staticmethod
    def add_path_to_server(server_display_name: str, path: str):
        """
        Adds a path to the given server.
        """

        data = Servers._load_json()
        server = next((r for r in data["servers"] if r["displayName"] == server_display_name), None)

        if server is None:
            raise ValueError("Server does not exists.")
        
        server["paths"].append(path)
        Servers._save_json(data)

    @staticmethod
    def update_path_in_server(display_name: str, path_old: str, path_new: str):
        """
        Updates the path of the given server.
        """

        data = Servers._load_json()
        server = next((r for r in data["servers"] if r["displayName"] == display_name), None)

        index = server["paths"].index(path_old)
        server["paths"][index] = path_new

        Servers._save_json(data)

    @staticmethod
    def remove_path_in_server(display_name: str, path: str):
        """
        Updates the path of the given server.
        """

        data = Servers._load_json()
        server = next((r for r in data["servers"] if r["displayName"] == display_name), None)

        server["paths"].remove(path)

        Servers._save_json(data)

    @staticmethod
    def update_server(display_name_old: str, display_name_new: str, host_name: str, paths: list[str]):
        """
        Updates the attributes of the given server in the JSON.
        """
        data = Servers._load_json()
        server = next((r for r in data["servers"] if r["displayName"] == display_name_old), None)

        if server is None:
            raise ValueError("Server does not exist.")

        if display_name_new and display_name_new.strip():
            server["displayName"] = display_name_new

        if host_name and host_name.strip():
            server["hostName"] = host_name

        if isinstance(paths, list):
            server["paths"] = paths

        Servers._save_json(data)

    @staticmethod
    def clear_servers():
        """
        Clears all the servers.
        """
        data = {"servers": []}
        Servers._save_json(data)
