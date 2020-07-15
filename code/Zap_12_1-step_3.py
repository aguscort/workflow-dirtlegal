import json
import requests

# PARAMETERS 
input_data = { 'task_gid':	'',
    'project_gid' : '',
    'status_id' : '',
    'status_name' : '',
    'status_ordered_online_value' : '',
    'status_ordered_mail_value' : '',
    'status_ordered_online_key' : '',
    'status_ordered_mail_key' : '',
    'status_shipped_key' : '',
    'status_shipped_value' : ''
    'token' :''}
# /PARAMETERS 

def remove_project(task_gid, project_gid):
    url = 'https://app.asana.com/api/1.0/tasks/' + str(task_gid).strip() + '/removeProject'
    headers = {"Content-Type" :"application/json", "Authorization": input_data['token']}    
    data = {"data" : {"project": project_gid}}
    return requests.post(url, data=json.dumps(data), headers=headers,).json()

def set_task_status(gid, custom_field_id, status_id):
    url = 'https://app.asana.com/api/1.0/tasks/' + str(gid)
    headers = {"Content-Type" :"application/json", "Authorization": input_data['token']}    
    data = {"data" : {"custom_fields": { custom_field_id : status_id}}}
    return requests.put(url, data=json.dumps(data), headers=headers,).json()
    
if input_data['status_name'].find("Ordered Online") != -1:
    print(set_task_status(input_data['task_gid'], input_data['status_ordered_online_key'], input_data['status_ordered_online_value']))
elif input_data['status_name'].find("Ordered via email") != -1:
    print(set_task_status(input_data['task_gid'], input_data['status_ordered_mail_key'], input_data['status_ordered_mail_value']))
else:
    #print(set_task_status(input_data['task_gid'], input_data['status_shipped_key'], input_data['status_shipped_value']))
    pass
print(remove_project(input_data['task_gid'], input_data['project_gid']))
#print(set_task_status(input_data['task_gid'], input_data['status_ordered_mail_value'], input_data['status_ordered_mail_key']))