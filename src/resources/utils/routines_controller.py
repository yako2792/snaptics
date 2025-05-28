import os
import json
from src.resources.properties import Properties as Props

class Routines: 

    _json_file: str = Props.ROUTINES_DIRECTORY
    
    @staticmethod
    def _load_json():
        """
        Loads data from routines json file.
        """
        try:
            with open(Routines._json_file, "r") as file:
                return json.load(file)
            
        except FileNotFoundError:
            os.makedirs(os.path.dirname(Routines._json_file), exist_ok=True)
            with open(Routines._json_file, "w") as file:
                json.dump({"routines": []}, file)
            return {"routines": []}

    @staticmethod
    def _save_json(data):
        """
        Saves routines data in routines json file.
        """
        with open(Routines._json_file, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def get_available_routines() -> list[str]:
        """
        Lists avaialble routines.
        """
        data = Routines._load_json()
        return [routine["name"] for routine in data["routines"]]
    
    @staticmethod
    def get_stages_in_routine(routine_name: str) -> list[str]:
        """
        Returns all the avaialble stages in given routine.
        """
        data = Routines._load_json()
        routine = next((r for r in data["routines"] if r["name"] == routine_name), None) 
        if routine is None:
            raise ValueError("Routine does not exists.")
        return [f"Stage {i+1}: {routine['stages'][i]['type']}" for i in range(len(routine["stages"]))]

    @staticmethod
    def get_stage_type(routine_name: str, stage_number: int) -> str:
        """
        Returns the stage type for the given stage in given routine.
        """
        data = Routines._load_json()
        routine = next((r for r in data["routines"] if r["name"] == routine_name), None)

        if routine is None:
            raise ValueError("Routine does not exists.")
        
        stages = routine["stages"]
        if stage_number < 0 or stage_number > len(stages):
            raise ValueError("Stage does not exists.")
        
        return stages[stage_number - 1]["type"]

    @staticmethod
    def get_stage_config(routine_name:str, stage_number: int) -> dict[str, str]:
        """
        Returns the configurations in given stage.
        """
        data = Routines._load_json()
        routine = next((r for r in data["routines"] if r["name"] == routine_name), None)

        if routine is None:
            raise ValueError("Routine does not exists.")
        
        stages = routine["stages"]
        if stage_number < 1 or stage_number > len(stages):
            raise ValueError("Stage does not exists.")
        
        return stages[stage_number - 1]["config"]

    @staticmethod
    def add_routine(routine_name: str, stages: list[dict]):
        """
        Adds or creates a new routine.
        """
        data = Routines._load_json() 
        data["routines"].append({"name": routine_name, "stages": stages})
        Routines._save_json(data)

    @staticmethod
    def remove_routine(routine_name: str):
        """
        Removes an existing routine.
        """
        data = Routines._load_json() 
        data["routines"] = [r for r in data["routines"] if r["name"] != routine_name]
        Routines._save_json(data)

    @staticmethod
    def update_routine(routine_name: str, stages: list[dict]):
        """
        Updates the stages of the given routine.
        """
        data = Routines._load_json() 
        routine = next((r for r in data["routines"] if r["name"] == routine_name), None)

        if routine is None:
            raise ValueError("Routine does not exists.")
        
        routine["stages"] = stages
        Routines._save_json(data)
