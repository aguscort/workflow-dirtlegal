import re
from datetime import datetime

# PARAMETERS 
input_data = { 'create_task':	'',
    'asana_renewal':	'',
    'continueZap' : '',
    'pdfs_to_apply' : '',
    'ship_to_name': '',
    'order':	'',
    'customer_email':	'',
    'ship_to_phone':	'',
    'order_total':	'',
    'item_name':	'',
    'date':	'',
    'title_request':'',
    'asana_renewal_status': '',
    'OrderRaw': '',
    'item_name__1': ''}
# /PARAMETERS 

def CreateAsana(ship_to_name, order, customer_email, ship_to_phone, order_total, item_name, date, pdfs_to_apply, title_request, date_short):    
    req = requests.get('https://hooks.zapier.com/hooks/catch/4834230/o5unn5k/',params={"ship_to_name" : ship_to_name, "order" : order, "customer_email" : customer_email, "ship_to_phone" : ship_to_phone, "order_total" : order_total, "item_name" : item_name, "date" : date, "pdfs_to_apply" : pdfs_to_apply, "title_request" : title_request, "date_short" : date_short})
    
def Create_asana_renewal(ship_to_name, order, customer_email, ship_to_phone, order_total, item_name, date, asana_renewal_status, pdfs_to_apply, title_request, date_short):    
    req = requests.get('https://hooks.zapier.com/hooks/catch/4834230/o54pn8b/',params={"ship_to_name" : ship_to_name, "order" : order, "customer_email" : customer_email, "ship_to_phone" : ship_to_phone, "order_total" : order_total, "item_name" : item_name, "date" : date, "asana_renewal_status" : asana_renewal_status, "pdfs_to_apply" : pdfs_to_apply, "title_request" : title_request, "date_short" : date_short})   

def date_treatment(datetimeStr):
    # Date treatment, change formatting and set timezone
    dateTimeObj = datetime.strptime(datetimeStr[:-1], '%Y-%m-%dT%H:%M:%S.%f') #+ timedelta(hours=3)
    #return dateTimeObj.strftime('%m/%d/%Y %H:%M:%S'), dateTimeObj.strftime('%m/%d')
    return dateTimeObj.strftime('%m/%d/%Y %H:%M:%S'), "{:01d}/{:02d}".format(dateTimeObj.month,dateTimeObj.day)

date_long, date_short = date_treatment(input_data['date'])        
        
try:
    pdfs_to_apply = input_data['pdfs_to_apply']
except:
    pdfs_to_apply = ''
#try:
if input_data['create_task'] == 'True' and input_data['asana_renewal'] == 'False':
    CreateAsana(input_data['ship_to_name'], 
                input_data['order'], 
                input_data['customer_email'], 
                input_data['ship_to_phone'], 
                input_data['order_total'], 
                input_data['item_name'], 
                date_long, 
                pdfs_to_apply, 
                input_data['title_request'], 
                date_short)

if input_data['create_task'] == 'True' and input_data['asana_renewal'] == 'True' :
    Create_asana_renewal(input_data['ship_to_name'], 
                         input_data['order'], 
                         input_data['customer_email'], 
                         input_data['ship_to_phone'], 
                         input_data['order_total'], 
                         input_data['item_name'], 
                         date_long, 
                         input_data['asana_renewal_status'], 
                         pdfs_to_apply, 
                         input_data['title_request'], 
                         date_short)     
    
#except:
#    print("Some issue arose")
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