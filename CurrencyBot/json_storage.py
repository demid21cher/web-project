import json


FILE = "bank.json"


def save_operation(data):
    with open(FILE, "r") as file:
        try:
            existing = json.load(file)
        except:
            existing = []

    existing.append(data)

    with open(FILE, "w") as file:
        json.dump(existing, file, indent=4)


def read_operations():
    with open(FILE, "r") as file:
        data = json.load(file)

        return data
