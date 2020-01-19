import json
import requests

def continue_process(name, text):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o6wl1yy/'
    print("continue_process")
    data = {"attempts" : "0", "name" : name,   "text" : text, "wo" : "None"}
    return requests.post(url, data=json.dumps(data),)

#
# Get Data
#
text_list = str(input_data['text']).split("\r\n\r\n")
name = text_list[0].split(":")[1].strip()
print(str(text_list))

continue_process(name, input_data['text'])