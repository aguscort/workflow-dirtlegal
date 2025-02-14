import re
from datetime import datetime, timedelta

#
# Define the Order Type
#
# Order type = Service if item name = Dirt Bike Conversion; ATV Conversion; UTV Conversion; Roxor Conversion; Military Conversion; Custom Street Legal Conversion; Golf Cart Conversion; Expedited Shipping Fee; Additional Fees For Registration/Parts/Shipping
# Order type = product if item name = ANYTHING ELSE
# Order type = combo if at least one item is a service and the other isn't a service as listed above.

serviceList = ['Dirt Bike Conversion','ATV Conversion' , 'UTV Conversion', 'Roxor Conversion', 'Military Conversion', 'Custom Street Legal Conversion', 'Golf Cart Conversion', 'Expedited Shipping Fee', 'Additional Fees For Registration/Parts/Shipping','Vehicle Registration Renewal']
service = False
product = False
item = ''
try:
    itemListRaw = input_data['item'].split (",")  # Convert the string to a list
except:
    itemListRaw = []
    
# Check if any Discouny is made
try:
    itemList =  re.sub(r'Discount', '', input_data['item']) # Extract the word Discount
    itemList =  re.sub(r',[ ]*$', '', itemList)             
    itemList =  re.sub(r',[ ]*,', ',', itemList).split (",") 
except:
    itemList = []

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


#
# Format the Order Number and the Payment Method
#
source = ''
if len(input_data['OrderRaw']) == 3:
    order = 'E' + input_data['OrderRaw']
elif len(input_data['OrderRaw']) == 4:
    order = input_data['OrderRaw']
else:
    order = input_data['OrderRaw']
    order = re.sub(r'-', '', order)

output = [{'order': order, "item" : item}]