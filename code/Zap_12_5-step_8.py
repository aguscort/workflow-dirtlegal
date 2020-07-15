import json
import requests

# PARAMETERS 
input_data = { 'shipping_data':	'',
    'gid' : '',
    'second_address' : ''
    'token' : ''}
# /PARAMETERS 

def list_to_text(data):
    text = ""
    for d in data:
        text += f"{d}\n"
    return text


def add_story(gid, text):
    url = 'https://app.asana.com/api/1.0/tasks/' +  str(gid) + '/stories'
    headers = {"Content-Type": "application/json", 
               "Authorization": input_data['token']}
    data = {"data" : {"text": text, "is_pinned" : False}}
    return requests.post(url, data=json.dumps(data), headers=headers,).json()


def are_duplicate(str1, str2):
    """Check if two strings are the same OR very similiar.
       Sometimes address 1 and address 2 duplicate in ShipStation OR they are very similiar 
       (e.g. 'x st' & 'x street')"""

    def street_and_st(str1, str2):
        # Filter variations of street and check if strings are the same
        str1 = str1.replace(' street', ' ').replace(' st', ' ').strip()
        str2 = str2.replace(' street', ' ').replace(' st', ' ').strip()
        if str1 == str2:
            return True
        return False

    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    
    if str1 == str2:
        return True
    
    elif street_and_st(str1, str2):
        return True
    
    return False


def get_comment(shipping_data):
    """Builds comment in the correct format for Copy and Paste Shipping info AutoHotKey
       script."""
    comment = "" 
    
    # add first name, last name, street address 
    comment += list_to_text(shipping_data[:3])  
    if input_data.get('second_address'):  # if second address was entered, else None
        if not are_duplicate(input_data.get('second_address'), shipping_data[2]):
            comment += f"{input_data.get('second_address')}\n"
        else:
            comment += "\r\n"             # add blank line
    else:
        comment += "\r\n"                 # add blank line
    # add city, state, zip
    comment += list_to_text(shipping_data[3:])
    return comment

# Testing   
# output['test'] = comment
# output['test_address_2'] = input_data.get('second_address')


# Main
shipping_data = input_data.get('shipping_data').split(';')
comment = get_comment(shipping_data)
add_story(input_data['gid'], comment)