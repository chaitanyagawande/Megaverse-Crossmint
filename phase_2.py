import requests
import time

class AstralObject:
    def __init__(self, api, row, column):
        self.api = api
        self.row = row
        self.column = column

    def create(self):
        raise NotImplementedError("This method should be implemented in subclasses")

class POLYanet(AstralObject):
    def create(self):
        self.api.generate_object("polyanets", self.row, self.column)

class Soloon(AstralObject):
    def __init__(self, api, row, column, color):
        super().__init__(api, row, column)
        self.color = color

    def create(self):
        self.api.generate_object("soloons", self.row, self.column, color=self.color)

class Cometh(AstralObject):
    def __init__(self, api, row, column, direction):
        super().__init__(api, row, column)
        self.direction = direction

    def create(self):
        self.api.generate_object("comeths", self.row, self.column, direction=self.direction)

class MegaverseAPI:
    BASE_URL = "https://challenge.crossmint.io/api"

    def __init__(self, candidate_id):
        self.candidate_id = candidate_id

    def get_goal_map(self):
        url = f"{self.BASE_URL}/map/{self.candidate_id}/goal"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get goal map: {response.text}")
            return None

    def generate_object(self, object_type, row, column, **kwargs):
        payload = {
            "candidateId": self.candidate_id, 
            "row": row, 
            "column": column
        }
        payload.update(kwargs)

        response = requests.post(f"{self.BASE_URL}/{object_type}", json=payload)
        if response.status_code == 200:
            print(f"Successfully created {object_type} at ({row}, {column})")
        else:
            print(f"Failed to create {object_type} at ({row}, {column}): {response.text}")

class MegaverseCreator:
    def __init__(self, api):
        self.api = api
        self.object_map = {
            "POLYANET": lambda row, col: POLYanet(api, row, col),
            "SOLOON": lambda row, col, color: Soloon(api, row, col, color),
            "COMETH": lambda row, col, direction: Cometh(api, row, col, direction),
        }

    def build_map(self, goal_map):
        for row_index, row in enumerate(goal_map['goal']):
            for col_index, cell in enumerate(row):
                self.generate_object_for(cell, row_index, col_index)
                

    def generate_object_for(self, cell, row, column):
        if cell == "SPACE":
            return
        
        if cell == "POLYANET":
            obj = self.object_map["POLYANET"](row, column)
        elif cell.endswith("SOLOON"):
            color = cell.split("_")[0].lower()
            obj = self.object_map["SOLOON"](row, column, color)
        elif cell.endswith("COMETH"):
            direction = cell.split("_")[0].lower()
            obj = self.object_map["COMETH"](row, column, direction)
        
        obj.create()
        time.sleep(1)

if __name__ == "__main__":
    candidate_id = "0b5796d7-4603-4795-b21a-6e8e3cb526a3"
    api = MegaverseAPI(candidate_id)
    builder = MegaverseCreator(api)

    goal_map = api.get_goal_map()
    if goal_map:
        builder.build_map(goal_map)
