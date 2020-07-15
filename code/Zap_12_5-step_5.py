import json
import requests

# PARAMETERS 
input_data = { 'variants_key':	'',
    'variants_name' : '',
    'name_key' : '',
    'second_address' : ''}
# /PARAMETERS 

try:
    keys  =  input_data['variants_key'].split(",")
except: 
    keys = ""
try:    
    name =  input_data['variants_name'].split(",")
except:    
    name =  ""
variants = ""
count = 0
for i in keys:
    variants += "- " + str(name[count]) + ": " + str(i) + "\r\n"
    count += 1

    
# Formatting second address for later
if input_data.get('second_address'):
    second_address = f"\n{input_data.get('second_address')}"    # push second address to next line
else:
    second_address = ''
    
output = [{'variants': variants , 
           'name_key': input_data['name_key'][0:31],
           'second_address': second_address}]