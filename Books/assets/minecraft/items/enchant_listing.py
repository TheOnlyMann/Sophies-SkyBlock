import json
import sys
import os



json_data = []
current_directory = os.path.dirname(__file__)

with open(current_directory + "/enchant_list.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
with open(current_directory + "/enchant_convert.json", "w", encoding="utf-8") as f:
    f.write("{\n")
    for enchant in json_data:
        f.write("\"sophie:item/enchant_books/\" : \"" + enchant + "\",\n")
    f.write("}")