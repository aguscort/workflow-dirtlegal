import json
import requests

# PARAMETERS 
input_data = { 'text':	'' }
# /PARAMETERS 

def continue_process(name, text):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o6wl1yy/'
    data = {"attempts" : "0", "name" : name,   "text" : input_data['text'], "wo" : "None"}
    return requests.post(url, data=json.dumps(data),)

#
# Get Data
#
text_list = str(input_data['text']).split("\r\n\r\n")
name = text_list[0].split(":")[1].strip()
continue_process(name, input_data['text'])       