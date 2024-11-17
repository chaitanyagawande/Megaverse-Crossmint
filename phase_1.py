import requests
import time

class MegaverseAPI:
    BASE_URL = "https://challenge.crossmint.io/api/polyanets"

    def __init__(self, candidate_id):
        self.candidate_id = candidate_id

    def generate_polyanet(self, row, column):
        payload = {
            "candidateId": self.candidate_id,
            "row": row,
            "column": column
        }

        try:
            response = requests.post(self.BASE_URL, json=payload)
            if response.status_code == 200:
                print(f"Successfully created POLYanet at ({row}, {column})")
            else:
                print(f"Failed to create POLYanet at ({row}, {column}): {response.text}")
        except Exception as e:
            print(f"Error creating POLYanet at ({row}, {column}): {e}")

    def generate_X_shape(self):
        coordinates = [
            (2, 2), (2, 8),
            (3, 3), (3, 7),
            (4, 4), (4, 6),
            (5, 5),
            (6, 4), (6, 6),
            (7, 3), (7, 7),
            (8, 2), (8, 8)
        ]

        for row, column in coordinates:
            self.generate_polyanet(row, column)
            time.sleep(1)

if __name__ == "__main__":
    candidate_id = "0b5796d7-4603-4795-b21a-6e8e3cb526a3"
    creator = MegaverseAPI(candidate_id)
    creator.generate_X_shape()
