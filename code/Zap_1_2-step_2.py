import json
import requests

# PARAMETERS 
input_data = { 'access_token' :	'' }
# /PARAMETERS 

order_dict = {}
orders = []

def GetStorage(access_token):
    url = 'https://store.zapier.com/api/records?secret=' + access_token
    return requests.get(url).json()

a = GetStorage(input_data['access_token'])
original_object = StoreClient(input_data['access_token'])
for item in dict.keys(a):
    order_dict.update({a[item]['date_time'] : item})

name = []
rate = []
payment_method = []
date_time = []
order_type = []
quantity = []
date = []
order = []

for item in sorted(order_dict.keys()):
    name.append(a[order_dict[item]]['name'])
    rate.append(a[order_dict[item]]['rate'])
    payment_method.append(a[order_dict[item]]['payment_method'])
    date_time.append(a[order_dict[item]]['date_time'])
    order_type.append(a[order_dict[item]]['order_type'])
    q = 0
    try:
        for i in range(len(a[order_dict[item]]['quantity'])):
            print(str(a[order_dict[item]]['quantity'][i]))          
            q += int(a[order_dict[item]]['quantity'][i])
    except:
        q = int(a[order_dict[item]]['quantity'])
    quantity.append(q)
    date.append(a[order_dict[item]]['date'])
    order.append(order_dict[item])

original_object.clear()
output = [{'name': name, 'rate': rate, 'payment_method': payment_method, 'date_time': date_time, 'order_type': order_type, 'quantity': quantity, 'date': date, 'order': order}]