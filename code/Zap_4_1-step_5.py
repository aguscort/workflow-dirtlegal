import json
import requests
import urllib.parse

# PARAMETERS 
input_data = { 'gid':	'',
    'project_gid':	''}
# /PARAMETERS 

def launch_asana_attach(project_gid, gid, file_name):
    req = requests.get('https://hooks.zapier.com/hooks/catch/4834230/ouq3xft/',params={"filename" : file_name, "project_gid" : project_gid, "gid" : gid,})

try:    
    files = str(input_data['filename']).split(",")
    for f in files:
        launch_asana_attach(input_data['project_gid'], input_data['gid'], urllib.parse.quote(str(f)))
except:
    pass
    
output = [{'project_gid': input_data["project_gid"], 'gid': input_data["gid"], 'go_agead' : 'True'}]