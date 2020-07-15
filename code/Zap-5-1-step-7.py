import re

# PARAMETERS 
input_data = { 'notes':	'',
    'title':	''}
# /PARAMETERS 

WO = input_data['title'].split("#")[-1]
name = input_data['title'].split(" ")[0]
email = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", input_data['notes'])

try:
    output = [{'name': name, 'WO': WO, 'email' : email[0]}]
except:
    output = [{'name': name, 'WO': WO, 'email' : ""}]