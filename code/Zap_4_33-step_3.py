# PARAMETERS 
input_data = { 'order1': '',
    'order2' : ''}
# /PARAMETERS 

order = ""
if len(input_data['order1']) > 4:
    order = input_data['order2']
else:
    order =  input_data['order1']
output = [{'order': order}]