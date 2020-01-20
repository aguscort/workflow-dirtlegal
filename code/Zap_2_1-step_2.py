import re

# PARAMETERS 
input_data = { 'itemsIncluded':	'SQ2712047,SQ5199410,SQ1055471,SQ9782880,SQ5166965,SQ9493879,SQ1624128,SQ9857937,SQ9579630,SQ8811460,SQ8403421,SQ1235346,SQ2649829,SQ0550038,SQ0910340,SQ0559800,SQ3553182,SQ0804171,SQ5736877,SQ0355699,SQ6283166,SQ8910742,SQ4922562,SQ4808996,SQ8069412,SQ5023998,SQ4359210,SQ6193077,SQ3509691,SQ7202884,SQ8874800,SQ4051474,SQ3647371,SQ5357769,SQ5997142,SQ0495127,SQ7846988,SQ5548002,SQ2127240,SQ3325725,SQ4635264,SQ9575974,SQ8335047,SQ7852377,SQ5191636,SQ1802005,SQ3578648,SQ5950920,SQ3301680,SQ0353501,SQ3403651,SQ3335709,SQ5260210,SQ2949442,SQ3423037,SQ0512676,SQ6417532,SQ6690036,SQ6298858,SQ8602839,SQ8578135,SQ0602630,SQ2062942,SQ6573152,SQ2175303,SQ1484391,SQ3699856,SQ8017200,SQ7666170,SQ8539067,SQ6418788,SQ9278038,SQ6700618,SQ4865322,SQ6335784,SQ1059138',
    'OrderRaw':	'',
    'itemName' : '',
    'shipToName' : '',
    'itemSku': ''}
# /PARAMETERS 

def call_next_step(order, ship_to_name):
    req = requests.get('https://hooks.zapier.com/hooks/catch/4834230/oomxlqv/',params={"order": order, "ship_to_name": ship_to_name},)


#The folder is automatically created ONLY when the item name is any of the following
# "Vehicle Registration Renewal; Dirt Bike Conversion; ATV Conversion; UTV Conversion; Roxor Conversion; 
# Military Conversion; Custom Street Legal Conversion; Golf Cart Conversion"
itemsForFoldersList = input_data['itemsIncluded'].split (",")
process = False
createFolder = False
item = ''
itemList = input_data['itemSku'].split (",")
for item in itemList:
    if item in itemsForFoldersList:
        createFolder = True
process = False
if len(input_data['OrderRaw']) == 3:
    order = 'E' + input['OrderRaw']
elif len(input_data['OrderRaw']) == 4:
    order = input['OrderRaw']
    process = True
else:
    order = input_data['OrderRaw']
    order = re.sub(r'-', '', order)

if createFolder and process:
    call_next_step(order, input_data['shipToName'])

output = [{'createFolder': createFolder, 'order': order, 'process' : process}]