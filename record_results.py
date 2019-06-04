import os
import json


JSON_PATH = 'results/rooms.json'


def save_data(room: dict) -> None:
    if not os.path.isfile(JSON_PATH):
        with open(JSON_PATH, 'w') as json_file:
            json.dump([room], json_file, indent=4)
    else:
        with open(JSON_PATH) as feeds_json:
            feeds = json.load(feeds_json)
            feeds.append(room)

            with open(JSON_PATH, 'w') as json_file:
                json.dump(feeds, json_file, indent=4)
