import os
import json


def save_data(room: dict) -> None:
    results_path = 'results/rooms.json'

    if not os.path.isfile(results_path):
        with open(results_path, 'w') as json_file:
            json.dump([room], json_file, indent=4)
    else:
        with open(results_path) as feeds_json:
            feeds = json.load(feeds_json)
            feeds.append(room)

            with open(results_path, 'w') as json_file:
                json.dump(feeds, json_file, indent=4)
