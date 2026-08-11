import json
import sys
import os


'''
Utility Script to automatically generate correct models/item.json files according to folder structure
file structure:
model_id: A:B/C
create folder A, then folder 'models' and 'textures' inside A, 
then create folder B inside both folders, then create file C.json inside models/B with the following

{
	"parent": "item/generated",
	"textures":
    {
		"layer0": "model_id"
	},
	"gui_light": "front",
	"display": {}
}

C always needs to be the last part after the last / or : if no / is present in model_id
B is the part after : and before the last /
A is the part before :
}
'''

# JSON read
def load_json(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)

# JSON write
def save_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(data)

# CLI usage
if __name__ == "__main__":
    inputsize = len(sys.argv)
    #if -h or --help in args, print usage
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Usage: python generate_itemmodel.py input.json")
        print("By default, generates all item model files within lower directory from")
        print("if input.json is not specified, will use enchants.json")
        print("if -h or --help is specified, prints this help message and exits.")
        sys.exit(0)
        
    # Default filenames
    base_directory = os.path.dirname(__file__)
    #expect all textures to be within textures/item/.. *.json format
    base_directory = base_directory.replace("\\", "/")
    iteration_directory = base_directory + "/textures/item"
    parent_namespace = base_directory.rsplit("/", 1)[-1]
    model_id_list = []
    for root, dirs, files in os.walk(iteration_directory):
        for file in files:
            if file.endswith(".png"):
                #get relative path from iteration_directory
                relative_path = os.path.relpath(os.path.join(root, file), iteration_directory)
                #replace \ with / for windows compatibility
                relative_path = relative_path.replace("\\", "/")
                #remove .png extension
                model_id = relative_path[:-4]
                #split model_id into parts EG: item/ [namespace] / [item_name] type, will generate models/item/[namespace]/[item_name].json with texture layer0: item/[namespace]/[item_name]
                model_name = model_id.split("/")[-1]
                model_path = model_id.rsplit("/", 1)[0] if "/" in model_id else ""
                mkdir_path = os.path.join(base_directory, "models", "item", model_path)
                os.makedirs(mkdir_path, exist_ok=True)
                json_data = {
                    
                    "parent": "item/generated",
                    "textures":
                    {
                        "layer0": parent_namespace + ":item/" + model_id
                    },
                    "gui_light": "front",
                    "display": {}
                }
                model_id_list.append(parent_namespace + ":item/" + model_id)
                json_file_path = os.path.join(mkdir_path, model_name + ".json")
                json_file_path = json_file_path.replace("\\", "/")
                with open(json_file_path, "w", encoding="utf-8") as f:
                    f.write(json.dumps(json_data, indent=4))
    with open(base_directory + "/model_id_list.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(model_id_list, indent=4))