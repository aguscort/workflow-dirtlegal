import json
import requests

# PARAMETERS 
input_data = { 'text' : '',
    'supplier' : ''}
# /PARAMETERS 

import json
import requests

def add_row(sku, desc, supplier):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o5kkdt9/'
    data = {"sku" : str(sku), 'desc' : str(desc) , 'supplier' : str(supplier)}
    headers = {"Content-Type" :"application/json"} 
    return requests.post(url, headers=headers, data=json.dumps(data),).json()

text_list = str(input_data['text']).split("\n")

list_sku = []
for i in range(len(text_list)):
    if len(text_list[i]) > 0:
        if text_list[i].find("https://") != -1:
            list_sku = []
        else:
            list_sku.append(text_list[i])
        if len(list_sku) == 2:
            print(add_row(list_sku[0], list_sku[1], input_data['supplier']))