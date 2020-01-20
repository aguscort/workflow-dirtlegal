import json
import requests

# PARAMETERS 
input_data = { 'item_name':	'',
    'gid':	''}
# /PARAMETERS 

def change_order_Type(gid, item_name):
    type_id = ""
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid) 
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    req = requests.get(url, headers=headers,).json()   
    for i in range(len(req["data"]["custom_fields"][1]["enum_options"])):
        if item_name.find(req["data"]["custom_fields"][1]["enum_options"][i]["name"]) != -1 and (len(type_id) < len(req["data"]["custom_fields"][1]["enum_options"][i]["name"])):
                type_id = req["data"]["custom_fields"][1]["enum_options"][i]["gid"]  
    # For SKUs SQ3325725,SQ4635264,SQ9575974
    if item_name.find("Roxor Street Legal Service") != -1: 
        type_id = "1130761583281370"                
    if type_id != "":
        data = {"data" : {"custom_fields": { "1130761583281368": type_id}}}
        return requests.put(url, data=json.dumps(data), headers=headers,).json()  

change_order_Type( input_data["gid"], input_data["item_name"])    