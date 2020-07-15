import re

# PARAMETERS 
input_data = { 'title':	''}
# /PARAMETERS 

WO = input_data['title'].split("#")[-1]
name = input_data['title'].split("#")[0]

output = [{'name': name, 'WO': WO}]