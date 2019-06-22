import csv
import json
import typing as typ


def load_data(path: str) -> typ.List[dict]:
    with open(path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [dict(item) for item in csv_reader]
        return data


def save_data(room: dict) -> None:
    results_path = 'results/rooms.json'
    with open(results_path, 'a+') as json_file:
        json_file.write(json.dumps(room, indent=4) + ',\n')
