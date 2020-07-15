import json
import requests
from datetime import datetime, date

# PARAMETERS 
input_data = { 'task_gid':	'',
    'status_id' : '',
    'status_value' : '',
    'status_key' :'',
    'token' : ''}
# /PARAMETERS 

def update_description(gid, text):
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid)  + "?opt_fields=html_notes"
    headers = {"Content-Type" :"application/json", "Authorization": input_data['token']}
    req = requests.get(url, headers=headers,).json()    
    try:
        prev_desc = req["data"]["html_notes"].split("</body>")[0]
    except:
        prev_desc = ""
    if prev_desc.find("Renewal") == -1 and len(prev_desc) > 0 :
        data = {"data" : {"html_notes": prev_desc + "\n<b>" + text  + "</b></body>"}}
        return requests.put(url, data=json.dumps(data), headers=headers,).json()   
    else:
        return False
    
def set_task_status(gid, custom_field_id, status_id):
    url = 'https://app.asana.com/api/1.0/tasks/' + str(gid)
    headers = {"Content-Type" :"application/json", "Authorization": input_data['token']}    
    data = {"data" : {"custom_fields": { custom_field_id : status_id}}}
    return requests.put(url, data=json.dumps(data), headers=headers,).json()
    
set_task_status(input_data['task_gid'], input_data['status_key'], input_data['status_value'])
update_description(input_data['task_gid'], f"{date.today().strftime('%-m/%d')}\nLabel Printed in Shipstation (Automated)")