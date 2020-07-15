import json
import requests

# PARAMETERS 
input_data = { 'key':	'',
    'gid' : '',
    'customer' : '{"email" : "", \
             "phone" : "", \
             "name" : "", \
             "street" : "", \
             "street2" : "", \
             "city" : "", \
             "state" : "", \
             "zipcode" : "", \
             "item_quantity" : "", \
             "item_name" : "", \
             "item_sku" : "", \
             "variants" : "", \
             "category" : ""}', 
    'address_validation' : '',
    'email' : '',
    'phone' : '',
    'name' : '',
    'street' : '',
    'street2' : '',
    'city' : '',
    'state' : '',
    'zipcode' : '',
    'item_quantity' : '',
    'item_name' : '',
    'item_sku' : '',
    'variants' : '',
    'category' : ''}
# /PARAMETERS 

def write_description(gid, html_text):
    """ Overwrites existing task (gid) description with html_text """
    
    url = f"https://app.asana.com/api/1.0/tasks/{str(gid)}?opt_fields=html_notes"
    headers = {'Content-Type': 'application/json', 'Authorization': input_data['key']}    
    data = {'data': {'html_notes': f"<body>{html_text}</body>"}}
    return requests.put(url, data = json.dumps(data), headers = headers,).json()

def append_description(gid, text):
    """ Adds text to the bottom of the existing task (gid) description.
        NOTE: Has potential to fail if conditions at the bottom aren't met.
        NOTE: Text will be rendered bolded (<b>text</b>) ?"""
    
    url = f"https://app.asana.com/api/1.0/tasks/{str(gid)}?opt_fields=html_notes"
    headers = {'Content-Type' :'application/json', 
               'Authorization': input_data['key']}
    req = requests.get(url, headers=headers,).json()  
    
    try:
        prev_desc = req['data']['html_notes'].split('</body>')[0]
    except:
        prev_desc = ''
        
    if prev_desc.find('Renewal') == -1 and len(prev_desc) > 0 :  # not sure why .find
        data = {'data': {'html_notes': prev_desc + '\n<b>' + text  + '</b></body>'}}
        return requests.put(url, data=json.dumps(data), headers=headers,).json()   
    else:
        return False
    
def are_duplicate(str1, str2):
    """Check if two strings are the same OR very similiar.
       Sometimes address 1 and address 2 duplicate in ShipStation OR they are very similiar 
       (e.g. 'x st' & 'x street')"""

    def street_and_st(str1, str2):
        # Filter variations of street and check if strings are the same
        str1 = str1.replace(' street', ' ').replace(' st', ' ').strip()
        str2 = str2.replace(' street', ' ').replace(' st', ' ').strip()
        if str1 == str2:
            return True
        return False

    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    
    if str1 == str2:
        return True
    
    elif street_and_st(str1, str2):
        return True
    
    return False

# customer = json.loads(r"{}".format(input_data['customer']))
# customer = json.loads(input_data['customer'].replace('\n', '').replace('\r', ''))
customer = {"email": input_data.get('email'),
            "phone": input_data.get('phone'),
            "name": input_data.get('name'),
            "street": input_data.get('street'),
            "street2": input_data.get('street2'),
            "city": input_data.get('city'),
            "state": input_data.get('state'),
            "zipcode": input_data.get('zipcode'),
            "item_quantity": input_data.get('item_quantity'),
            "item_name": input_data.get('item_name'),
            "item_sku": input_data.get('item_sku'),
            "variants": input_data.get('variants'),
            "category": input_data.get('category')}
text = ''

# Bold QTY integer if > 1
if int(customer['item_quantity']) > 1:
    customer['item_quantity'] = f"<strong>{customer['item_quantity']}</strong>"
    
# TODO: Possibly have to handle empty variants and \n

# Customer Email and Phone
text += f"{customer['email']}\n{customer['phone']}\n\r\n"  # \r\n to leave blank line

# Customer Name
text += f"{customer['name']}\n"

# Customer Address Validation Status on ShipStation
if input_data['address_validation'] == 'Address validation warning':  # ShipStation !verify address
    text += "<strong>Invalid address\n</strong>"
    
# Customer Address 1 / Address 2
try: 
    if not are_duplicate(customer['street'], customer['street2']):
        text += f"{customer['street']} {customer['street2']}\n"
    else:
        text += f"{customer['street']}\n"
except Exception as e:  # AttributeError if None values passed into are_duplicate() 
    text += f"{customer['street']}\n"

# Customer City, State, ZIP
text += f"{customer['city']} {customer['state']} {customer['zipcode']}\n\r\n"

# Footer (Line Item Info / Variants / Supplier)
text += f"QTY: {customer['item_quantity']}\n{customer['item_name']} - {customer['item_sku']}\n"
text += f"Variants:\n{customer['variants']}\n\r\n"
text += f"Supplier: {customer['category']}\n"

# Tests
# output_data['customer'] = customer
# output['text'] = text

write_description(input_data['gid'], text)