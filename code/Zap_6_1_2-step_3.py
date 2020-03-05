import json
import requests
import re, random
import urllib.parse
from datetime import datetime, timedelta

# PARAMETERS 
input_data = { 'item_name':	'',
    'wo':	'',
    'text':	'',
    'name':'',
    'sku': '',
    'apikey_shipstation': '',
    'password_shipstation': '' }
# /PARAMETERS 

orders_dict = {}
customer_dict = {}
attempts = int(input_data['attempts'])
skus_for_lien_holder = {'SQ4359210', 'SQ6193077', 'SQ3509691', 'SQ7202884', 'SQ9493879', 'SQ1624128', 'SQ9857937', 'SQ9579630', 'SQ6283166', 'SQ8910742', 'SQ9575974', 'SQ5997142'}
add_lien_holder_name = False

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

def continue_process(attempts, name, text, wo):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/omn6opx/'
    print("continue_process")
    data = {"attempts" : attempts, "name" : name,   "text" : text, "wo" : wo}
    return requests.post(url, data=json.dumps(data),)

def get_tasks():
    url = 'https://app.asana.com/api/1.0/workspaces/1122730176672819/tasks/search?completed=false'
    headers = { "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    return requests.get(url, headers=headers,).json()

def update_description(gid, text):
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid)  + "?opt_fields=html_notes"
    #headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/825342430bedc4e0cbcc701c8f59fd96"}
    req = requests.get(url, headers=headers,).json()    
    prev_desc = req["data"]["html_notes"].split("</body>")[0]
    if prev_desc.find("Renewal") == -1:
        #print(prev_desc)
        data = {"data" : {"html_notes": prev_desc + "\n<b>" + text  + "</b></body>"}}
        return requests.put(url, data=json.dumps(data), headers=headers,).json()   
    else:
        return False

def add_story(gid, text):
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid) + '/stories'
    #headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/b8024a8ee666abda2c08db438001492b"}
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer0/825342430bedc4e0cbcc701c8f59fd96"}
    data = {"data" : {"text": text, "is_pinned" : True}}
    return requests.post(url, data=json.dumps(data), headers=headers,).json()

def get_orders_period(created_at_min, created_at_max):
    url = 'https://ssapi.shipstation.com/orders?createDateStart=' + created_at_min + '&createDateEnd=' + created_at_max + '&pageSize=500'        
    return requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json()

def get_customers(page = 1):
    url = 'https://ssapi.shipstation.com/customers?page=' + str(page) + '&pageSize=500&SortBy=ModifyDate&sortDir=Asc'        
    customers, total, page, pages = requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json().values()
    return customers, total, page, pages

def get_all_orders_customer(customerName, numorders):
    url = 'https://ssapi.shipstation.com/orders?customerName=' + str(customerName).replace(" ","+")  + '&sortBy=OrderDate&sortDir=Desc&pageSize=' + str(numorders)
    return requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json()

def get_orders_customer(customerName, created_at_min, created_at_max, numorders):
    url = 'https://ssapi.shipstation.com/orders?customerName=' + str(customerName).replace(" ","+") + '&createDateStart=' + created_at_min + '&createDateEnd=' + created_at_max + '&pageSize=500'
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
    return list_folder

def exhaustive_customer_search():
    customers = []
    t_customers, total, page, pages = get_customers()
    customers.extend(t_customers)
    while page <= pages:         
        t_customers, total, page, pages = get_customers(page+1)
        customers.extend(t_customers)
    return customers
    
datetoday, date_lastweek, datetoday_lastmonth = date_treatment()
is_Order = False

#
# Get Data
#
order_sku = []
order_item_name = []
count = 0
text_list = str(input_data['text']).split("\r\n\r\n")
name = text_list[0].split(":")[1].strip()
address = text_list[1].split(":")[1].upper()
address = re.sub(r'[\w\.-]+@[\w\.-]+', '', address)    # Extract an email wrongly informed into this field
#print(str(text_list))
try:
    match = re.findall(r'[\w\.-]+@[\w\.-]+', input_data['text'])    
    email = match[0].strip()
except:
    email = ""
#print(str(email))    
phone = input_data['text'].split("Phone:")[1].split("Email:")[0]
phone = re.sub(r'[\D-]','',phone)
phone_short = phone[-4:]
taxes_paid  = text_list[18].split(":")[1].strip()
try:
    taxes_amount = str(text_list[19].split(":")[1].strip())
except:
    taxes_amount = ""
try:
    lien_holder_name = text_list[14].split(":")[1].strip()
except:
    lien_holder_name = ""
#
# Get for PDF
#
pfd_vehicle_owner = text_list[0].split(":")[1].strip().upper()
pfd_vehicle_owner = re.sub(r'\r\n', '', pfd_vehicle_owner) # Extract an newline character
pfd_vehicle_adress = address.split(",")[0].strip()
pfd_vehicle_adress = re.sub(r'[\w\.-]+@[\w\.-]+', '', pfd_vehicle_adress)    # Extract an email wrongly informed into this field
pfd_vehicle_adress2 = ", ".join(address.split(",")[1:]).strip()
pfd_vehicle_adress2 = " ".join(pfd_vehicle_adress2.split("\r\n")).strip()
pfd_vehicle_adress2 = re.sub(r'[\w\.-]+@[\w\.-]+', '', pfd_vehicle_adress2)    # Extract an email wrongly informed into this field
pdf_vin = str(text_list[8].split(":")[1]).upper()    
try:
    pdf_year =  text_list[4].split(":")[1]  
except:
    pdf_year =  ""
try:
    pdf_make =  text_list[5].split(":")[1]   
except:    
    pdf_make =  ""
try:
    pdf_model =  text_list[6].split(":")[1] 
except:    
    pdf_model = ""
#
# Format text
#
formatted_text = ""
# Name
formatted_text += text_list[0].split(":")[1].strip().upper() + "\r\n\r\n"
# Address
formatted_text += re.sub('[^a-zA-Z0-9 ]', '', address.split(",")[0]).strip() + "\r\n" +  re.sub('[^a-zA-Z0-9 ]', '', " ".join(address.split(",")[1:])).strip() + "\r\n\r\n" #+  re.sub('[^a-zA-Z0-9 ]', '', address.split(" ")[-1].strip())  + "\r\n\r\n"
count = 2
# Number
formatted_text += text_list[count].split(":")[1].strip() + "\r\n\r\n"
count += 1
# Mail
formatted_text += text_list[count].split(":")[1].strip() + "\r\n\r\n"
count += 1
# Vehicle Year, Make and Model
formatted_text += text_list[count].split(":")[1].strip() + " " + text_list[count+1].split(":")[1].strip() + " " + text_list[count+2].split(":")[1].strip() + "\r\n\r\n"
count += 3
# Before Vehicle Engine Size
while (text_list[count].find("Disclaimer") == -1) and (count+3 <= len(text_list)):
    if text_list[count].find("VIN") != -1:
        formatted_text += "VIN: " + str(text_list[count].split(":")[1]).strip().upper() + "\r\n\r\n"
    else:
        formatted_text +=  text_list[count].strip() + "\r\n\r\n"
    count += 1
formatted_text += str("\r\n\r\n").join(text_list[count+1:-1])
#print(formatted_text)
#
# Look for Order
#
target_order  = []
is_Order = False
order_id = ""
customers = exhaustive_customer_search()
for customer in customers:
    try:
        customer_dict.update({ re.sub(r'[\D-]','',customer['phone'])[-4:]: customer['name']})    
    except:
        pass
    
    try:
        if customer['email'].lower() == email.lower():
            name = customer['name']        
            print("Customer found")
            orders =  get_all_orders_customer(customer['name'], 1)
            print("Take all the orders from Shipstation")
            if orders['total'] > 0:
                for order in orders['orders']:
                    for item in order['items']:
                        if item['name'].find("Conversion") != -1 or item['name'].find("Custom Street Legal Service") != -1 :
                            is_Order = True
                            order_sku.append(item['sku'])
                            order_item_name.append(item['name'])             
                            order_id = order['orderId']
                            if item['sku'] in skus_for_lien_holder:
                                add_lien_holder_name = True                            
                    if is_Order:
                        target_order = order
                        # Create Comment in Asana Task
                        for task in get_tasks()["data"]:                            
                            if task["resource_type"] == "task" and str(task["name"]).find(str(target_order["orderNumber"])) != -1:
                                #Add Lien Holder Name
                                if add_lien_holder_name: 
                                    comment =  lien_holder_name + '\n<b>' 
                                else:
                                    comment =  ''
                                #Add taxes                                
                                if taxes_paid == "Yes":
                                    update_description(str(task['gid']), "TAX PAID: $" + str(taxes_amount))
                                else:
                                    update_description(str(task['gid']), "TAX OWED: $")
                                print(str(task['gid']))
                                add_story(str(task['gid']), formatted_text )
                                break                        
                        break
            print("Order found from customer's name: " + target_order['orderNumber'].strip())
            output = { "folder_name" : "Automated POA #" + get_order_number(target_order['orderNumber'].strip()), "text" : formatted_text, "pfd_vehicle_owner" : pfd_vehicle_owner, "pfd_vehicle_adress" : pfd_vehicle_adress, "pfd_vehicle_adress2" : pfd_vehicle_adress2, "pdf_vin" : pdf_vin, "pdf_year" : pdf_year, "pdf_make" : pdf_make, "pdf_model" : pdf_model, "wait" : str(random.randint(1, 5)), "wo" : get_order_number(target_order['orderNumber'].strip()), "order_sku" : order_sku, "order_item_name" : order_item_name,  "customer_name" : name, "order_id" : order_id}
    except:
        output = { "folder_name" : "None"}      

try:        
    if not is_Order and customer_dict[str(phone_short)] is not None:
        print("Look customer name from phone")
        orders =  get_all_orders_customer(customer_dict[str(phone_short)], 1) 
        print ("Get all orders from customer name")
        print("CUSTOMER: " + str(customer_dict[str(phone_short)]))
        print("TOTAL: " + str(orders['total']))        
        if orders['total'] > 0:
            for order in orders['orders']:
                for item in order['items']:
                    if item['name'].find("Conversion") != -1 or item['name'].find("Custom Street Legal Service") != -1:
                        is_Order = True
                        order_sku.append(item['sku'])
                        order_item_name.append(item['name'])
                        order_id = order['orderId']
                if is_Order:
                    target_order = order
                    # Create Comment in Asana Task
                    for task in get_tasks()["data"]:
                        if task["resource_type"] == "task" and task["name"].find(target_order["orderNumber"]) != -1:
                            if taxes_paid == "Yes":
                                update_description(str(task['gid']), "TAX PAID: $" + str(taxes_amount))
                            else:
                                update_description(str(task['gid']), "TAX OWED: $")
                            print(str(task['gid']))                                
                            add_story(task['gid'], formatted_text )
                            break    
                    break                  
            output = {"folder_name" : "Automated POA #" + get_order_number(target_order['orderNumber'].strip()), "text" : formatted_text, "pfd_vehicle_owner" : pfd_vehicle_owner, "pfd_vehicle_adress" : pfd_vehicle_adress, "pfd_vehicle_adress2" : pfd_vehicle_adress2, "pdf_vin" : pdf_vin, "pdf_year" : pdf_year, "pdf_make" : pdf_make, "pdf_model" : pdf_model, "wait" : str(random.randint(1, 5)), "wo" : target_order['orderNumber'].strip(), "order_sku" : order_sku, "order_item_name" : order_item_name, "customer_name" : name, "order_id" : order_id}    
except:
    pass

if is_Order:
    if output["folder_name"] != "None": 
        folder_exists = False
        try:
            for i in exhaustive_search(input_data['root']):
                if i['.tag'] ==  'folder' and i['name'] == output["folder_name"]:
                    folder_exists = True
                    break
            if  not folder_exists:
                #create_folder(input_data["root"].strip() + "/" + output["folder_name"].strip())
                pass
        except:
            pass
else:
    if attempts < 10:   
        attempts += 1
        print(str(attempts))       
        continue_process(attempts, name, input_data['text'], None)
    output = { "folder_name" : None , "text" : formatted_text, "pfd_vehicle_owner" : pfd_vehicle_owner, "pfd_vehicle_adress" : pfd_vehicle_adress, "pfd_vehicle_adress2" : pfd_vehicle_adress2, "pdf_vin" : pdf_vin, "pdf_year" : pdf_year, "pdf_make" : pdf_make, "pdf_model" : pdf_model, "wait" : str(random.randint(1, 5)), "wo" : None,  "order_sku" : order_sku, "order_item_name" : order_item_name, "customer_name" : name, "order_id" : None}  