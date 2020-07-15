import json
import requests

# PARAMETERS 
input_data = { 'workspace' : '',
    'project' : '',
    'authorization' : '',
    'item_name' : '',
    'sku' : '',
    'custom_field_key' : '',
    'custom_field_value' : '',
    'section_id' : ''}
# /PARAMETERS 

def get_tasks(workspace, project):
    url = 'https://app.asana.com/api/1.0/tasks?project='+ str(project) 
    headers = { "Authorization": input_data['authorization']}
    return requests.get(url, headers=headers,).json()

def set_task_status(gid, custom_field_id, status_id):
    url = 'https://app.asana.com/api/1.0/tasks/' + str(gid)
    headers = {"Content-Type" :"application/json", "Authorization": input_data['authorization'] }
    data = {"data" : {"custom_fields": { custom_field_id : status_id}}}
    return requests.put(url, data=json.dumps(data), headers=headers,).json()

def get_task(id):
    url = 'https://app.asana.com/api/1.0/tasks/'+ str(id) 
    headers = { "Authorization": input_data['authorization']}
    return requests.get(url, headers=headers,).json()

def get_subtask(gid):
    url = 'https://app.asana.com/api/1.0/tasks/' + str(gid) + '/subtasks'
    headers = {"Content-Type" :"application/json", "Authorization": input_data['authorization'] }
    return requests.get(url, headers=headers,).json() 

def add_subtask(gid, title):
    url = 'https://app.asana.com/api/1.0/tasks/' + str(gid) + '/subtasks'
    headers = {"Content-Type" :"application/json", "Authorization": input_data['authorization'] }
    data = {"data" : {"name": title}}
    req = requests.post(url, data=json.dumps(data), headers=headers,).json() 
    return req['data']['gid']

def add_task(workspace, title):
    url = 'https://app.asana.com/api/1.0/tasks/'
    headers = {"Content-Type" :"application/json", "Authorization": input_data['authorization'] }
    data = {"data" : {"workspace" : workspace , "name" : title }}
    req = requests.post(url, data=json.dumps(data), headers=headers,).json() 
    return req['data']['gid']

# Get the proper task
task_created = False
section_found = False
subtask_gid =  ''
memberships = []
try:
    sku = str(input_data['sku'])
except:
    sku = "##"
tasks = get_tasks(input_data['workspace'], input_data['project'])
for task in tasks['data']:
    if task['resource_type'] == 'task' and task['name'].find(sku) != -1: # Found task for SKU
        task_all = get_task(task['gid'])
        # Create subtask
        try:
            memberships = task_all['data']['memberships']            
        except:
            pass
        if len(memberships) > 0:
            for i in range(len(memberships)):
                
                if memberships[i]['section']['name'].find('Inventory Items') != -1:
                    if task_all['data']['projects'][0]['name'].find("Dirt Legal (Inventory)") != -1:
                        subtask_gid = add_subtask(task['gid'], 'Order (' + str(input_data['item_name']) + ")")
                        task_created = True
                        break

if not task_created:   #   No task exists
    #subtask_parent = add_subtask(subtask['gid'], str(input_data['item_name'])) 2020/05/12
    subtask_parent = add_task(input_data['workspace'], str(input_data['item_name']))
    # Create subtask
    subtask_gid = add_subtask(subtask_parent['gid'], 'Order (' + str(input_data['item_name']) + ")")
    print("Order created and task parent created too")
    
print(set_task_status(subtask_gid, input_data['custom_field_key'], input_data['custom_field_value']))
output= {'subtask_gid' : str(subtask_gid)}