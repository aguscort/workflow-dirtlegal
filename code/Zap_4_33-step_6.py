import json
import requests

# PARAMETERS 
input_data = { 'order': '',
    'mail' : '',
    'task_gid' : '',
    'password_shipstation' : '',
    'order_id' : '',
    'items' : '',
    'phone' : '',
    'total' : '',
    'apikey_shipstation' : ''}
# /PARAMETERS 

def add_subtask(gid, title):
    url = 'https://app.asana.com/api/1.0/tasks/' + str(gid) + '/subtasks'
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    data = {"data" : {"name": title}}
    req = requests.post(url, data=json.dumps(data), headers=headers,).json() 
    return req['data']['gid']

def update_description(gid, text):
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid)  + "?opt_fields=html_notes"
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    data = {"data" : {"html_notes": text }}
    req = requests.put(url, data=json.dumps(data), headers=headers,).json()
    return req

def get_order_by_id(id):
    items = []
    options =  []
    url = 'https://ssapi.shipstation.com/orders/' + str(id)
    req = requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json()
    for item in req['items']:
        items.append(item['name'])
        options_str = ""
        for option in item['options']:
            try: 
                options_str += "- " + option['name'] + ": " + option['value'] + "\r\n"
            except:
                options_str += ""
        options.append(options_str)        
    return req['shipTo']['street1'] + req['shipTo']['street2'], req['shipTo']['city'] + " " + req['shipTo']['state'] + " " + str(req['shipTo']['postalCode']), str(req['amountPaid']), items, options

# Build the notes field in Asana.
address1 = ""
address2 = ""
amount_paid = "" 
amount_discount = 0
items = []
options = []

address1, address2, amount_paid, items, options = get_order_by_id(input_data['order_id'])
# Get the items and variants
count = 0
for item in items:
    if item.find("Conversion") != -1 or item.find("Discount") != -1:
        pass
    else:          
        subtask_gid = add_subtask(input_data["task_gid"], "#" + str(input_data['order']) + " " + item.strip())
        update_description(subtask_gid, "<body>" + options[count] + "</body>")  
    count += 1