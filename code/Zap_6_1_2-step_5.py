import json
import requests
from datetime import datetime


# PARAMETERS 
input_data = { 'item_name':	'',
    'wo':	'',
    'text' : '',
    'name' : '',
    'sku': '',
    'apikey_shipstation':	'',
    'password_shipstation' : '' }
# /PARAMETERS 

def date_today():
    # Date treatment
    datetoday = datetime.utcnow() #- timedelta(hours=8)
    day = datetoday.strftime('%d')
    month = datetoday.strftime('%B')
    year = datetoday.strftime('%y')
    return day, month, year

def create_title_request(tr_lien_holder_name, tr_lien_holder_addres_1, tr_lien_holder_address_2, tr_day, tr_month, tr_year, tr_vehicle_year, tr_vehicle_make, tr_vehicle_serial, tr_vehicle_owner, tr_vehicle_adress, tr_vehicle_adress2, tr_account, wo):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o4gnv9l/'
    print("create_title_request")
    data = {"tr_lien_holder_name" : tr_lien_holder_name, "tr_lien_holder_addres_1" : tr_lien_holder_addres_1,   "tr_lien_holder_address_2" : tr_lien_holder_address_2, "tr_day" : tr_day, "tr_month" :tr_month,  "tr_year" : tr_year, "tr_vehicle_year" : tr_vehicle_year,  "tr_vehicle_make" : tr_vehicle_make, "tr_vehicle_serial" : tr_vehicle_serial, "tr_vehicle_owner" : tr_vehicle_owner, "tr_vehicle_adress" : tr_vehicle_adress + " " + tr_vehicle_adress2, "tr_account" : tr_account, "wo" : wo }
    return requests.post(url, data=json.dumps(data),)

def create_ut_vin_inspection(pdf_vehicle_owner, pdf_vin, pdf_year,  pdf_make,  pdf_model,  pdf_vehicle_adress,  pdf_vehicle_adress2, wo):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o4g7tca/'
    print("create_ut_vin_inspection")
    data = { "pdf_vehicle_owner" : pdf_vehicle_owner,  "pdf_vin" : pdf_vin, "pdf_year" : pdf_year, "pdf_make" : pdf_make, "pdf_model" : pdf_model, "pdf_vehicle_adress" : pdf_vehicle_adress, "pdf_vehicle_adress2" : pdf_vehicle_adress2, "wo" : wo  }
    return requests.post(url, data=json.dumps(data),)    
    
def create_vt_inspection_form_with_letterhead(pdf_vehicle_owner, pdf_vin, pdf_year,  pdf_make,  pdf_model,  pdf_vehicle_adress,  pdf_vehicle_adress2, pdf_mileage, wo):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o4g7tj5/'
    print("vt_inspection_form_with_letterhead")
    data = { "pdf_vehicle_owner" : pdf_vehicle_owner,  "pdf_vin" : pdf_vin, "pdf_year" : pdf_year, "pdf_make" : pdf_make, "pdf_model" : pdf_model, "pdf_vehicle_adress" : pdf_vehicle_adress, "pdf_vehicle_adress2" : pdf_vehicle_adress2, "pdf_mileage": pdf_mileage, "wo" : wo  }
    return requests.post(url, data=json.dumps(data),)
    
def create_vt_title_app(pdf_vehicle_owner, pdf_vin, pdf_year,  pdf_make,  pdf_model,  pdf_vehicle_adress,  pdf_vehicle_adress2, pdf_city , pdf_state , pdf_zip , pdf_color, pdf_mileage, pdf_ccs, wo, name, pdf_body_type, pdf_wheels):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o635mec/'
    print("vt_title_app")
    data = { "pdf_vehicle_owner" : pdf_vehicle_owner,  "pdf_vin" : pdf_vin, "pdf_year" : pdf_year, "pdf_make" : pdf_make, "pdf_model" : pdf_model, "pdf_vehicle_adress" : pdf_vehicle_adress, "pdf_vehicle_adress2" : pdf_vehicle_adress2, "pdf_city" : pdf_city , "pdf_state" : pdf_state , "pdf_zip" : pdf_zip , "pdf_color" : pdf_color,  "pdf_mileage": pdf_mileage, "pdf_ccs" : pdf_ccs, "wo" : wo , "name" : name, "pdf_body_type" : pdf_body_type, "pdf_wheels" : pdf_wheels  }
    return requests.post(url, data=json.dumps(data),)  

def create_ut_title_app(pdf_vehicle_owner, pdf_vin, pdf_year,  pdf_make,  pdf_model,  pdf_vehicle_adress,  pdf_vehicle_adress2, pdf_city , pdf_state , pdf_zip , pdf_color, pdf_mileage, pdf_ccs, wo, name):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o635mrg/'
    print("ut_title_app")
    data = { "pdf_vehicle_owner" : pdf_vehicle_owner,  "pdf_vin" : pdf_vin, "pdf_year" : pdf_year, "pdf_make" : pdf_make, "pdf_model" : pdf_model, "pdf_vehicle_adress" : pdf_vehicle_adress, "pdf_vehicle_adress2" : pdf_vehicle_adress2, "pdf_city" : pdf_city , "pdf_state" : pdf_state , "pdf_zip" : pdf_zip , "pdf_color" : pdf_color,  "pdf_mileage": pdf_mileage, "pdf_ccs" : pdf_ccs, "wo" : wo , "name" : name  }
    return requests.post(url, data=json.dumps(data),)

def create_sd_lien_cover_sheet(tr_lien_holder_name, tr_vehicle_year, tr_vehicle_make,  tr_vehicle_model, tr_vehicle_serial, tr_vehicle_owner, tr_account, wo):
    url = 'https://hooks.zapier.com/hooks/catch/4834230/o6wlqor/'
    print("sd_lien_cover")
    data = { "tr_lien_holder_name" : tr_lien_holder_name, "vehicle" : tr_vehicle_year + " " + tr_vehicle_make + " " + tr_vehicle_model, "tr_vehicle_serial" : tr_vehicle_serial, "tr_vehicle_owner" : tr_vehicle_owner, "tr_account" : tr_account, "wo" : wo}
    return requests.post(url, data=json.dumps(data),)

#
# Get Data
#
count = 0
text_list = str(input_data['text']).split("\r\n\r\n")
name = text_list[0].split(":")[1].strip()
address = text_list[1].split(":")[1].upper()
print(str(text_list))
try:
    match = re.findall(r'[\w\.-]+@[\w\.-]+', input_data['text'])    
    email = match[0].strip()
except:
    email = ""
phone = input_data['text'].split("Phone:")[1].split("Email:")[0]
phone = re.sub(r'[\D-]','',phone)
#
# Get for TR PDF
#
tr_vehicle_owner = text_list[0].split(":")[1].strip().upper()
tr_vehicle_adress = address.split(",")[0].strip()
tr_vehicle_adress2 = ", ".join(address.split(",")[1:]).strip()
tr_vehicle_adress2 = " ".join(tr_vehicle_adress2.split("\r\n")).strip()
tr_vehicle_serial = str(text_list[8].split(":")[1]).upper()    
try:
    tr_vehicle_year =  text_list[4].split(":")[1]  
except:
    tr_vehicle_year =  ""
try:
    tr_vehicle_make =  text_list[5].split(":")[1]   
except:    
    tr_vehicle_make =  ""
try:
    tr_vehicle_model =  text_list[6].split(":")[1] 
except:    
    tr_vehicle_model = ""    
tr_day, tr_month, tr_year = date_today()
tr_account = text_list[16].split(":")[1].strip()
try:
    tr_lien_holder_name = text_list[14].split(":")[1].strip()
    tr_lien_holder_addres_1 = text_list[15].split(":")[1].strip()
    tr_lien_holder_address_2 = ""
except:
    tr_lien_holder_name = ""
    tr_lien_holder_addres_1 = ""
    tr_lien_holder_address_2 = ""
#
# Get for PDF
#
pdf_vehicle_owner = text_list[0].split(":")[1].strip().upper()
pdf_vehicle_adress = address.split(",")[0].strip()
pdf_vehicle_adress2 = ", ".join(address.split(",")[1:]).strip()
pdf_vehicle_adress2 = " ".join(pdf_vehicle_adress2.split("\r\n")).strip()
pdf_city =  pdf_vehicle_adress2.split(",")[0].strip()
pdf_state = pdf_vehicle_adress2.split(",")[1].split(" ")[0].strip()
pdf_zip = pdf_vehicle_adress2.split(",")[1].split(" ")[1].strip()
pdf_vin = str(text_list[8].split(":")[1]).upper()
pdf_mileage = str(text_list[10].split(":")[1])
try:
    pdf_year =  text_list[4].split(":")[1]  
except:
    pdf_year =  ""
try:
    pdf_make =  text_list[5].split(":")[1]   
except:    
    pdf_make =  ""
try:
    pdf_model =  text_list[6].split(":")[1] 
except:    
    pdf_model = ""
try:
    pdf_color = text_list[9].split(":")[1] 
except:    
    pdf_color = ""    
try:
    pdf_ccs = str(text_list[7].split(":")[1])
except:    
    pdf_ccs = ""
#
# Body Type
# (Dirt Bike Conversion, ATV Conversion, UTV Conversion, Roxor Conversion, Military Conversion, Custom Street Legal Conversion, Golf Cart Conversion,Vehicle Registration Renewal)
#
pdf_body_type = ""
if input_data["item_name"].find("Dirt Bike") != -1:
    pdf_body_type = "MC"
elif input_data["item_name"].find("ATV") != -1:
    pdf_body_type = "ATV"    
elif input_data["item_name"].find("UTV") != -1:
    pdf_body_type = "UTV"    
elif input_data["item_name"].find("Military") != -1:
    pdf_body_type = "Truck"    
else:
    pdf_body_type = ""    
#
# Wheels
#
pdf_wheels = ""
if input_data["item_name"].find("Dirt Bike") != -1:
    pdf_wheels = "2"
elif input_data["item_name"].find("ATV") != -1:
    pdf_wheels = "4"    
elif input_data["item_name"].find("UTV") != -1:
    pdf_wheels = "4"      
else:
    pdf_body_type = ""
    pdf_ccs = "" # Leave this field blank
    
# Send Autofilled PDF
s1_title_request_pdf_asana = ["SQ5997142","SQ9575974","SQ4359210","SQ6193077","SQ3509691","SQ7202884","SQ9493879","SQ1624128","SQ9857937","SQ9579630","SQ6283166","SQ8910742"]
s1_ut_vin_inspection_pdf_asana = ["SQ5548002","SQ2127240"]
s1_vt_inspection_form_with_letterhead_pdf_asana = ["SQ8811460","SQ8403421","SQ1235346","SQ0550038","SQ0910340","SQ0559800","SQ3553182","SQ0355699","SQ0038404","SQ9197192","SQ2127240"]
s2_vt_title_app = ["SQ8811460","SQ8403421","SQ1235346","SQ0550038","SQ0910340","SQ0559800","SQ3553182","SQ0355699","SQ0038404","SQ9197192","SQ0495127"]
s2_vt_title_app_for_ut_transfer = ["SQ2127240"]
s2_ut_title_app = ["SQ5548002","SQ2127240"]
s2_sd_lien_cover_sheet = ["SQ5997142", "SQ9575974", "SQ4359210", "SQ6193077", "SQ3509691", "SQ7202884", "SQ9493879", "SQ1624128", "SQ9857937", "SQ9579630", "SQ6283166", "SQ8910742"]

if input_data['sku'] in s1_title_request_pdf_asana:
    create_title_request(tr_lien_holder_name, tr_lien_holder_addres_1, tr_lien_holder_address_2, tr_day, tr_month, tr_year, tr_vehicle_year, tr_vehicle_make, tr_vehicle_serial, tr_vehicle_owner, tr_vehicle_adress, tr_vehicle_adress2, tr_account, input_data["wo"])  

if input_data['sku'] in s1_ut_vin_inspection_pdf_asana:     
    create_ut_vin_inspection(pdf_vehicle_owner, pdf_vin, pdf_year,  pdf_make,  pdf_model,  pdf_vehicle_adress,  pdf_vehicle_adress2, input_data["wo"])

if input_data['sku'] in s1_vt_inspection_form_with_letterhead_pdf_asana:     
    create_vt_inspection_form_with_letterhead(pdf_vehicle_owner, pdf_vin, pdf_year,  pdf_make,  pdf_model,  pdf_vehicle_adress,  pdf_vehicle_adress2, pdf_mileage, input_data["wo"])       
    
if input_data['sku'] in s2_vt_title_app:
    create_vt_title_app(pdf_vehicle_owner, pdf_vin, pdf_year,  pdf_make,  pdf_model,  pdf_vehicle_adress,  pdf_vehicle_adress2, pdf_city , pdf_state , pdf_zip , pdf_color, pdf_mileage, pdf_ccs, input_data["wo"], input_data["name"],  pdf_body_type, pdf_wheels)

if input_data['sku'] in s2_vt_title_app_for_ut_transfer:
    create_vt_title_app(pdf_vehicle_owner, pdf_vin, pdf_year,  pdf_make,  pdf_model,  "3169 E Atlantic Blvd #137",  "", "POMPANO BEACH" , "FL" , "33062" , pdf_color, pdf_mileage, pdf_ccs, input_data["wo"], input_data["name"],  pdf_body_type, pdf_wheels)

if input_data['sku'] in s2_ut_title_app:
    create_ut_title_app(pdf_vehicle_owner, pdf_vin, pdf_year,  pdf_make,  pdf_model,  pdf_vehicle_adress,  pdf_vehicle_adress2, pdf_city , pdf_state , pdf_zip , pdf_color, pdf_mileage, pdf_ccs, input_data["wo"], input_data["name"]) 

if input_data['sku'] in s2_sd_lien_cover_sheet:
    create_sd_lien_cover_sheet(tr_lien_holder_name, tr_vehicle_year, tr_vehicle_make,  tr_vehicle_model, tr_vehicle_serial, tr_vehicle_owner, tr_account, input_data["wo"])