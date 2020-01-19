
import json
import requests
import re, random
from datetime import datetime, timedelta


def date_treatment():
    # Date treatment
    datetoday = datetime.utcnow() #- timedelta(hours=8)
    date_lastweek = datetoday - timedelta(days=7)
    try:
        datetoday_lastmonth = (datetoday - timedelta(days=datetoday.day)).replace(day=datetoday.day)
    except ValueError:
        datetoday_lastmonth = datetoday.replace(month=datetoday.month, day=1) - timedelta(days=1)        
    datetoday = datetoday.strftime('%Y-%m-%d')        
    date_lastweek = date_lastweek.strftime('%Y-%m-%d')
    datetoday_lastmonth = datetoday_lastmonth.strftime('%Y-%m-%d')
    return datetoday, date_lastweek, datetoday_lastmonth

def get_task_by_id(id):
    url = 'https://app.asana.com/api/1.0/workspaces/1122730176672819/tasks/search?completed=false'
    headers = {"Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    return requests.get(url, headers=headers,).json()

def continue_process(attempts, name, text, wo):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o6wl1yy/'
    print("continue_process")
    data = {"attempts" : attempts, "name" : name,   "text" : text, "wo" : wo}
    return requests.post(url, data=json.dumps(data),)

def get_tasks():
    url = 'https://app.asana.com/api/1.0/workspaces/1122730176672819/tasks/search?completed=false'
    headers = { "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    return requests.get(url, headers=headers,).json()

def add_story(gid, text):
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid) + '/stories'
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    data = {"data" : {"text": text}}
    return requests.post(url, data=json.dumps(data), headers=headers,).json()

def update_description(gid, text):
    #'Vehicle Registration Renewal'
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid)  + "?opt_fields=html_notes"
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    req = requests.get(url, headers=headers,).json()    
    prev_desc = req["data"]["html_notes"].split("</body>")[0]
    if prev_desc.find("Renewal") == -1:
        print(prev_desc)
        data = {"data" : {"html_notes": prev_desc + "\n<b>" + text  + "</b></body>"}}
        return requests.put(url, data=json.dumps(data), headers=headers,).json()        

def change_order_Type(gid, item_name):
    type_id = ""
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid) 
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    req = requests.get(url, headers=headers,).json()   
    for i in range(len(req["data"]["custom_fields"][1]["enum_options"])):
        if item_name.find(req["data"]["custom_fields"][1]["enum_options"][i]["name"]) != -1:
            type_id = req["data"]["custom_fields"][1]["enum_options"][i]["gid"]
            break
    if type_id != "":
        data = {"data" : {"custom_fields": { "1130761583281368": type_id}}}
        return requests.put(url, data=json.dumps(data), headers=headers,).json()     

def get_orders_period(created_at_min, created_at_max):
    url = 'https://ssapi.shipstation.com/orders?createDateStart=' + created_at_min + '&createDateEnd=' + created_at_max + '&pageSize=500'        
    return requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json()

def get_customers(page = 1):
    url = 'https://ssapi.shipstation.com/customers?page=' + str(page) + '&pageSize=500&SortBy=ModifyDate&sortDir=Asc'        
    customers, total, page, pages = requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json().values()
    return customers, total, page, pages

def get_all_orders_customer(customerName):
    url = 'https://ssapi.shipstation.com/orders?customerName=' + str(customerName)  + '&sortBy=OrderDate&sortDir=Desc&pageSize=500'
    return requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json()

def get_orders_customer(customerName, created_at_min, created_at_max):
    url = 'https://ssapi.shipstation.com/orders?customerName=' + str(customerName) + '&createDateStart=' + created_at_min + '&createDateEnd=' + created_at_max + '&pageSize=500'
    return requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json()

def get_order_number(order_raw):
    if len(order_raw) == 3:
        order = 'E' + order_raw
    elif len(order_raw) == 4:
        order = order_raw
    else:
        order = order_raw
        order = re.sub(r'-', '', order)
    return order

def get_folders(path, cursor = None):
    req = ''
    data = {"path": path, "recursive": False}
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer " + input_data["dropbox_token"]}
    if cursor != None:
        entries, cursor, has_more = requests.post('https://api.dropboxapi.com/2/files/list_folder/continue', headers=headers, data={"cursor": cursor}).json().value()
    else:
        entries, cursor, has_more = requests.post('https://api.dropboxapi.com/2/files/list_folder', headers=headers, data=json.dumps(data),).json().values()
    return entries, cursor, has_more


def create_folder(name):
    req = ''
    data = {"path": name.strip(), "autorename": False}
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer " + input_data["dropbox_token"]}
    req = requests.post('https://api.dropboxapi.com/2/files/create_folder_v2', headers=headers, data=json.dumps(data),).json()
    return req

def exhaustive_search(path):
    list_folder = []
    entries, cursor, has_more = get_folders(path)
    list_folder = entries
    while has_more:
        entries, cursor, has_more = get_folders(path, cursor)
        list_folder.extend(entries)
    else:
        return list_folder

def exhaustive_customer_search():
    customers = []
    t_customers, total, page, pages = get_customers()
    customers.extend(t_customers)
    while page <= pages:         
        t_customers, total, page, pages = get_customers(page+1)
        customers.extend(t_customers)
    else:
        return customers

def get_order_by_id(id):
    url = 'https://ssapi.shipstation.com/orders?createDateStart=' + created_at_min + '&createDateEnd=' + created_at_max + '&pageSize=500'        
    return requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json()

    
#datetoday, date_lastweek, datetoday_lastmonth = date_treatment()

    # {'gid': '1130761583281374', 'color': 'none', 'enabled': True, 'name': 'Lien', 'resource_type': 'enum_option'}
    # {'gid': '1130765891421629', 'color': 'none', 'enabled': True, 'name': 'VT', 'resource_type': 'enum_option'}
    # {'gid': '1130761583281371', 'color': 'none', 'enabled': True, 'name': 'UT', 'resource_type': 'enum_option'}
    # {'gid': '1130761583281373', 'color': 'aqua', 'enabled': True, 'name': 'Renewal/Dup Title', 'resource_type': 'enum_option'}
    # {'gid': '1133133725261464', 'color': 'none', 'enabled': True, 'name': 'VT > AZ', 'resource_type': 'enum_option'}
    # {'gid': '1132974097861500', 'color': 'none', 'enabled': True, 'name': 'VT > UT', 'resource_type': 'enum_option'}
    # {'gid': '1146626261361355', 'color': 'none', 'enabled': True, 'name': 'VT > SD', 'resource_type': 'enum_option'}
    # {'gid': '1130761583281376', 'color': 'none', 'enabled': True, 'name': 'AZ', 'resource_type': 'enum_option'}
    # {'gid': '1130761583281372', 'color': 'none', 'enabled': True, 'name': 'MT', 'resource_type': 'enum_option'}
# change_order_Type(str(1153906503176026), "Dirt Bike Conversion -VT MCO")


# def create_asana_task_for_product(ship_to_name, order, customer_email, ship_to_phone, order_total, date, items_sku, items_name):
#     req = requests.get('https://hooks.zapier.com/hooks/catch/4834230/otoh0ip/',params={"ship_to_name" : ship_to_name, "order" : order, "customer_email" : customer_email, "ship_to_phone" : ship_to_phone, "order_total" : order_total, "date" : date, "items_sku" : items_sku, "items_name" : items_name})
# 'orderTotal': 0.0, 'amountPaid': 0.0, 'taxAmount': 0.0, 'shippingAmount': 0.0, 