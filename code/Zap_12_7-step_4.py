# PARAMETERS 
input_data = { 'variants_key':	'',
    'variants_name' : '',
    'name_key' : '',
    'task_name' :''}
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
    
# Get Asana Task Name for Lookup
raw_data = input_data['task_name'].split(';')
task_name = f"#{raw_data[0]} - {raw_data[1]} - {raw_data[2]}"
    
output = [{'variants': variants, 'name_key': input_data['name_key'][0:31], 'task_name': task_name}]