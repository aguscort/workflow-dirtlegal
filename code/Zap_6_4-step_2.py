output = {}

for i in range(len(input_data["vin"])):
    output.update({i: input_data["vin"][i]})    
for i in range(len(input_data["vin"]), 18):   
    output.update({i: "_"})   