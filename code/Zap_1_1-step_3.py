import re
from datetime import datetime

# PARAMETERS 
input_data = { 'order_id':	'',
    'item':	'',
    'ItemQuantity' : '',
    'matchs' : 'Dirt Bike Conversion, ATV Conversion, UTV Conversion, Roxor Conversion, Military Conversion, Custom Street Legal Conversion, Golf Cart Conversion,Vehicle Registration Renewal',
    'paymentMethod': '',
    'ship_to_name':	'',
    'order_total':	'',
    'orderDate':	'',
    'itemSKU':	'',
    'customer_email':	'',
    'OrderRaw':	'',
    'items':'',
    'createDate': '',
    'fulfillmentSku': '',
    'imageUrl': '',
    'lineItemKey': '',
    'modifyDate': '',
    'name': '',
    'options': '',
    'orderItemId': '',
    'productId':'',
    'quantity': '',
    'shippingAmount': '',
    'sku': '',
    'taxAmount': '',
    'unitPrice': '',
    'upc': '',
    'warehouseLocation': '',
    'weight': '',
    'access_token':	'',
    'ship_to_phone': '',
    'asana_webhook': '' }
# /PARAMETERS 


def CreateAsana(ship_to_name, order, customer_email, ship_to_phone, order_total, item_name, date, pdfs_to_apply, title_request):
    req = requests.get('https://hooks.zapier.com/hooks/catch/4834230/otl7ydt/',params={"ship_to_name" : ship_to_name, "order" : order, "customer_email" : customer_email, "ship_to_phone" : ship_to_phone, "order_total" : order_total, "item_name" : item_name, "date" : date, "pdfs_to_apply" : pdfs_to_apply, "title_request" : title_request})
    
def Create_asana_renewal(ship_to_name, order, customer_email, ship_to_phone, order_total, item_name, date, asana_renewal_status, pdfs_to_apply, title_request):
    req = requests.get('https://hooks.zapier.com/hooks/catch/4834230/ouqdrzi/',params={"ship_to_name" : ship_to_name, "order" : order, "customer_email" : customer_email, "ship_to_phone" : ship_to_phone, "order_total" : order_total, "item_name" : item_name, "date" : date, "asana_renewal_status" : asana_renewal_status, "pdfs_to_apply" : pdfs_to_apply, "title_request" : title_request})

    
def create_asana_task_for_product(ship_to_name, order, customer_email, ship_to_phone, order_total, date, items, order_id, order_id_raw):
    req = requests.get('https://hooks.zapier.com/hooks/catch/4834230/otskw5d/',params={"ship_to_name" : ship_to_name, "order" : order, "customer_email" : customer_email, "ship_to_phone" : ship_to_phone, "order_total" : order_total, "date" : date, "items" : items, "order_id" : order_id, "order_id_raw" : order_id_raw })    
    
def date_treatment(datetimeStr):
    # Date treatment, change formatting and set timezone
    dateTimeObj = datetime.strptime(datetimeStr[:-1], '%Y-%m-%dT%H:%M:%S.%f') #+ timedelta(hours=3)
    #return dateTimeObj.strftime('%m/%d/%Y %H:%M:%S'), dateTimeObj.strftime('%m/%d')
    return dateTimeObj.strftime('%m/%d/%Y %H:%M:%S'), "{:01d}/{:02d}".format(dateTimeObj.month,dateTimeObj.day)

def save_order_data(access_token):
    a = StoreClient(access_token)
    try:
        order_total_St = input_data['order_total']
    except:
        order_total_St = 0
    a.set_child_values(order, {'name': input_data['ship_to_name'], 'date': date_long, 'order_type': item, 'rate': order_total_St, 'quantity': total, 'payment_method': source, 'date_time': input_data['orderDate']})

#
# Format the Order Number and the Payment Method
#
source = ''
if len(input_data['OrderRaw']) == 3:
    order = 'E' + input_data['OrderRaw']
    source = 'Ebay (Paypal)'
elif len(input_data['OrderRaw']) == 4:
    order = input_data['OrderRaw']
    #source = 'Stripe'
else:
    order = input_data['OrderRaw']
    order = re.sub(r'-', '', order)
    source = 'Amazon'

try:
    if len(source) == 0:
        source = input_data['paymentMethod']
except:
    pass

# Re-code "Fix Payment Method"
if source == 'Credit Card':
        source = 'Stripe'

date_long, date_short = date_treatment(input_data['orderDate'])        
        
#
# Define the Order Type
#
# Order type = Service if item name = Dirt Bike Conversion; ATV Conversion; UTV Conversion; Roxor Conversion; Military Conversion; Custom Street Legal Conversion; Golf Cart Conversion; Expedited Shipping Fee; Additional Fees For Registration/Parts/Shipping
# Order type = product if item name = ANYTHING ELSE
# Order type = combo if at least one item is a service and the other isn't a service as listed above.

serviceList = ['Dirt Bike Conversion','ATV Conversion' , 'UTV Conversion', 'Roxor Conversion', 'Military Conversion', 'Custom Street Legal Conversion', 'Golf Cart Conversion', 'Expedited Shipping Fee', 'Additional Fees For Registration/Parts/Shipping','Vehicle Registration Renewal', 'Dirt Bike Street Legal Service']
service = False
product = False
item = ''
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
# Elegible for Title Request PDF Autofill
#        
s1_title_request_pdf_asana = ["SQ5997142","SQ9575974","SQ4359210","SQ6193077","SQ3509691","SQ7202884","SQ9493879","SQ1624128","SQ9857937","SQ9579630","SQ6283166","SQ8910742"]    
title_request = False

for i in range(len(s1_title_request_pdf_asana)):
    if s1_title_request_pdf_asana[i] in input_data['itemSKU']:
            title_request = True
            break

#
# Choosing the PDFS
#    
s1_instruction_pdf_asana = [['(1) SD LIEN INSTRUCTIONS.pdf' , ['SQ5997142', 'SQ9575974', 'SQ4359210', 'SQ6193077', 'SQ3509691', 'SQ7202884', 'SQ9493879', 'SQ1624128', 'SQ9857937', 'SQ9579630', 'SQ6283166', 'SQ8910742','Custom']], \
['(1) SD MCO INSTRUCTIONS.pdf' , ['SQ6671046','SQ4635264','SQ5166965','SQ2649829','SQ4922562','SQ4808996','SQ8069412','SQ5023998','Custom']], \
['(1) SD TITLE INSTRUCTIONS.pdf' , ['SQ5357769', 'SQ3325725', 'SQ4922562', 'SQ4808996', 'SQ8069412', 'SQ5023998', 'SQ2712047', 'SQ5199410', 'SQ1055471', 'SQ9782880', 'SQ0804171', 'SQ5736877','Custom']], \
['(1) UT ONLY INSTRUCTIONS.pdf' , ['SQ5548002','Custom']], \
['(1) UT VT TO UT INSTRUCTIONS.pdf' , ['SQ2127240','Custom']], \
['(1) VT INSTRUCTIONS.pdf', ['SQ8811460', 'SQ8403421','SQ1235346', 'SQ0550038', 'SQ0910340', 'SQ0559800', 'SQ3553182', 'SQ0355699','SQ9197192', 'SQ0495127', 'SQ0038404','Custom']]]
s1_checklist_pdf_asana = [['(1) CL SD Lien Tax.pdf', ['SQ5997142', 'SQ9575974', 'SQ4359210', 'SQ6193077',  'SQ3509691', 'SQ7202884','SQ9493879', 'SQ1624128','SQ9857937', 'SQ9579630', 'SQ6283166', 'SQ8910742','Custom']], \
['(1) CL SD Lien.pdf', ['SQ5997142', 'SQ9575974', 'SQ4359210', 'SQ6193077',  'SQ3509691', 'SQ7202884','SQ9493879', 'SQ1624128','SQ9857937', 'SQ9579630', 'SQ6283166', 'SQ8910742','Custom']], \
['(1) CL SD MCO or Title in Name Tax.pdf', ['SQ6671046', 'SQ4635264', 'SQ5166965', 'SQ2649829', 'SQ4922562', 'SQ4808996', 'SQ8069412', 'SQ5023998', 'SQ5357769', 'SQ3325725', 'SQ4922562', 'SQ4808996', 'SQ8069412', 'SQ5023998','SQ2712047', 'SQ5199410', 'SQ1055471', 'SQ9782880', 'SQ0804171', 'SQ5736877','Custom']], \
['(1) CL SD MCO.pdf', ['SQ6671046', 'SQ4635264', 'SQ5166965', 'SQ2649829', 'SQ4922562', 'SQ4808996', 'SQ8069412', 'SQ5023998', 'SQ5357769', 'SQ3325725', 'SQ4922562', 'SQ4808996', 'SQ8069412', 'SQ5023998','SQ2712047', 'SQ5199410', 'SQ1055471', 'SQ9782880', 'SQ0804171', 'SQ5736877','Custom']], \
['(1) CL SD Title in Name.pdf', ['SQ5357769', 'SQ3325725', 'SQ4922562', 'SQ4808996', 'SQ8069412', 'SQ5023998', 'SQ2712047', 'SQ5199410', 'SQ1055471', 'SQ9782880', 'SQ0804171', 'SQ5736877','Custom']], \
['(1) CL SD Title Signed Over Tax.pdf', ['SQ5357769', 'SQ3325725', 'SQ4922562', 'SQ4808996', 'SQ8069412', 'SQ5023998', 'SQ2712047', 'SQ5199410', 'SQ1055471', 'SQ9782880', 'SQ0804171', 'SQ5736877','Custom']], \
['(1) CL UT Only Tax.pdf', ['SQ5548002','Custom']], \
['(1) CL UT Only.pdf', ['SQ5548002','Custom']] , \
['(1) CL VT BOS VIN Inspection.pdf', ['SQ8811460', 'SQ8403421', 'SQ1235346', 'SQ0550038', 'SQ0910340', 'SQ0559800', 'SQ3553182', 'SQ0355699','SQ9197192', 'SQ0038404','Custom']],  \
['(1) CL VT BOS.pdf', ['SQ8811460', 'SQ8403421', 'SQ1235346', 'SQ0550038', 'SQ0910340', 'SQ0559800', 'SQ3553182', 'SQ0355699','Custom']],  \
['(1) CL VT MCO Tax.pdf', ['SQ8811460', 'SQ8403421', 'SQ1235346', 'SQ0550038', 'SQ0910340', 'SQ0559800', 'SQ3553182', 'SQ0355699','Custom']], \
['(1) CL VT TO UT BOS BIZ TAX.pdf', ['SQ2127240','Custom']], \
['(1) CL VT MCO.pdf', ['SQ0550038', 'SQ0910340', 'SQ0559800', 'SQ3553182','Custom']], \
['(1) CL VT TO UT BOS BIZ.pdf', ['SQ2127240','Custom']], \
['(1) CL VT TITLE SF97.pdf', ['SQ0495127','Custom']], \
['(1) CL VT TITLE SF97 TAX.pdf', ['SQ0495127','Custom']], \
['(1) CL VT TO SD BOS.pdf', ['SQ8874800', 'SQ4051474', 'SQ3647371','Custom']], \
['(1) CL VT TO SD BOS TAX.pdf', ['SQ8874800', 'SQ4051474', 'SQ3647371','Custom']], \
['(1) VT TO SD INSTRUCTIONS.pdf', ['SQ8874800', 'SQ4051474', 'SQ3647371']], \
['(1) CL VT TO UT BOS.pdf', ['SQ2127240','Custom']]]   
pdfs_to_apply = []

for i in range(len(s1_instruction_pdf_asana)):
    for sku in range(len(s1_instruction_pdf_asana[i][1])):
        if s1_instruction_pdf_asana[i][1][sku] in input_data['itemSKU']:
            pdfs_to_apply.append(s1_instruction_pdf_asana[i][0])      
            
for i in range(len(s1_checklist_pdf_asana)):
    for sku in range(len(s1_checklist_pdf_asana[i][1])):
        if s1_checklist_pdf_asana[i][1][sku] in input_data['itemSKU']:
            pdfs_to_apply.append(s1_checklist_pdf_asana[i][0])                           

#if input_data['item'].find("Custom Street Legal Conversion") != -1:
#    for i in range(len(s1_instruction_pdf_asana)):
#        if 'Custom' in s1_instruction_pdf_asana[i][1]:
#            pdfs_to_apply.append(s1_instruction_pdf_asana[i][0])      
#
#    for i in range(len(s1_checklist_pdf_asana)):
#        if 'Custom' in s1_checklist_pdf_asana[i][1]:
#            pdfs_to_apply.append(s1_checklist_pdf_asana[i][0])                     
                        
print(str(pdfs_to_apply))     
#
# Setting up Conditions to create the Asana Task
#
skus_for_renewal = ["SQ6436158", "SQ4150338", "SQ3515830", "SQ2022544", "SQ4433756", "SQ5546410", "SQ2152089", "SQ5483646", "SQ2281782", "SQ1664377", "SQ5155354", "SQ2636526", "SQ5547942", "SQ2373355", "SQ1603291"]
skus_for_draft = ["SQ6436158", "SQ4150338", "SQ3515830", "SQ2022544", "SQ4433756"]
skus_for_draft_dupe_tag = ["SQ2022544"]
asana_renewal = False
asana_renewal_status = ""
itemsForAsanaTaskList = input_data['matchs'].split (",")
item_SKU  = input_data['itemSKU'].split (",")
create_task = False
item2 = ''
items_name = []
i_match = False

for item2 in itemList: 
    exit_loop = False
    for elem in itemsForAsanaTaskList: # Perform a loop checking if it belong to the list
        if item2.strip().find(elem.strip()) != -1: 
            i_match = True
            exit_loop = True
            items_name.append(item2)
    if i_match == True:
        create_task = True       
        for i in item_SKU:
            if i in skus_for_renewal:
                asana_renewal = True
                if i in skus_for_draft:
                    asana_renewal_status = "1143826211847520"
                    break
                elif i in skus_for_draft_dupe_tag:
                    asana_renewal_status = "1146228767964637"
                    break

try:
    if create_task and not asana_renewal:
        CreateAsana(input_data['ship_to_name'] , order, input_data['customer_email'], input_data['ship_to_phone'], input_data['order_total'], ','.join(items_name), date_long, pdfs_to_apply, title_request)

    if create_task and asana_renewal:
        Create_asana_renewal(input_data['ship_to_name'] , order, input_data['customer_email'], input_data['ship_to_phone'], input_data['order_total'], ','.join(items_name), date_long, asana_renewal_status, pdfs_to_apply, title_request)     
except:
    print("Some issue arose")
    
#
# This will apply for ANY order that has an actual product, including combo orders.
#
getFirstOrder = re.search(r"^\d\d\d\d-(\d)$", input_data['OrderRaw'])
try:
    if item != 'Service' and str(getFirstOrder).find("match") == -1:
        # Send info to Asana
        create_asana_task_for_product(input_data['ship_to_name'] , order, input_data['customer_email'], input_data['ship_to_phone'], input_data['order_total'], date_long, input_data['items'], input_data['order_id'], input_data['OrderRaw'] )    
except:
    print("Some issue arose")
    
#
# Get the Quantities
#
try:            # if ItemQuantity exists
    total = 0
    index = 0
    quantity = input_data['ItemQuantity'].split (",") 
    for i in quantity:      
        if itemListRaw[index]  != "Discount": # We check that the item is not a Discount
            total = total + int(i)
        index += 1
except:         # in case the field doesn't exist
    total = len(input_data['itemSKU'].split (",")) # We don't know the quantity, we do a guess 


#
# Setting up Conditions to control the flow
#
# We need a filter for all manual orders created in shipstation. 
# Everytime i have an order with multiple items i need to split it and the new order number 
# becomes "XXXX-1" These cannot show up on the google sheet, so the easiest way to fix this 
# would be to have NO manual created orders added into the google sheet
continueZap = re.search(r"^\d\d\d\d-(\d)$", input_data['OrderRaw'])
try:
    if str(continueZap).find("match") == -1 and float(input_data['order_total']) > 0.0:
        save_order_data(input_data['access_token'])
except:
    pass

output = [{'order': order, 'source': source, 'quantity': total, 'item': item, 'continueZap' : str(continueZap), 'data' : date_long, "create_task" : create_task }]