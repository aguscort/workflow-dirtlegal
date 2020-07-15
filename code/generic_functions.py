import requests
import re


# PARAMETERS 
input_data = { 'type':	'',
    'id' : '',
    'asana_token':	'0/b8024a8ee666abda2c08db438001492b',
    'airtable_token' : 'keyhERs1AvoB1EZT0'}
# /PARAMETERS 



def get_items(offset = None):
    req = ''
    if offset:
        req = requests.get('https://api.airtable.com/v0/appFufkqfl9yZNU5b/SKU%20List', headers={"Authorization":"Bearer " + input_data['airtbale_token']}, params={"offset":offset}).json()
    else:
        req = requests.get('https://api.airtable.com/v0/appFufkqfl9yZNU5b/SKU%20List', headers={"Authorization":"Bearer "+ input_data['airtbale_token']},).json()
    try:
        if req['offset']:
            return req['records'], req['offset']
    except:
        return req['records'], None


def get_full_list():
    offset = None
    full_list = []
    # Get full list of items 
    records, offset = get_items(offset)
    for i in records:
        full_list.append(i)
    while offset:
        records, offset = get_items(offset)
        for i in records:
            full_list.append(i)        
    return full_list



def format_order(order):
#
# Format the Order Number and the Payment Method (QA)
#
    order_new = ""
    source = ""
    if len(order) == 3:
        order_new = 'E' + order
        source = 'Ebay (Paypal)'
    elif len(order) == 4:
        order_new = order
        source = 'Stripe'
    else:
        order_new = order
        order_new = re.sub(r'-', '', order_new)
        source = 'Amazon'
    return order_new, source

def order_type(services, items): 
    #
    # Define the Order Type
    #
    # Order type = Service if item name = Dirt Bike Conversion; ATV Conversion; UTV Conversion; Roxor Conversion; Military Conversion; Custom Street Legal Conversion; Golf Cart Conversion; Expedited Shipping Fee; Additional Fees For Registration/Parts/Shipping
    # Order type = product if item name = ANYTHING ELSE
    # Order type = combo if at least one item is a service and the other isn't a service as listed above.
    service = False
    product = False
    item_type = ''
    item_list = []
    itemListRaw = items.split (",")  # Convert the string to a list
    # Check if any Discouny is made
    item_list =  re.sub(r'Discount', '', items) # Extract the word Discount
    item_list =  re.sub(r',[ ]*$', '', item_list)             
    item_list =  re.sub(r',[ ]*,', ',', item_list).split (",") 

    for item in item_list: # Get all the items ordered by the customer
        exit_loop = False
        i_product = False
        i_service = False
        for elem in services: # Perform a loop checking if it's a Service
            if item.strip().find(elem.strip()) != -1:   # If the item contains the Service 
                i_service = True        # we mark the item as Service
                i_product = False       # we mark the item as not a Product
                exit_loop = True        # we inform that we can leave the loop and go for the next item
            else:
                if exit_loop == False:  # only if we should leave the loop
                    i_product = True    # in that case the item is identified as a product
        if i_product == True:           # The item has been categorized, we update the proper variable
            product = True
        elif i_service == True:
            service = True

    if service and product:             # If there is both kind of item
        item_type = 'Combo'
    elif service and not product:       # If there is only item that they are services
        item_type = 'Service'
    elif not service and product:       # If there is only item that they are products
        item_type = 'Product'

    return item_list, item_type

def change_order_Type(gid, item_name, asana_token):
    type_id = ""
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid) 
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer" + str(asana_token)}
    req = requests.get(url, headers=headers,).json()   
    for i in range(len(req["data"]["custom_fields"][1]["enum_options"])):
        if item_name.find(req["data"]["custom_fields"][1]["enum_options"][i]["name"]) != -1 and (len(type_id) < len(req["data"]["custom_fields"][1]["enum_options"][i]["name"])):
                type_id = req["data"]["custom_fields"][1]["enum_options"][i]["gid"]  
    # For SKUs SQ3325725,SQ4635264,SQ9575974
    if item_name.find("Roxor Street Legal Service") != -1: 
        type_id = "1130761583281370"                
    if type_id != "":
        data = {"data" : {"custom_fields": { "1130761583281368": type_id}}}
        return requests.put(url, data=json.dumps(data), headers=headers,).json()  

def update_description(gid):
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid)  + "?opt_fields=html_notes"
    headers = {"Content-Type" :"application/json", "Authorization": "Bearer" + str(asana_token)}
    req = requests.get(url, headers=headers,).json()    
    data = {"data" : {"html_notes": req["data"]["html_notes"].replace("mailto:","").replace("&lt;/code&gt;","").replace("&lt;code&gt;","")}}
    return requests.put(url, data=json.dumps(data), headers=headers,).json()       


    