import json
import sys
import os

def read_json(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_json(input_file):
    current_directory = os.path.dirname(__file__)
    return read_json(current_directory + "/" + input_file)

def enchant_level_module():
    level_data = load_json("enchant_levels.json")
    level_format = {
            "type": "minecraft:condition",
            "property": "minecraft:component",
            "predicate": "stored_enchantments",
            "value": [],
            "on_true": {
                "type": "minecraft:model",
            },
            "on_false": {
                "type": "minecraft:model",
            }
    }
    format_pointer = level_format
    fallback_method = {
        "type": "minecraft:empty"
    }
    for model, level in level_data.items():
        if level == "fallback":
            fallback_method = {
                "type": "minecraft:model",
                "model": model
            }
        else:
            format_pointer.update({
                "type": "minecraft:condition",
                "property": "minecraft:component",
                "predicate": "stored_enchantments",
                "value": [
                    {
                        "levels":level
                    }
                ],
                "on_true": {
                    "type": "minecraft:model",
                    "model": model
                },
                "on_false": {
                    "type": "minecraft:model",
                }
            })
            format_pointer = format_pointer["on_false"]
    format_pointer.update(fallback_method)
    return json.dumps(level_format, indent=4)

def enchant_type_module(json_name="enchant_types.json"):
    type_data = load_json(json_name)
    type_format = {
            "type": "minecraft:condition",
            "property": "minecraft:component",
            "predicate": "stored_enchantments",
            "value": [],
            "on_true": {
                "type": "minecraft:model",
            },
            "on_false": {
                "type": "minecraft:model",
            }
    }
    format_pointer = type_format
    fallback_method = {
        "type": "minecraft:empty"
    }
    for model, enchant_type in type_data.items():
        if enchant_type == "fallback":
            fallback_method = {
                "type": "minecraft:model",
                "model": model
            }
        else:
            format_pointer.update({
                "type": "minecraft:condition",
                "property": "minecraft:component",
                "predicate": "stored_enchantments",
                "value": [
                    {
                        "enchantments":enchant_type
                    }
                ],
                "on_true": {
                    "type": "minecraft:model",
                    "model": model
                },
                "on_false": {
                    "type": "minecraft:model",
                }
            })
            format_pointer = format_pointer["on_false"]
    format_pointer.update(fallback_method)
    return json.dumps(type_format, indent=4)

def enchant_composite_module(*args):
    composite_format = {
        "type": "minecraft:composite",
        "models":[
            
        ]
    }
    to_list = []
    for arg in args:
        to_list.append(json.loads(arg))
    composite_format["models"] = to_list
    return json.dumps(composite_format, indent=4)

def enchant_finish_module(total_data):
    total_format = {
        "model": {
        }
    }
    total_format["model"] = json.loads(total_data)
    return json.dumps(total_format, indent=4)

def export_json(json_data, output_file="enchanted_book.json"):
    current_directory = os.path.dirname(__file__)
    with open(current_directory + "/" + output_file, "w", encoding="utf-8") as f:
        f.write(json_data)

#print(enchant_level_module())
#print(load_json("enchant_types.json"))
#print(enchant_type_module())
#print(enchant_composite_module(enchant_level_module(), enchant_type_module()))
#print(enchant_finish_module(enchant_level_module()))

json_read = [
    "enchant_types.json",
    "enchant_meleeranged.json"
]
json_stuff =[]
for json_file in json_read:
    json_stuff.append(enchant_type_module(json_file))
export_json(enchant_finish_module(enchant_composite_module(*json_stuff, enchant_level_module())))