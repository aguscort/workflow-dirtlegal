import re
from datetime import datetime

# PARAMETERS 
input_data = { 'OrderRaw':	'',
    'matchs' : 'Dirt Bike Conversion, ATV Conversion, UTV Conversion, Roxor Conversion, Military Conversion, Custom Street Legal Conversion, Golf Cart Conversion,Vehicle Registration Renewal, Custom Street Legal',
    'item' : '',
    'apikey_shipstation' : '',
    'password_shipstation' : '',
    'sku' : '',
    'token' :''}
# /PARAMETERS 

def get_product_by_sku(sku):
    items = []
    options =  []
    url = 'https://ssapi.shipstation.com/products?sku=' + str(sku)
    id = requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json()['products'][0]['productId']
    url = 'https://ssapi.shipstation.com/products/' + str(id)
    req = requests.get(url, auth=(input_data['apikey_shipstation'], input_data['password_shipstation'])).json()    
    try:            
        return req['productCategory']['name']
    except:
        return None

#
# Format the Order Number and the Payment Method
#
source = ''
if len(input_data['OrderRaw']) == 3:
    order = 'E' + input_data['OrderRaw']
    source = 'Ebay (Paypal)'
elif len(input_data['OrderRaw']) == 4:
    order = input_data['OrderRaw']
    source = 'Stripe'
else:
    order = input_data['OrderRaw']
    # Asked by Dash, remove formatting  03/26/2019
    #order = re.sub(r'-', '', order)
    source = 'Amazon'

#
# Define the Order Type
#
serviceList = ['Dirt Bike Conversion','ATV Conversion' , 'UTV Conversion', 'Roxor Conversion', 'Military Conversion', 'Custom Street Legal Conversion', 'Golf Cart Conversion', 'Expedited Shipping Fee', 'Additional Fees For Registration/Parts/Shipping','Vehicle Registration Renewal', 'Dirt Bike Street Legal Service','Custom Street Legal']
service = False
product = False
Exception = False
category = ''
item = ''
sku_order = ''
itemListRaw = input_data['item'].split (",")  # Convert the string to a list
# Check if any Discouny is made
itemList =  re.sub(r'Discount', '', input_data['item']) # Extract the word Discount
itemList =  re.sub(r',[ ]*$', '', itemList)             
itemList =  re.sub(r',[ ]*,', ',', itemList).split (",") 

for item in itemList: # Get all the items ordered by the customer
    exit_loop = False
    i_product = False
    i_service = False
    for elem in serviceList: # Perform a loop checking if it's a Service
        if item.strip().find(elem.strip()) != -1:   # If the item contains the Service 
            i_service = True        # we mark the item as Service
            i_product = False       # we mark the item as not a Product
            exit_loop = True        # we inform that we can leave the loop and go for the next item
        else:
            if exit_loop == False:  # only if we should leave the loop
                i_product = True    # in that case the item is identified as a product
        if item.strip().find('Additional Parts Fee') != -1: # Added the 20200528
            Exception = True
    if i_product == True:           # The item has been categorized, we update the proper variable
        product = True
    elif i_service == True:
        service = True

if service and product:             # If there is both kind of item
    item = 'Combo'
elif service and not product:       # If there is only item that they are services
    item = 'Service'
elif not service and product:       # If there is only item that they are products
    item = 'Product'
    
try:
    sku_order = input_data['sku']
except:
    sku_order = ''
if sku_order != '':
    category = get_product_by_sku(sku_order)

output = [{'order': order, 'item': item, 'source_mod' : source, 'category' : category, 'Exception' : Exception}]