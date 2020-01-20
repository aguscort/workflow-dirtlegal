import json
import requests
import re

# PARAMETERS 
input_data = { 'city':	'',
    'Apartment':	'',
    'name' : '',
    'webhook_apex' : '',
    'tr_param': '',
    'webhook':	'',
    'phone':	'',
    'state':	'',
    'street':	'',
    'itemList':	'',
    'td_quantity_param':	'',
    'postalcode':'',
    'quantity': '',
    'order': '',
    'td_name_param': '' }
# /PARAMETERS 

def GetStorage(access_token):
    url = 'https://store.zapier.com/api/records?secret=' + access_token
    return requests.get(url).json()

def SendMessage(sku, order):
    req = requests.get('https://hooks.zapier.com/hooks/catch/4834230/oyox8ih/',params={"sku": sku, "order": order},)

def sendMail(sku, itens, orderid, supplier, supplier_to, name, street, city, state, postalcode, phone, note, email):
    if supplier.find("Apex") == -1:
        req = requests.post(input_data['webhook'], data={"SKU": sku, "items": supplier,"supplier": supplier_to, "supplier_to": itens, "orderid": orderid, "name": name, "street": street, "city": city, "state": state, "postalcode": postalcode, "phone": phone, "note": note, "email": email},).json()
    else:
        req = requests.post(input_data['webhook_apex'], data={"SKU": sku, "items": supplier,"supplier": supplier_to, "supplier_to": itens, "orderid": orderid, "name": name, "street": street, "city": city, "state": state, "postalcode": postalcode, "phone": phone, "note": note, "email": email},).json()
    return req

def getItems(offset = None):
    req = ''
    if offset:
        req = requests.get('https://api.airtable.com/v0/appFufkqfl9yZNU5b/SKU%20List', headers={"Authorization":"Bearer keyYk3nnO04dbLGaT"}, params={"offset":offset}).json()
    else:
        req = requests.get('https://api.airtable.com/v0/appFufkqfl9yZNU5b/SKU%20List', headers={"Authorization":"Bearer keyYk3nnO04dbLGaT"},).json()
    try:
        if req['offset']:
            return req['records'], req['offset']
    except:
        return req['records'], None

def getPhone(supplier):
    try:
        if supplier.lower() == 'riva' or supplier.lower() == 'hardcabs':
            return "Phone: " + input_data['phone']
        else:
            return ''    
    except:
        return '' # Added in case there is no phone number


access_token = "J4SBnZ4wfhw3J3m8"
items = ''
sku = ''
cont = 0
offset = None
outcome = []
notes = {}
full_list = []
suppliers = []
quantity_items = {}
desc_def = {}
itemNote = ''
street = ''
try:
    itemsList = [str(i) for i in input_data['itemList'].split (",")]
except:
    itemsList = []
try:
    itemsQuantity = [str(i) for i in input_data['quantity'].split (",")]
except:
    itemsQuantity = []

# Get full list
records, offset = getItems(offset)
for i in records:
    full_list.append(i)
while offset:
    records, offset = getItems(offset)
    for i in records:
        full_list.append(i)

# Get the items quantity from order
for i in itemsList:
        try:
            quantity_items.update({i: itemsQuantity[cont]})
        except:
            quantity_items.update({i: ''})
        cont += 1

# Get the items data from order
for a in itemsList:
    for i in full_list:
        try:
            field = str(i['fields']['SKU']).lower().strip()
            if field == str(a).lower():
                outcome.append([str(i['fields']['SKU']).strip(),re.sub(r'\n', ' ', ''.join(i['fields']['Item Name/Part #/Variants'])), str(i['fields']['Supplier']), str(i['fields']['Supplier to:']), str(i['fields']['Supplier Email'])])
                try:
                    notes.update({str(i['fields']['SKU']).strip(): i['fields']['Internal Note']})
                except:
                    notes.update({str(i['fields']['SKU']).strip(): ''})
        except:
            continue 

# Concatename the desc from the same supplier
for i in outcome:
    suppliers.append(i[2])
    if int(quantity_items[i[0]]) > 1:
        color_text = '<font color ="red">'
    else:
        color_text = '<font color ="black">'
    if i[2] in desc_def:
        e = [str(list(desc_def[i[2]])[0]) + '<tr><td><font size="+2"><b>QTY:' + color_text + str(quantity_items[i[0]])  + '</b></font></td><td>' + i[1] + '</td></tr>', notes[i[0]] if len(str(list(desc_def[i[2]])[1])) == 0 else list(desc_def[i[2]])[1]]
    else:
        e = ['<tr><td><font size="+2"><b>QTY:' + color_text + str(quantity_items[i[0]])  + '</font></b></td><td>' + i[1] + '</font></td></tr>', notes[i[0]]]
    desc_def.update({i[2] : e})
    
# Get line 2 Address for ebay orders
try:
    street = input_data['street']
except:    
    street = ""
if len(input_data['order']) == 3:
    try:
        street = street + " " + input_data['Apartment']
    except:    
        pass
print(street)
#
# Format the Order Number and the Payment Method (QA)
#
order_new = ""
if len(input_data['order']) == 3:
    order_new = 'E' + input_data['order']
    #source = 'Ebay (Paypal)'
elif len(input_data['order']) == 4:
    order_new = input_data['order']
    #source = 'Stripe'
else:
    order_new = input_data['order']
    order_new = re.sub(r'-', '', order_new)

    
# Send the mails through a webhook
num_mails = 0
for i in outcome:       # get the suppliers list...
    if i[2] in desc_def:       # ... but avoid to send the mail twice to the same supplier
        sendMail(i[0], desc_def[i[2]][0], input_data['order'], i[3],  i[2], input_data['name'], street, input_data['city'], input_data['state'], input_data['postalcode'], getPhone(i[2]), desc_def[i[2]][1], i[4])
        output = [{"0" : i[0], "1" : desc_def[i[2]][0], "2" : i[2], "3" : i[3],  "4" : input_data['order'], "5" : input_data['name'], "6" : street, "7" : input_data['city'], "8" : input_data['state'], "9": input_data['postalcode'], "10" : getPhone(i[2]), "11" : desc_def[i[2]][1], "12" : i[4], "num_mails" : str(num_mails), "order_def" : order_new}]
        num_mails += 1
        desc_def.pop(i[2])
output = [{"num_mails" : str(num_mails), "order_def" : order_new}]