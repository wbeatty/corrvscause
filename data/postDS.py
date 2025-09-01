import json

import requests

url = "http://localhost:3000/api/datasets"


def main():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            datasets = data["datasets"]
    except FileNotFoundError:
        print("Data file not found")
        return
    for dataset in datasets:
        x = requests.post(url, json=dataset)
        print(x.text)


if __name__ == "__main__":
    main()
