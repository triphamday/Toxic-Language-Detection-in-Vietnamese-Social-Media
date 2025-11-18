import os
import json


def load_json(file_path):
    """Load data from a JSON file"""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def save_json(data, file_path):
    """Save data to a JSON file"""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    