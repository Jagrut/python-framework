import os
import json
from pprint import pprint
import sys

with open(os.path.join("/home","jk","juniper","jsoninput.json")) as data_file:
    data = json.load(data_file)
            
pprint(data)
list1=data.keys();
for key in list1:
	 open(os.path.join("/home","jk","juniper",key+"_config"),'w') 
print "checking"
print data["r0"]["interfaces"]["r1"]["xe-0/0/34"]
#sys.exit(2)
#for key in list1:
#	print key
#	connected_to_key=data[key]["interfaces"].keys()
#	for each_connected_to_key in connected_to_key:
#		connection_keys   = data[key]["interfaces"][each_connected_to_key].keys();
#		connection_values = data[key]["interfaces"][each_connected_to_key].values();
#		with open(os.path.join("/home","jk","juniper",key+"_config"),'a') as my_file:
#			for i in range (len(connection_keys)):
for key in list1:
	if("vlan_range" in data[key].keys()):
		range_var=data[key]["vlan_range"]
		range_array=range_var.split('-')
		print "range_arrya 0 == "+range_array[0]+"range_array 1 ==" + range_array[1]
		with open(os.path.join("/home","jk","juniper",key+"_config"),'a') as my_file:
			for i in range (int(range_array[0]),int(range_array[1])+1):
				my_file.write("set groups vlans vlans vlanL2_"+str(i) +" vlan-id "+ str(i)+ "\n");
			
						
				
		


