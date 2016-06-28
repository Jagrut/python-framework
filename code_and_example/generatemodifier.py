import yaml
import os
import json
from pprint import pprint
import sys
import re
import itertools

def ip_range(input_string):
    octets = input_string.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]
    ip_list = []
    for address in itertools.product(*ranges):
        yield '.'.join(map(str, address))

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
          open(os.path.join("./",each_target_list+"_config"),'w')
    x=len(data['PAS_STATIC_CMDS'])
    if("PAS_STATIC_CMDS" in list1):
    	while(x!=0):
		str=data['PAS_STATIC_CMDS'][x-1]['cmd']
		print type(str)
		target=data['PAS_STATIC_CMDS'][x-1]['targets']
		print target
		PAS_STATIC_CMDS(str,POOL_TO_LIST(target))
		x-=1
	needylist.remove("PAS_STATIC_CMDS")
    for each_need in needylist:
	target_length=len(data[each_need])
	str_tmp="set "+each_need+" "
	str_tmp_cp="set "+each_need+" "
	
	#command_list1.append(str_tmp)
	#print "target_length == "+str(target_length)+"\n\n"
	inside_went_or_not=0
	for i in range(target_length):
		command_list1=[]
		str_tmp=str_tmp_cp
		command_list1.append(str_tmp)
		recursive_modifier(data[each_need][i],command_list1,data[each_need][i]['TARGETS'])
    return data
def POOL_TO_LIST(pool):
        poollist=[]
        if ',' in pool :
                        val = pool.split(',')
                        for x in val :
                                if '-' in x :
                                        val1 = x.split('-')
                                        #print val1
                                        for ii in range(int(val1[0]),int(val1[1])+1,1):
                                                poollist.append(ii)
                                else :
                                        poollist.append(x)
        elif '-' in pool :
                val1 = pool.split('-')
                for ii in range(int(val1[0]),int(val1[1])+1,1):
                        poollist.append(ii)
        else :
		poollist.append(pool)
	return poollist

def PAS_STATIC_CMDS(Data,Targets) :
        NoOfTargets=len(Targets)
        while(NoOfTargets!=0) :
                file=Targets[(NoOfTargets-1)]+"_config"
                text_file = open(file, "a")
                text_file.write(Data)
                text_file.close()
                NoOfTargets-=1




def mixrange(s):
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l,h = map(int, i.split('-'))
            r+= range(l,h+1)
    return r

def recursive_modifier(data,command_list1,targets):
	#cp_command_list1=command_list1*1
	print "inside recursive modifiier whether_or_not == \n\n"
	#print "command_list1\n\n"
	print "first command list1 \n\n"
	pprint(command_list1)
	#if whether_or_not==1:
	#	target_list=data["TARGETS"].split(",")
	raw_command=data["VALUE"]
	raw_command_list=raw_command.split(' ')
	num=1
	print "first raw command list"
	pprint(raw_command_list)
	#print "data[$1]=="+"\n\n"
	#print data['$'+str(num)]
	#sys.exit(5)
	for i in xrange(len(raw_command_list)):
		if(re.search(r'.*\$(\d)',raw_command_list[i])):
			print "matched a number \n\n=="+str(i)+"\n\n"
			matchobj=re.search(r'.*\$(\d)',raw_command_list[i])
			num=matchobj.group(1)
			modifier_data=data['$'+str(num)]
			modifier_keys=modifier_data.keys()
			if ("START" in modifier_keys):
				if "MAPPING" in modifier_keys:
					if(modifier_data['MAPPING']=='one2one'):
						if "TYPE" in modifier_keys:
							print "call ipv4 or ipv6 next ip function mapping is one2one== \n\n"
							raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
							if (len(command_list1)!=int(modifier_data["COUNT"])):
                                                                print "inside if not equal to count 1 \n\n"
                                                                command_list1=command_list1*(int(modifier_data["COUNT"]))
                                                                print "commmand_list1 len==="+str(len(command_list1))+"\n\n"

							if(modifier_data["TYPE"]=="IPV4"):
								command_track=0
								for address in ip_range(modifier_data["START"]):
									if(command_track==int(modifier_keys["COUNT"])):
										break
									print "generated address is=="+address+"\n\n"
									command_list1[command_track]=command_list1[command_track]+" "+raw_command_list[i] +address
									command_track=command_track+1							
						else:
							print "mapping is  one2one== \n\n"
							start_index=int(modifier_data["START"])
							raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
							if (len(command_list1)!=int(modifier_data["COUNT"])):
								print "inside if not equal to count 1 \n\n"
								command_list1=command_list1*(int(modifier_data["COUNT"]))
								print "commmand_list1 len==="+str(len(command_list1))+"\n\n"
							for each_command in range(len(command_list1)):
								command_list1[each_command]=command_list1[each_command]+" "+raw_command_list[i]+str(start_index)
								start_index=start_index+1
							print "after one2one operation \n\n"
							pprint(command_list1)
					##one2one is ended here##
					else:
						if "TYPE" in modifier_keys:
							if(modifier_data["TYPE"]=="IPV4"):
								print "call ipv4 or ipv6 next ip function mapping is one2many== \n\n"
								raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
								initial_len=len(command_list1)
                                                        	command_tracker=0
                                                        	command_list1=command_list1*int(modifier_data["COUNT"])
								list_tracker=0
								for address in ip_range(modifier_data["START"]):
									if(command_tracker==int(modifier_data["COUNT"])):
                                                                                break
                                                                        print "generated address is=="+address+"\n\n"
									for ukl in range(list_tracker,list_tracker+initial_len):
										command_list1[ukl]=command_list1[ukl]+" "+raw_command_list[i] +address
									list_tracker=list_tracker+initial_len
									command_tracker=command_tracker+1
									
                                                        	
                                                        print "after one2many operation \n\n"
                                                        pprint(command_list1)
						else:
							
							start_index=int(modifier_data["START"])
							print "start index=="+str(start_index)+"\n\n"
							raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
							initial_len=len(command_list1)
							command_tracker=0
							command_list1=command_list1*int(modifier_data["COUNT"])
							for each_command in range(len(command_list1)):
								command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+str(start_index)
								command_tracker=command_tracker+1
								if(command_tracker==initial_len):
									start_index=start_index+1
									command_tracker=0
							print "after one2many operation \n\n"
                                                        pprint(command_list1)
					##one2many has ended here##
				else:
					print "please specify the mapping in your yaml file script aborting \n\n"
					sys.exit(3)
			else:
				if("MODE" in modifier_keys):
					mode_type=modifier_data['MODE']
					if(mode_type=="LIST"):
						ranges=modifier_data["sub_range"]
						ranges_list=ranges.split(',')
						if ("MAPPING" in modifier_keys):
							raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
							if(modifier_data['MAPPING']=='one2one'):
								if(len(ranges_list)!=len(command_list1)):
									command_list1=command_list1*len(ranges_list)
								for each_command in range(len(command_list1)):
									command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[each_command]
							else:
								initial_len=len(command_list1)
								command_tracker=0
								real_index=0
								add_num=initial_len
								command_list1=command_list1*len(ranges_list)
								for each_command in range(len(command_list1)):
                                                                	command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[real_index]
                                                                	command_tracker=command_tracker+1
                                                                	if(command_tracker==initial_len):
                                                                        	real_index=real_index+1
										initial_len=initial_len+add_num
										#start_index=start_index+1
                                                                        	#command_tracker=command_tracker+1
								
						else:
							print "please specify the mapping in your yaml file script aborting \n\n"
                                         		sys.exit(4)

						
					elif(mode_type=="EXPAND"):
						ranges=modifier_data["sub_range"]
                                                ranges_list=mixrange(ranges)
						if("MAPPING" in modifier_keys):
							raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
							if(modifier_data['MAPPING']=='one2one'):
                                                                if(len(ranges_list)!=len(command_list1)):
                                                                        command_list1=command_list1*len(ranges_list)
                                                                for each_command in range(len(command_list1)):
                                                                        command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[each_command]
							else:
                                                                initial_len=len(command_list1)
                                                                command_tracker=0
                                                                real_index=0
                                                                add_num=initial_len
                                                                command_list1=command_list1*len(ranges_list)
                                                                for each_command in range(len(command_list1)):
                                                                        command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[real_index]
                                                                        command_tracker=command_tracker+1
                                                                        if(command_tracker==initial_len):
                                                                                real_index=real_index+1
                                                                                initial_len=initial_len+add_num
                                                                                #start_index=start_index+1
                                                                                #command_tracker=command_tracker+1

						else:
							print "please specify the mapping in your yaml file script aborting \n\n"
                                                        sys.exit(8)
						
						
				else:
					print "please specify the mode list or expand in your yaml file script aborting \n\n"
					sys.exit(2)
		else:
			#command_list1=[raw_command_list[i]+"  ".format(i) for pk in command_list1]
			for pq in range(len(command_list1)):
				command_list1[pq]=command_list1[pq]+" "+raw_command_list[i]+" "	
				
	print "\n\n "+raw_command+"\n\n"
	target_array=targets.split(",")
	for each_file in target_array:
		with open(os.path.join("/home","jk","juniper",each_file+"_config"),'a') as my_file:
			for each_comm in command_list1:
				my_file.write(each_comm+"\n")
				

	
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
	filepath = "./example/example2cp.yaml"
	
	data = yaml_reader(filepath)
	#x = data['VLAN_POOL1']['VLAN_POOL_IPV4']['RANGE']
	#config_vlan(x)
