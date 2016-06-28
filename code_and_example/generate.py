import yaml
import os
import json
from pprint import pprint
import sys

def yaml_reader(filepath):
    file = open(filepath,"r")
    data=yaml.load(file)
    print "data keys\n\n"
    pprint(data)
    print "data keys now real\n\n"
    list1=data.keys()
    needylist=[]
    for each_list1 in list1:
	if isinstance(data[each_list1],list):
		#print "see this chutiya==="+data[each_list1]+"\n"
		needylist.append(each_list1)
    print "\n\n\n\n\n"
    #for each_list1 in list1:
    #    if not isinstance(data[each_list1],list):
    #            print "real list without junk==="+data[each_list1]+"\n"
    #yaml_chunk=data['groups vlans_irb vlans'][0]['MODIFIER']
    print "checking yaml chunk\n\n\n"
    #pprint(yaml_chunk);
    print "checking yaml chunk end \n\n\n"
    pprint(data.keys())
    print "end\n\n"
    #sys.exit(2)
    pprint(needylist)
    target_list=data["TARGETS"].split(",")
    for each_target_list in target_list:
          open(os.path.join("/home","jk","juniper",each_target_list+"_config"),'w')

    for each_need in needylist:
	target_length=len(data[each_need])
	str_tmp="set "+each_need+" "
	str_tmp_cp="set "+each_need+" "
	
	#command_list1.append(str_tmp)
	print "target_length == "+str(target_length)+"\n\n"
	inside_went_or_not=0
	for i in range(target_length):
		command_list1=[]
		str_tmp=str_tmp_cp
		if('VALUE_PREFIX' in data[each_need][i].keys()):
			print "value_prefix exists \n\n"
               		str_tmp=str_tmp+" "+data[each_need][i]['VALUE_PREFIX']
			#str_tmp_cp=str_tmp
       		if('VALUE' in data[each_need][i].keys()):
			print "value exists in \n\n"
               		range_array=data[each_need][i]['VALUE'].split('-')
               		for j in range (int(range_array[0]),int(range_array[1])+1):
				#print "j==="+"\n\n"
		       		str_tmp=str_tmp_cp
                       		if('VALUE_SUFFIX' in data[each_need][i].keys()):
                               		str_tmp=str_tmp+str(j)+data[each_need][i]['VALUE_SUFFIX']
                       		else:
                               		str_tmp=str_tmp+str(j)
				command_list1.append(str_tmp)
				inside_went_or_not=1
		if(inside_went_or_not==0):
			command_list1.append(str_tmp)
		
		#whether_or_not=
		recursive_modifier(data[each_need][i],command_list1,int(data[each_need][i]['NOT_START_EXPAND']),data[each_need][i]['TARGETS'])
	#sys.exit(2)
	#target_list=target.split(",")
	#for each_target_list in target_list:
	#	open(os.path.join("/home","jk","juniper",each_target_list+"_config"),'w')
#	if('VALUE_PREFIX' in data[each_need].keys()):
#		str_tmp=str_tmp+" "+data[each_need]['VALUE_PREFIX']
#	if('VALUE' in data[each_need].keys()):
#		range_array=data[each_need]['VALUE'].split('-')
#		for i in range (int(range_array[0]),int(range_array[1])+1):
#			if('VALUE_SUFFIX' in data[each_need].keys()):
#				str_tmp=str_tmp+i+data[each_need]['VALUE_SUFFIX']
#			else:
#				str_tmp=str_tmp+i
	#command_list1.append(str_tmp)
    #recursive_modifier(command_list1,data,needylist)	
    return data
def recursive_modifier(data,command_list1,whether_or_not,targets):
	cp_command_list1=command_list1*1
	expanded=0
	print "inside recursive modifiier whether_or_not == \n\n"+str(whether_or_not)+"\n"
	print "command_list1\n\n"
	pprint(command_list1)
	#if whether_or_not==1:
	#	target_list=data["TARGETS"].split(",")
	if "MODIFIER" in data.keys():
		print "yes modifier exists in data.keys\n\n"
		modifier_keys=data["MODIFIER"].keys()
		for each_modifier_keys in modifier_keys:
			print "inside each modifier keys for loop\n\n"
			expanded=0
			command_list1=cp_command_list1*1
        		if("VALUE" in data["MODIFIER"][each_modifier_keys].keys() and whether_or_not==0):
                		#tmp_str=" "+each_modifier_keys
				print "value exists in for loop"
				range_array=data["MODIFIER"][each_modifier_keys]["VALUE"].split('-')
                        	command_list1=command_list1*(int(range_array[1])-int(range_array[0])+1)
				expanded=1
				print "command list1 pprint show\n\n"
				pprint(command_list1)
			#for each_command in command_list1:
			track=0
			tmp_str=" "+each_modifier_keys+" "
			prefix_var=0
			if("VALUE_PREFIX" in data["MODIFIER"][each_modifier_keys].keys()):
				tmp_str=tmp_str+ " " + data["MODIFIER"][each_modifier_keys]["VALUE_PREFIX"]
				prefix_var=1
			if("VALUE" in data["MODIFIER"][each_modifier_keys].keys()):
				another_range_array=data["MODIFIER"][each_modifier_keys]["VALUE"].split('-')
				for i in range (int(another_range_array[0]),int(another_range_array[1])+1):
					if(prefix_var==1):
						tmp_str=" "+each_modifier_keys+" " + data["MODIFIER"][each_modifier_keys]["VALUE_PREFIX"]
					else:
						tmp_str=" "+each_modifier_keys+" "
					print "dfsf"
					if("VALUE_SUFFIX" in data["MODIFIER"][each_modifier_keys].keys()):
						tmp_str=tmp_str+str(i)+data["MODIFIER"][each_modifier_keys]["VALUE_SUFFIX"]
					else:
						tmp_str=tmp_str+str(i)
					print "aaa"
					if expanded==1:
						iter_for=int(len(command_list1)/(int(range_array[1])-int(range_array[0])+1))
						print "item_for"+str(iter_for)+"\n\n"
						for k in range(iter_for):
							command_list1[track]=command_list1[track]+tmp_str
							track=track+1
					else:
						command_list1[track]=command_list1[track]+tmp_str
                                                track=track+1

			print("command list to watch")
			pprint(command_list1)
			if("MODIFIER" in data["MODIFIER"][each_modifier_keys].keys()):
				recursive_modifier(data["MODIFIER"][each_modifier_keys],command_list1,0,targets)
			else:
				target_array=targets.split(",")
				for each_file in target_array:
					with open(os.path.join("/home","jk","juniper",each_file+"_config"),'a') as my_file:
						for each_comm in command_list1:
							my_file.write(each_comm+"\n")
				
#def recursive_modifier(command_list1,data,needylist):
#	cp_command_list1=command_list1
#	for each_need in needylist:
#		if "MODIFIER" in data[each_need].keys():
#			if("VALUE" in data[each_need]["MODIFIER"].keys()):
#                        	range_array=data[each_need]["MODIFIER"]["VALUE"].split('-')
#				command_list1=command_list1*(int(range_array[1])-int(range_array[0])+1)
#			for inx,each_command in enumerate(command_list):
#				track=0
#				tmp_list=data[each_need]["MODIFIER"].keys()
#				for each_tmp_item in tmp_list:
#					tmp_str=" "
#					command_list1=cp_command_list1
#					if("VALUE_PREFIX" in data[each_need]["MODIFIER"].keys()):
#                				tmp_str=tmp_str+" "+data[each_need]["MODIFIER"]["VALUE_PREFIX"]
#        				if("VALUE" in data[each_need]["MODIFIER"].keys()):
#                				range_array=data[each_need]["MODIFIER"]["VALUE"].split('-')
#                				for i in range (int(range_array[0]),int(range_array[1])+1):
#                        				if("VALUE_SUFFIX" in data[each_need]["MODIFIER"].keys()):
#                                				tmp_str=tmp_str+i+data[each_need]["MODIFIER"]['VALUE_SUFFIX']
#                        				else:
#                                				tmp_str=tmp_str+i
#                        				command_list1[track]=command_list1[track]+tmp_str
#							track=track+1
#
			
		
#def yaml_checker(data):	

	
def config_vlan(data) :
	
	if '-' in data :
		val = data.split('-')
		for i in range(int(val[0]),int(val[1])+1,1):
			print "set groups vlan vlan vlan_L2_",i," vlan_id ",i;
	elif ',' in data :
		val = data.split(',')
		for i in val :
			print "set groups vlan vlan vlan_L2_",i," vlan_id ",i;
	else :
		print "###### PLEASE ENTER CORRECT FORMAT ##############";

			
		

if  __name__ == "__main__" :
	filepath = "mmohan.yaml"
	
	data = yaml_reader(filepath)
	#x = data['VLAN_POOL1']['VLAN_POOL_IPV4']['RANGE']
	#config_vlan(x)
