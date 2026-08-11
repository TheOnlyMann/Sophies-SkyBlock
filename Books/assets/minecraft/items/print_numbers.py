import json
import sys
import os


def print_slotted_types(slot,num,max=256):
    step = 10 ** (slot)
    substep = 10 ** (slot-1)
    superstep = 10 ** (slot-2)
    
    result=[]
    for i in list(range(num,max,step)):
        if superstep < 1:
            result.append(i)
        elif superstep == 1:
            submax = max
            if submax > i+ substep:
                submax = i + substep
            result.append({"min":i,"max":submax})
        elif superstep > 1:
            submax = max
            if submax > i+ substep:
                submax = i + substep
            result.append(list(range(i,submax,superstep)))
    return result

json_data = []
current_directory = os.path.dirname(__file__)
for i in range(10,0,-1):
    json_data.append({i:print_slotted_types(1,i)})
with open(current_directory + "/levels_1.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(json_data, indent=4))
json_data = []
for i in range(100,0,-10):
    json_data.append({i:print_slotted_types(2,i)})
with open(current_directory + "/levels_10.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(json_data, indent=4))
json_data = []
for i in range(200,0,-100):
    json_data.append({i:print_slotted_types(3,i)})
with open(current_directory + "/levels_100.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(json_data, indent=4))