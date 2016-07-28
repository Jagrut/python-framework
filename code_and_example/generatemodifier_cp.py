import yaml
import os
import json
from pprint import pprint
import sys
import re
import itertools
from netaddr import *

total_targets=[]
def generate_ip(ip_addr,ip_step,ip_count):
	ip_addr_list=[]
	ip_addr_list.append(ip_addr)
	prefix=0
	if(ip_step=='x'):
		network_host=ip_addr.split('/')
		if(len(network_host)==1):
			print "You haven't define step either mask aborting scipt\n\n"
			sys.exit(1)
		else:
			network_host[0]=network_host[0]+"/0"
			prefix=int(network_host[1])
			if(prefix==32):
				ip_step='0.0.0.1'
			elif(prefix==24):
				ip_step='0.0.1.0'
			elif(prefix==16):
				ip_step="0.1.0.0"
			elif(prefix==8):
				ip_step='1.0.0.0'

		
	if not(ip_step=='x'):
		network_host=ip_addr.split('/')
		if(len(network_host)==1):
			ip_addr=ip_addr+"/0"
			ip = IPNetwork(ip_addr)
		else:
			network_host[0]=network_host[0]+"/0"
			prefix=network_host[1]
			ip = IPNetwork(ip_addr)
		step_ip=IPAddress(ip_step)
		num_to_increase=int(step_ip)
		count=1
		while(count<=ip_count):
			if prefix==0:
				ip_addr_list.append(str(ip.ip+count*num_to_increase))
			else:
				ip_addr_list.append(str(ip.ip+count*num_to_increase)+"/"+network_host[1])
			count=count+1
	return ip_addr_list
def ip_range(input_string):
     network_host=input_string.split('/')
     #octets = network_host[0]
     octets = network_host[0].split('.')
     r=[]
     ranges=[]
      
     for octet in octets: 
         if ',' in octet: 
                 for i in octet.split(','):
                         if '-' not in i:
                                 r.append(int(i))
                                 #ranges.append(r)
                                 #r=[]
                         else:   
                                 l,h=map(int,i.split('-'))
                                 #r+=[range(l,h+1)]
                                 for kpl in range(l,h+1):
                                        r.append(kpl)
                                 
                                 #ranges.append(r)
                                 #r=[]
                 ranges.append(r)
         else:   
                 if '-' not in octet:
                         r.append(int(octet))
                         ranges.append(r)
                         r=[]
                 else:   
                         l,h=map(int,octet.split('-'))
                         for kpl in range(l,h+1):
                                 r.append(kpl)
                         ranges.append(r)
                         r=[]
 
     print "new ranges__==\n\n"
     pprint(ranges)
     #chunks = [map(int, octet.split('-')) for octet in octets]
     for address in itertools.product(*ranges):
         yield '.'.join(map(str, address)) +'/'+network_host[1]


def yaml_reader(filepath):
    file = open(filepath,"r")
    data=yaml.load(file)
    print "data keys\n\n"
    pprint(data)
    print "data keys now real\n\n"
    list1=data.keys()
    #if(data['ipclos_fbf1']['list'][0]['set groups ipclos_fbf routing-options interface-routes rib-group inet fbf-group'] is None):
    #    print "None\n"
    #else:
    #    print "Not None\n"
    #sys.exit(28)
    needylist=[]
    for each_list1 in list1:
	if isinstance(data[each_list1],dict) or isinstance(data[each_list1],list) :
		needylist.append(each_list1)
			
    print "\n\n\n\n\n"
    #for each_list1 in list1:
    #    if not isinstance(data[each_list1],list):
    #            print "real list without junk==="+data[each_list1]+"\n"
    #yaml_chunk=data['groups vlans_irb vlans'][0]['MODIFIER']
    print "checking  yaml chunk\n\n\n"
    #pprint(yaml_chunk);
    print "checking yaml chunk end \n\n\n"
    pprint(data.keys())
    print "end\n\n"
    #sys.exit(2)
    if 'PAS_CONFIGS' in needylist:
	needylist.remove('PAS_CONFIGS')
    if 'PAS_CONFIG_MAPS' in needylist:
	needylist.remove('PAS_CONFIG_MAPS')
    print "needy list start \n"
    pprint(needylist)
    print "needy list end \n"
    static_cmd_dict={}
    if ("PAS_CONFIGS" in list1):
	pas_config_tags=data["PAS_CONFIGS"].keys()
	for each_pas_config_tag in pas_config_tags:
		command_set=data["PAS_CONFIGS"][each_pas_config_tag]
		if("GRPID" in command_set.keys()):
			static_cmd_dict[each_pas_config_tag]="set groups "+command_set["GRPID"]
		else:
			static_cmd_dict[each_pas_config_tag]="set groups "+each_pas_config_tag
		temp_cmd=static_cmd_dict[each_pas_config_tag]
		if isinstance(command_set,list):
			tmp_static_cmd_str=static_cmd_dict[each_pas_config_tag]
                        static_cmd_dict[each_pas_config_tag]=static_cmd_dict[each_pas_config_tag]+" " + command_set[0]+" \n"
                        for command_set_itr in range(1,len(command_set)):
                                static_cmd_dict[each_pas_config_tag]=static_cmd_dict[each_pas_config_tag]+" "+tmp_static_cmd_str+" " + command_set[command_set_itr]+" \n"
			print "hi hello how r u?\n"
		else:
			tag_keys=command_set.keys()
			for each_tag_key in tag_keys:
				if isinstance(command_set[each_tag_key],list):
					static_cmd_dict[each_pas_config_tag]=static_cmd_dict[each_pas_config_tag]+" "+each_tag_key
					tmp_static_cmd_str=static_cmd_dict[each_pas_config_tag]
					static_cmd_dict[each_pas_config_tag]=static_cmd_dict[each_pas_config_tag]+" " + command_set[each_tag_key][0]+" \n"
					for command_set_itr in range(1,len(command_set[each_tag_key])):
						static_cmd_dict[each_pas_config_tag]=static_cmd_dict[each_pas_config_tag]+" "+tmp_static_cmd_str+" " + command_set[each_tag_key][command_set_itr]+" \n"
    	print "before static cmd dict\n\n"
    	pprint(static_cmd_dict)
    	print "after static cmd dict\n\n"
	if("PAS_CONFIG_MAPS" in list1):
		maps_device=data["PAS_CONFIG_MAPS"]
		map_list=maps_device.keys()
		for each_map_device in map_list:
			regex = re.compile(r"\s*r\s*", flags=re.I)
			map_device_ind_list=regex.split(each_map_device)
			if '' in map_device_ind_list:
				map_device_ind_list.remove('')
			tmp_list=[]
			for each_generate_list in map_device_ind_list :
				tmp_list=tmp_list+mixrange(each_generate_list)

			if(isinstance(maps_device[each_map_device],list)):
				for write_data in range(len(maps_device[each_map_device])) :
					PAS_STATIC_CMDS(static_cmd_dict[maps_device[each_map_device][write_data]],tmp_list)					
			else:
				map_devices_list=str(maps_device[each_map_device]).split(",")
				for write_data in range(len(map_devices_list)) :
                                	PAS_STATIC_CMDS(static_cmd_dict[map_devices_list[write_data]],tmp_list)
			
	else:
		print "you have defined PAS_CONFIG KEY but forgot to create PAS_CONFIG_MAPS keys aborting script\n\n"			
    #	sys.exit(29)
    #target_list=data["TARGETS"].split(",")
    #for each_target_list in target_list:
    #      open(os.path.join("./",each_target_list+"_config"),'w')
    #x=len(data['PAS_STATIC_CMDS'])
    #if("PAS_STATIC_CMDS" in list1):
    #	while(x!=0):
    #    	str=data['PAS_STATIC_CMDS'][x-1]['cmd']
    #    	print type(str)
    #    	target=data['PAS_STATIC_CMDS'][x-1]['targets']
    #    	print target
    #    	PAS_STATIC_CMDS(str,POOL_TO_LIST(target))
    #    	x-=1
    #    needylist.remove("PAS_STATIC_CMDS")
    
    for each_need in needylist:
	print "\n inside main for loop start\n"
	command_list1=[]
	#str_tmp=str_tmp_cp
	
	needylist_dict=data[each_need]
	needylist_keys=needylist_dict.keys()


	if "GRPID" in data[each_need].keys():
		str_tmp="set groups "+data[each_need]["GRPID"]+" "
		needylist_keys.remove("GRPID")
	else:
		str_tmp="set groups "+each_need+" "
	command_list1.append(str_tmp)
	
	#command_list1.append(str_tmp)
	#print "target_length == "+str(target_length)+"\n\n"
	#inside_went_or_not=0
	if ("TARGETS" in needylist_keys):
		regex = re.compile(r"\s*r\s*", flags=re.I)
                needy_device_ind_list=regex.split(data[each_need]["TARGETS"])
                if '' in needy_device_ind_list:
                        needy_device_ind_list.remove('')
                tmp_list=[]
                for each_generate_list in needy_device_ind_list :
                        tmp_list=tmp_list+mixrange(each_generate_list)
		for each_outer_needylist_keys in needylist_keys:
			if not (re.search(r"\s*target\s*",each_outer_needylist_keys,re.IGNORECASE)):
				recursive_modifier(data[each_need],each_need,each_outer_needylist_keys,command_list1,tmp_list)
				needylist_keys.remove(each_outer_needylist_keys)	
		needylist_keys.remove("TARGETS")
		#target_list=mixrangedata[each_need]["TARGETS"]
	tmp_device_list=[]
	where_is_list(data[each_need],needylist_keys,each_need,command_list1,tmp_device_list)
	#for iter_needylist_keys in needylist_keys:
	#	if (re.search(r"\s*target\s*",iter_needylist_keys,re.IGNORECASE)):
	#		if(isinstance(data[each_need][iter_needylist_keys],list)):
					
	#needylist_target_cnt=0
	#for each_needylist_keys in needylist_keys:
	#	if(re.search(r"\s*target\s*",raw_command_list[i])):
	#		needylist_target_cnt=needylist_target_cnt+1
		
	#recursive_modifier(data[each_need][i],command_list1,data[each_need][i]['TARGETS'])
    return data
def where_is_list(data,needylist_keys,each_need,command_list1,tmp_list):
	print "\ninside where_is_list \n"
	for iter_needylist_keys in needylist_keys:
		recursive_list=[]
                if(isinstance(data[iter_needylist_keys],dict)):
			recursive_list=data[iter_needylist_keys].keys()
			if (re.search(r"\s*target\s*",iter_needylist_keys,re.IGNORECASE)):
				tmp_list=[]
				last_underscore=iter_needylist_keys.rfind('_')
	                        actual_range=iter_needylist_keys[last_underscore+2:]
        	                tmp_list=mixrange(actual_range)
				for each_recursive_list in recursive_list:
					if(isinstance(data[iter_needylist_keys][each_recursive_list],list)):
						recursive_modifier(data[iter_needylist_keys],each_need,each_recursive_list,command_list1,tmp_list)
					else:
						where_is_list(data[iter_needylist_keys],recursive_list,each_need,command_list1,tmp_list)
			else:
				#if ("list" in recursive_list):
				print "\ncalling recursive_modifier form inside whereislist \n"
				print "\ntmp_list start \n"
				pprint(tmp_list)
				print "\ntmp_list end \n"
				#recursive_modifier(data[iter_needylist_keys],each_need,"list",command_list1,tmp_list)
				#recursive_list.remove("list")

		#if (re.search(r"\s*target\s*",iter_needylist_keys,re.IGNORECASE)):
                #        last_underscore=iter_needylist_keys.rfind('_')
                #        actual_range=iter_needylist_keys[last_underscore+2:]
                #        tmp_list=mixrange(actual_range)
		#	print "\nin where is list target match\n"
		#	print "\n iter needylist key=="+iter_needylist_keys+"\n"
		#	pprint(tmp_list)
		#	print "\nin where is list target match end\n"
		#	if(isinstance(data[iter_needylist_keys],list)):
		#		print "\ncalling recursive_modifier from inside where_is_list"
		#		recursive_modifier(data,each_need,iter_needylist_keys,command_list1,tmp_list)
		#	else:
		#		if(len(recursive_list)>=1):
		#			print "\nrecursive call to where_is_list\n"
		#			where_is_list(data[iter_needylist_keys],recursive_list,each_need,command_list1,tmp_list)
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
                file="R"+str(Targets[(NoOfTargets-1)])+"_config"
                if(Targets[(NoOfTargets-1)] in total_targets):
			text_file = open(file, "a")
		else:
			total_targets.append(Targets[(NoOfTargets-1)])
			text_file = open(file, "w")
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

def recursive_modifier(data,each_need,needylist_key,command_list1,targets):
	static_cmd_dict={}
	tmp_str=command_list1[0]
	command_list1=[]
	cmt_cnt=0
	print "\n inside "+each_need+"tag\n"
	print "\n needylist keys start\n"
	pprint(needylist_key)
	print "\n needylist keys end \n"
	if(isinstance(data[needylist_key],list)):
		needylist_key_len=len(data[needylist_key])
		for each_and_every_cmd in range(needylist_key_len):
			if(isinstance(data[needylist_key][each_and_every_cmd],dict)):
				each_and_every_cmd_keys=data[needylist_key][each_and_every_cmd].keys()
				for iterate_keys in each_and_every_cmd_keys:
					if(re.search(r'.*mod_(\w)',iterate_keys)):
						matchobj= re.search(r'.*mod_(\w)',iterate_keys)
						static_cmd_dict[matchobj.group(1)]=each_and_every_cmd
			else:
				print "first for loop all static commands no modifier \n\n"
		print "\n static_cmd_dict start \n"
		pprint(static_cmd_dict)
		print "\n static_cmd_dict end \n"	
		for each_and_every_cmd in range(needylist_key_len):
			command_list1.append(tmp_str)
			if(isinstance(data[needylist_key][each_and_every_cmd],dict)):
				print "\n it's a dictionary \n"
                                each_and_every_cmd_keys=data[needylist_key][each_and_every_cmd].keys()
                                for iterate_keys in each_and_every_cmd_keys:
                                        if not(re.search(r'.*mod_(\w)',iterate_keys)):
						raw_command=iterate_keys
						print "\nraw_command===="+raw_command+"\n"
						raw_command_list=raw_command.split(' ')
						print "\n raw_command_list start\n"
						pprint(raw_command_list)
						print "\n raw_command_list end\n"
						for i in range(len(raw_command_list)):
							if(re.search(r'.*\$(\w)',raw_command_list[i])):
								print "matched a number \n\n=="+str(i)+"\n\n"
								print "\n raw_command_list of i =="+raw_command_list[i]+"\n"
								p=re.compile(r'\$\w')
								mod_num_list=p.findall(raw_command_list[i])
								print "\nmod_num_list start\n"
								pprint(mod_num_list)
								print "\nmod_num_list end\n"
								for each_mod_num_list in mod_num_list:
									matchobj=re.search(r'.*\$(\w)',each_mod_num_list)
									
								#matchobj=re.search(r'.*\$(\w)',raw_command_list[i])
									num=matchobj.group(1)
									print "\ninside mod_num_list for loop matchobj.group"+num+"\n"
									modifier_data={}
									modifier_keys=[]
									if(isinstance(data[needylist_key][each_and_every_cmd][iterate_keys],dict)):
										print "\nin data[needylist_key][each_and_every_cmd][iterate_keys]== dict\n"	
										if(data[needylist_key][each_and_every_cmd][iterate_keys] is not None):
											inside_modifier_keys=data[needylist_key][each_and_every_cmd][iterate_keys].keys()
										if('mod_'+str(num) in inside_modifier_keys):
											modifier_data=data[needylist_key][each_and_every_cmd][iterate_keys]['mod_'+str(num)]
											modifier_keys=modifier_data.keys()
										elif(str(num) in static_cmd_dict.keys()):
											modifier_data=data[needylist_key][int(static_cmd_dict[num])]['mod_'+str(num)]
											modifier_keys=modifier_data.keys()
										else:
											print "modifier key "+num+" is missing in "+each_need +"tag aborting script\n\n"
											sys.exit(50)
									else:
										if(str(num) in static_cmd_dict.keys()):
											modifier_data=data[needylist_key][int(static_cmd_dict[num])]["mod_"+str(num)]
											modifier_keys=modifier_data.keys()
										else:
											print "modifier key "+num+" is missing in "+each_need +"tag aborting script\n    \n"
                                                                                        sys.exit(50)
									print "\nmodifier data start\n"
									pprint(modifier_data)
									print "\nmodifier data end\n"
									print "\nmodifier keys start\n"
									pprint(modifier_keys)
									print "\nmodifier keys end\n"
									print "reading modifier values\n\n"
										
									if ("START" in modifier_keys):
										if not  ("LINK" in modifier_keys):
											if not ("TYPE" in modifier_keys):
												print "call ipv4 or ipv6 next ip function mapping is one2one== \n\n"
												#raw_command_list[i]=re.sub(r'{{\$'+num+'}}.*$', "", raw_command_list[i])
												if (len(command_list1)==1):
                					        	        	                print "inside if not equal to count 1 \n\n"
                					        	        	                if("COUNT" in modifier_keys):
														command_list1=command_list1*(int(modifier_data["COUNT"]))
                					        	        	                else:
														print "as a first ip modifier key you must define a Count key aborting script \n"
														sys.exit(100)
													print "commmand_list1 len==="+str(len(command_list1))+"\n\n"

												command_track=0
												ip_addr=modifier_data["START"];
												ip_step='x'
												ip_count=0
												if "STEP" in modifier_keys:
													ip_step=modifier_data["STEP"];
												print "\nip_step=="+ip_step+"\n"
												if "COUNT" in modifier_keys:
													ip_count=int(modifier_data["COUNT"]);
												
												ip_addr_list=generate_ip(ip_addr,ip_step,len(command_list1))
												### another pattern for writing IP address ###
												#for address in ip_range(modifier_data["START"]):
												#	if(command_track==int(modifier_keys["COUNT"])):
												#		break
												#	print "generated address is=="+address+"\n\n"
												#	command_list1[command_track]=command_list1[command_track]+" "+raw_command_list[i] +address
												#	command_track=command_track+1
												for address in ip_addr_list:
													if(command_track==len(command_list1)):
														break
													print "generated address is=="+address+"\n\n"
													command_list1[command_track]=command_list1[command_track]+" "+ re.sub(r'{{\$'+num+'}}.*$', address, raw_command_list[i])
													command_track=command_track+1
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\ncommand list start\n"
												pprint(command_list1)
												print "\ncommand list end\n"
												
												### another pattern 							
											#else:
											#	print "mapping is  one2one== \n\n"
											#	start_index=int(modifier_data["START"])
											#	raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
											#	if (len(command_list1)!=int(modifier_data["COUNT"])):
											#		print "inside if not equal to count 1 \n\n"
											#		command_list1=command_list1*(int(modifier_data["COUNT"]))
											#		print "commmand_list1 len==="+str(len(command_list1))+"\n\n"
											#	for each_command in range(len(command_list1)):
											#		command_list1[each_command]=command_list1[each_command]+" "+raw_command_list[i]+str(start_index)
											#		start_index=start_index+1
											#	print "after one2one operation \n\n"
											#	pprint(command_list1)
											###one2one is ended here##
										else:
											if not ("TYPE" in modifier_keys):
												print "call one2many ipv4 or ipv6 next ip function mapping is one2many== \n\n"
												if not ("COUNT" in modifier_keys):
													print "in one2many link relation count must defined aborting script \n\n"
													sys.exit(150)
												initial_len=len(command_list1)
                					        		        	command_tracker=0
                					        		        	command_list1=command_list1*int(modifier_data["COUNT"])
												list_tracker=0
												ip_addr_list=generate_ip(ip_addr,ip_step,len(command_list1))
												for address in ip_addr_list:
													if(command_tracker==int(modifier_data["COUNT"])):
                					        		        	                break
                					        		        	        print "generated address is=="+address+"\n\n"
													for ukl in range(list_tracker,list_tracker+initial_len):
														command_list1[ukl]=command_list1[ukl]+" "+re.sub(r'{{\$'+num+'}}.*$', address, raw_command_list[i])
													list_tracker=list_tracker+initial_len
													command_tracker=command_tracker+1
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\ncommand list start\n"
												pprint(command_list1)
												print "\ncommand list end\n"
		
                					        		                	
                					        		                print "after one2many operation \n\n"
                					        		                pprint(command_list1)
																			
									elif("VALUE" in modifier_keys):
										if not ("MODE" in modifier_keys):
											ranges=modifier_data["VALUE"]
                                                                                        last_underscore=ranges.rfind('_')
                                                                                        actual_range=''
                                                                                        if not(last_underscore==-1):
                                                                                                actual_range=ranges[last_underscore+1:]
                                                                                                ranges_list=mixrange(actual_range)
                                                                                                for each_range_item in range(len(ranges_list)):
                                                                                                        ranges_list[each_range_item]=ranges[:last_underscore]+str(ranges_list[each_range_item])      
                                                                                        
                                                                                        else:
                                                                                                actual_range=ranges
                                                                                                ranges_list=mixrange(actual_range)

											print "\nranges list start\n"
											pprint(ranges_list)	
											print "\nranges list end\n"	
											if not("LINK" in modifier_keys):
												#raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
												#if(modifier_data['MAPPING']=='one2one'):
												print "\n inside one2one link relation\n"
                					        		                if(len(ranges_list)!=len(command_list1)):
                					        		                        command_list1=command_list1*len(ranges_list)
                					        		                for each_command in range(len(command_list1)):
                					        		                        #command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[each_command]
													command_list1[each_command]=command_list1[each_command]+ re.sub(r'{{\$'+num+'}}.*$', ranges_list[each_command], raw_command_list[i])
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\n command list start\n"
												pprint(command_list1)
												print "\n command list end\n"	
											else:
												print "\n inside one2many link relation\n"
                					        		                initial_len=len(command_list1)
                					        		                command_tracker=0
                					        		                real_index=0
                					        		                add_num=initial_len
                					        		                command_list1=command_list1*len(ranges_list)
                					        		                for each_command in range(len(command_list1)):
                					        		                        #command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[real_index]
                					        		                        command_list1[each_command]=command_list1[each_command]+ re. sub(r'{{\$'+num+'}}.*$', ranges_list[each_command], raw_command_list[i])
                					        		                        command_tracker=command_tracker+1
                					        		                        if(command_tracker==initial_len):
                					        		                                real_index=real_index+1
                					        		                                initial_len=initial_len+add_num
                					        		                                #start_index=start_index+1
                					        		                                #command_tracker=command_tracker+1
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\n command list start\n" 
                                                                                                pprint(command_list1)
                                                                                                print "\n command list end\n"

										
										else:
											ranges=modifier_data["VALUE"]
                                                                                        last_underscore=ranges.rfind('_')
                                                                                        actual_range=''
                                                                                        if not(last_underscore==-1):
                                                                                                actual_range=ranges[last_underscore+1:]
                                                                                                ranges_list=mixrange(actual_range)
                                                                                                for each_range_item in range(len(ranges_list)):
                                                                                                        ranges_list[each_range_item]=ranges[:last_underscore]+str(ranges_list[each_range_item]) 
                                                                                        
                                                                                        else:
                                                                                                actual_range=ranges
                                                                                                ranges_list=mixrange(actual_range)
											print "\nranges start\n"
											pprint(ranges_list)
											print "\nranges end\n"
											if not ("LINK" in modifier_keys):
												print "\ninside one2one link relation\n"
												#raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
												#if(modifier_data['MAPPING']=='one2one'):
												if(len(ranges_list)!=len(command_list1)):
													command_list1=command_list1*len(ranges_list)
												for each_command in range(len(command_list1)):
													#command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[each_command]
													command_list1[each_command]=command_list1[each_command]+re.  sub(r'{{\$'+num+'}}.*$', ranges_list[each_command], raw_command_list[i])
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\n command list start\n" 
                                                                                                pprint(command_list1)
                                                                                                print "\n command list end\n"

											else:
												print "\ninside one2many link relation\n"
												initial_len=len(command_list1)
												command_tracker=0
												real_index=0
												add_num=initial_len
												command_list1=command_list1*len(ranges_list)
												for each_command in range(len(command_list1)):
                					        		                	#command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[real_index]
                					        		                	command_list1[each_command]=command_list1[each_command]+re.  sub(r'{{\$'+num+'}}.*$', ranges_list[each_command], raw_command_list[i])
                					        		                	command_tracker=command_tracker+1
                					        		                	if(command_tracker==initial_len):
                					        		                        	real_index=real_index+1
														initial_len=initial_len+add_num
														#start_index=start_index+1
                					        		                        	#command_tracker=command_tracker+1
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\n command list start\n" 
                                                                                                pprint(command_list1)
                                                                                                print "\n command list end\n"

							else:
								#command_list1=[raw_command_list[i]+"  ".format(i) for pk in command_list1]
								for pq in range(len(command_list1)):
									command_list1[pq]=command_list1[pq]+" "+raw_command_list[i]+" "	
								print "in fffffff not match else\n"
								pprint(command_list1)
						#target_array=targets.split(",")
						for each_file in targets:
						      	 if(each_file in total_targets):
        					        	 with open("R"+str(each_file)+"_config", 'a') as outfile: 
        					        	 	for each_comm in command_list1:
										outfile.write(each_comm+"\n")

							 else:
        					                 total_targets.append(each_file)
        					        	 with open("R"+str(each_file)+"_config", 'w') as outfile: 
								 	for each_comm in command_list1:
										outfile.write(each_comm+"\n")
        					command_list1=[]                                        	

						
			else:
						print "not a dictionary\n"
						raw_command=data[needylist_key][each_and_every_cmd]
						print "\nraw_command=="+raw_command+"\n"
						raw_command_list=raw_command.split(' ')
						for i in xrange(len(raw_command_list)):
							if(re.search(r'.*\$(\w)',raw_command_list[i])):
								print "matched a number \n\n=="+str(i)+"\n\n"
								p=re.compile(r'\$\w')
								mod_num_list=p.findall(raw_command_list[i])
								print "\n mod_num_list start \n"
								pprint(mod_num_list)
								print "\n mod_num_list end \n"
								for each_mod_num_list in mod_num_list:
									matchobj=re.search(r'.*\$(\w)',each_mod_num_list)
									
								#matchobj=re.search(r'.*\$(\w)',raw_command_list[i])
									num=matchobj.group(1)
									print "\ninside each_mod_num_list for loop match object"+matchobj.group(1)+"\n"
									modifier_data={}
									modifier_keys=[]
									if(str(num) in static_cmd_dict.keys()):
										modifier_data=data[needylist_key][int(static_cmd_dict[num])]["mod_"+num]
										modifier_keys=modifier_data.keys()
									else:
										print "modifier key "+num+" is missing in "+each_need +"tag aborting script\n\n"
										sys.exit(50)
									print "\n modifier_data start\n"
									pprint(modifier_data)
									print "\n modifier_data end\n"
									print "\n modifier_keys start\n"
									pprint(modifier_keys)
									print "\n modifier_keys end\n"
									print "reading modifier values\n\n"	
									if ("START" in modifier_keys):
										if not  ("LINK" in modifier_keys):
											if not ("TYPE" in modifier_keys):
												print "\n call start in else one2one ipv4 or ipv6 next ip function mapping is one2one== \n\n"
												#raw_command_list[i]=re.sub(r'{{\$'+num+'}}.*$', "", raw_command_list[i])
												if (len(command_list1)==1):
                					        	        	                print "inside if not equal to count 1 \n\n"
                					        	        	                if("COUNT" in modifier_keys):
														command_list1=command_list1*(int(modifier_data["COUNT"]))
                					        	        	                else:
														print "as a first ip modifier key you must define a Count key aborting script \n"
														sys.exit(100)
													print "commmand_list1 len==="+str(len(command_list1))+"\n\n"

												command_track=0
												ip_addr=modifier_data["START"];
												ip_step='x'
												ip_count=0
												if "STEP" in modifier_keys:
													ip_step=modifier_data["STEP"];
												if "COUNT" in modifier_keys:
													ip_count=int(modifier_data["COUNT"]);
												ip_addr_list=generate_ip(ip_addr,ip_step,len(command_list1))
												### another pattern for writing IP address ###
												#for address in ip_range(modifier_data["START"]):
												#	if(command_track==int(modifier_keys["COUNT"])):
												#		break
												#	print "generated address is=="+address+"\n\n"
												#	command_list1[command_track]=command_list1[command_track]+" "+raw_command_list[i] +address
												#	command_track=command_track+1
												for address in ip_addr_list:
													if(command_track==int(modifier_keys["COUNT"])):
														break
													print "generated address is=="+address+"\n\n"
													command_list1[command_track]=command_list1[command_track]+" "+ re.sub(r'{{\$'+num+'}}.*$', address, raw_command_list[i])
													command_track=command_track+1
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\n command_list start\n"
												pprint(command_list1)
												print "\n command_list end\n"
												### another pattern 							
											#else:
											#	print "mapping is  one2one== \n\n"
											#	start_index=int(modifier_data["START"])
											#	raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
											#	if (len(command_list1)!=int(modifier_data["COUNT"])):
											#		print "inside if not equal to count 1 \n\n"
											#		command_list1=command_list1*(int(modifier_data["COUNT"]))
											#		print "commmand_list1 len==="+str(len(command_list1))+"\n\n"
											#	for each_command in range(len(command_list1)):
											#		command_list1[each_command]=command_list1[each_command]+" "+raw_command_list[i]+str(start_index)
											#		start_index=start_index+1
											#	print "after one2one operation \n\n"
											#	pprint(command_list1)
											###one2one is ended here##
										else:
											if not ("TYPE" in modifier_keys):
												print "call start in else one2many ipv4 or ipv6 next ip function mapping is one2many== \n\n"
												#raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
												if not ("COUNT" in modifier_keys):
													print "in one2many link relation count must defined aborting script \n\n"
													sys.exit(150)
												initial_len=len(command_list1)
                					        		        	command_tracker=0
                					        		        	command_list1=command_list1*int(modifier_data["COUNT"])
												list_tracker=0
												ip_addr_list=generate_ip(ip_addr,ip_step,len(command_list1))
												for address in ip_addr_list:
													if(command_tracker==int(modifier_data["COUNT"])):
                					        		        	                break
                					        		        	        print "generated address is=="+address+"\n\n"
													for ukl in range(list_tracker,list_tracker+initial_len):
														command_list1[ukl]=command_list1[ukl]+" "+re.sub(r'{{\$'+num+'}}.*$', address, raw_command_list[i])
													list_tracker=list_tracker+initial_len
													command_tracker=command_tracker+1
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
														
                					        		                	
                					        		                print "after one2many operation \n\n"
                					        		                pprint(command_list1)
											#else:
											#	
											#	start_index=int(modifier_data["START"])
											#	print "start index=="+str(start_index)+"\n\n"
											#	raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
											#	initial_len=len(command_list1)
											#	command_tracker=0
											#	command_list1=command_list1*int(modifier_data["COUNT"])
											#	for each_command in range(len(command_list1)):
											#		command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+str(start_index)
											#		command_tracker=command_tracker+1
											#		if(command_tracker==initial_len):
											#			start_index=start_index+1
											#			command_tracker=0
											#	print "after one2many operation \n\n"
                					        		        #        pprint(command_list1)
										##one2many has ended here##
								
									elif("VALUE" in modifier_keys):
										
										if not ("MODE" in modifier_keys):
											ranges=modifier_data["VALUE"]
											last_underscore=ranges.rfind('_')
											actual_range=''
											if not(last_underscore==-1):
												actual_range=ranges[last_underscore+1:]
												ranges_list=mixrange(actual_range)
												for each_range_item in range(len(ranges_list)):
													ranges_list[each_range_item]=ranges[:last_underscore]+str(ranges_list[each_range_item])

											else:
												actual_range=ranges
												ranges_list=mixrange(actual_range)
										
											pprint(ranges_list)
											print "\n ranges_list end \n"
											if not("LINK" in modifier_keys):
												print "\n inside value one2one expand mode \n"
												#raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
												#if(modifier_data['MAPPING']=='one2one'):
                					        		                if(len(ranges_list)!=len(command_list1)):
                					        		                        command_list1=command_list1*len(ranges_list)
                					        		                for each_command in range(len(command_list1)):
                					        		                        #command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[each_command]
													command_list1[each_command]=command_list1[each_command]+ re.sub(r'{{\$'+num+'}}.*$', ranges_list[each_command], raw_command_list[i])
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\ncommand_list1 start \n"
												pprint(command_list1)
												print "\ncommand_list1 end \n"
											else:
												print "\n inside value one2many expand mode \n"
												#raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
                					        		                initial_len=len(command_list1)
                					        		                command_tracker=0
                					        		                real_index=0
                					        		                add_num=initial_len
                					        		                command_list1=command_list1*len(ranges_list)
                					        		                for each_command in range(len(command_list1)):
                					        		                        #command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[real_index]
                					        		                        command_list1[each_command]=command_list1[each_command]+ re. sub(r'{{\$'+num+'}}.*$', str(ranges_list[each_command]), raw_command_list[i])
                					        		                        command_tracker=command_tracker+1
                					        		                        if(command_tracker==initial_len):
                					        		                                real_index=real_index+1
                					        		                                initial_len=initial_len+add_num
                					        		                                #start_index=start_index+1
                					        		                                #command_tracker=command_tracker+1
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\ncommand_list1 start \n"
                                                                                                pprint(command_list1)
                                                                                                print "\ncommand_list1 end \n"
										
										else:
											ranges=modifier_data["VALUE"]
                                                                                        last_underscore=ranges.rfind('_')
                                                                                        actual_range=''
                                                                                        if not(last_underscore==-1):
                                                                                                actual_range=ranges[last_underscore+1:]
                                                                                                ranges_list=mixrange(actual_range)
                                                                                                for each_range_item in range(len(ranges_list)):
                                                                                                        ranges_list[each_range_item]=ranges[:last_underscore]+str(ranges_list[each_range_item])
                                                                                        
                                                                                        else:
                                                                                                actual_range=ranges
                                                                                                ranges_list=mixrange(actual_range)

											print "\nranges_list start\n"
											pprint(ranges_list)
											print "\nranges_list end\n"
											if not ("LINK" in modifier_keys):
												print "\n inside value one2one list mode \n"
												#raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
												#raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
												#if(modifier_data['MAPPING']=='one2one'):
												if(len(ranges_list)!=len(command_list1)):
													command_list1=command_list1*len(ranges_list)
												for each_command in range(len(command_list1)):
													#command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[each_command]
													command_list1[each_command]=command_list1[each_command]+re.  sub(r'{{\$'+num+'}}.*$', ranges_list[each_command], raw_command_list[i])
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])

												print "\ncommand_list1 start \n"
                                                                                                pprint(command_list1)
                                                                                                print "\ncommand_list1 end \n"
											else:
												print "\n inside value one2many list mode \n"
												initial_len=len(command_list1)
												command_tracker=0
												real_index=0
												add_num=initial_len
												command_list1=command_list1*len(ranges_list)
												for each_command in range(len(command_list1)):
                					        		                	#command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[real_index]
                					        		                	command_list1[each_command]=command_list1[each_command]+re.  sub(r'{{\$'+num+'}}.*$', ranges_list[each_command], raw_command_list[i])
                					        		                	command_tracker=command_tracker+1
                					        		                	if(command_tracker==initial_len):
                					        		                        	real_index=real_index+1
														initial_len=initial_len+add_num
														#start_index=start_index+1
                					        		                        	#command_tracker=command_tracker+1
												raw_command_list[i]=re.sub(r'{{\$'+num+'}}', "", raw_command_list[i])
												print "\ncommand_list1 start \n"
                                                                                                pprint(command_list1)
                                                                                                print "\ncommand_list1 end \n"
							else:
								#command_list1=[raw_command_list[i]+"  ".format(i) for pk in command_list1]
								for pq in range(len(command_list1)):
									command_list1[pq]=command_list1[pq]+" "+raw_command_list[i]+" "	
								print "\nin not match word else\n"
								pprint(command_list1)
								print "\nin not match work else end\n"	
						#target_array=targets.split(",")
						for each_file in targets:
						      	 if(each_file in total_targets):
        					        	 with open("R"+str(each_file)+"_config", 'a') as outfile: 
        					        	 	for each_comm in command_list1:
										outfile.write(each_comm+"\n")

							 else:
        					                 total_targets.append(each_file)
        					        	 with open("R"+str(each_file)+"_config", 'w') as outfile: 
								 	for each_comm in command_list1:
										outfile.write(each_comm+"\n")
        					command_list1=[]                                        	
						
	static_cmd_dict={}		
	##cp_command_list1=command_list1*1
	#print "inside recursive modifiier whether_or_not == \n\n"
	##print "command_list1\n\n"
	#print "first command list1 \n\n"
	##pprint(command_list1)
	#command_list1=[]
	#command_list1.append(tmp_str)
	##if whether_or_not==1:
	##	target_list=data["TARGETS"].split(",")
	#if(needylist_key=="list"):
	#	print "if list \n\n"
	#else:
	#	raw_command=needylist_key
	#raw_command_list=raw_command.split(' ')
	#num=1
	#print "first raw command list"
	#pprint(raw_command_list)
	##print "data[$1]=="+"\n\n"
	##print data['$'+str(num)]
	##sys.exit(5)
	#for i in xrange(len(raw_command_list)):
	#	if(re.search(r'.*\$(\w)',raw_command_list[i])):
	#		print "matched a number \n\n=="+str(i)+"\n\n"
	#		p=re.compile(r'\$\w')
	#		mod_num_list=p.findall(raw_command_list[i])
	#		for each_mod_num_list in mod_num_list:
	#			matchobj=re.search(r'.*\$(\w)',each_mod_num_list)
	#			
	#		#matchobj=re.search(r'.*\$(\w)',raw_command_list[i])
	#		num=matchobj.group(1)
	#		modifier_data=data['mod_'+str(num)]
	#		modifier_keys=modifier_data.keys()
	#		if ("START" in modifier_keys):
	#			if not  ("MAPPING" in modifier_keys):
	#				if not ("TYPE" in modifier_keys):
	#					print "call ipv4 or ipv6 next ip function mapping is one2one== \n\n"
	#					raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
	#					if (len(command_list1)==1):
        #                        	                print "inside if not equal to count 1 \n\n"
        #                        	                command_list1=command_list1*(int(modifier_data["COUNT"]))
        #                        	                print "commmand_list1 len==="+str(len(command_list1))+"\n\n"

	#					if(modifier_data["TYPE"]=="IPV4"):
	#						command_track=0
	#						ip_addr=modifier_data["START"];
	#						ip_step='x'
	#						ip_count=0
	#						if "STEP" in modifier_keys:
	#							ip_step=modifier_data["STEP"];
	#						if "COUNT" in modifier_keys:
	#							ip_count=int(modifier_data["COUNT"]);
	#						generate_ip(ip_addr,ip_step,ip_count)
	#						### another pattern for writing IP address ###
	#						for address in ip_range(modifier_data["START"]):
	#							if(command_track==int(modifier_keys["COUNT"])):
	#								break
	#							print "generated address is=="+address+"\n\n"
	#							command_list1[command_track]=command_list1[command_track]+" "+raw_command_list[i] +address
	#							command_track=command_track+1
	#						### another pattern 							
	#				else:
	#					print "mapping is  one2one== \n\n"
	#					start_index=int(modifier_data["START"])
	#					raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
	#					if (len(command_list1)!=int(modifier_data["COUNT"])):
	#						print "inside if not equal to count 1 \n\n"
	#						command_list1=command_list1*(int(modifier_data["COUNT"]))
	#						print "commmand_list1 len==="+str(len(command_list1))+"\n\n"
	#					for each_command in range(len(command_list1)):
	#						command_list1[each_command]=command_list1[each_command]+" "+raw_command_list[i]+str(start_index)
	#						start_index=start_index+1
	#					print "after one2one operation \n\n"
	#					pprint(command_list1)
	#				##one2one is ended here##
	#			else:
	#				if "TYPE" in modifier_keys:
	#					if(modifier_data["TYPE"]=="IPV4"):
	#						print "call ipv4 or ipv6 next ip function mapping is one2many== \n\n"
	#						raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
	#						initial_len=len(command_list1)
        #                	                	command_tracker=0
        #                	                	command_list1=command_list1*int(modifier_data["COUNT"])
	#						list_tracker=0
	#						for address in ip_range(modifier_data["START"]):
	#							if(command_tracker==int(modifier_data["COUNT"])):
        #                	                                        break
        #                	                                print "generated address is=="+address+"\n\n"
	#							for ukl in range(list_tracker,list_tracker+initial_len):
	#								command_list1[ukl]=command_list1[ukl]+" "+raw_command_list[i] +address
	#							list_tracker=list_tracker+initial_len
	#							command_tracker=command_tracker+1
	#							
        #                	                	
        #                	                print "after one2many operation \n\n"
        #                	                pprint(command_list1)
	#				else:
	#					
	#					start_index=int(modifier_data["START"])
	#					print "start index=="+str(start_index)+"\n\n"
	#					raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
	#					initial_len=len(command_list1)
	#					command_tracker=0
	#					command_list1=command_list1*int(modifier_data["COUNT"])
	#					for each_command in range(len(command_list1)):
	#						command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+str(start_index)
	#						command_tracker=command_tracker+1
	#						if(command_tracker==initial_len):
	#							start_index=start_index+1
	#							command_tracker=0
	#					print "after one2many operation \n\n"
        #                	                pprint(command_list1)
	#			##one2many has ended here##
	#		else:
	#			if("MODE" in modifier_keys):
	#				mode_type=modifier_data['MODE']
	#				if(mode_type=="LIST"):
	#					ranges=modifier_data["sub_range"]
	#					ranges_list=ranges.split(',')
	#					if ("MAPPING" in modifier_keys):
	#						raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
	#						if(modifier_data['MAPPING']=='one2one'):
	#							if(len(ranges_list)!=len(command_list1)):
	#								command_list1=command_list1*len(ranges_list)
	#							for each_command in range(len(command_list1)):
	#								command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[each_command]
	#						else:
	#							initial_len=len(command_list1)
	#							command_tracker=0
	#							real_index=0
	#							add_num=initial_len
	#							command_list1=command_list1*len(ranges_list)
	#							for each_command in range(len(command_list1)):
        #                                                        	command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[real_index]
        #                                                        	command_tracker=command_tracker+1
        #                                                        	if(command_tracker==initial_len):
        #                                                                	real_index=real_index+1
	#									initial_len=initial_len+add_num
	#									#start_index=start_index+1
        #                                                                	#command_tracker=command_tracker+1
	#							
	#					else:
	#						print "please specify the mapping in your yaml file script aborting \n\n"
        #                                 		sys.exit(4)

	#					
	#				elif(mode_type=="EXPAND"):
	#					ranges=modifier_data["sub_range"]
        #                                        ranges_list=mixrange(ranges)
	#					if("MAPPING" in modifier_keys):
	#						raw_command_list[i]=re.sub(r'\$.*$', "", raw_command_list[i])
	#						if(modifier_data['MAPPING']=='one2one'):
        #                                                        if(len(ranges_list)!=len(command_list1)):
        #                                                                command_list1=command_list1*len(ranges_list)
        #                                                        for each_command in range(len(command_list1)):
        #                                                                command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[each_command]
	#						else:
        #                                                        initial_len=len(command_list1)
        #                                                        command_tracker=0
        #                                                        real_index=0
        #                                                        add_num=initial_len
        #                                                        command_list1=command_list1*len(ranges_list)
        #                                                        for each_command in range(len(command_list1)):
        #                                                                command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[real_index]
        #                                                                command_tracker=command_tracker+1
        #                                                                if(command_tracker==initial_len):
        #                                                                        real_index=real_index+1
        #                                                                        initial_len=initial_len+add_num
        #                                                                        #start_index=start_index+1
        #                                                                        #command_tracker=command_tracker+1

	#					else:
	#						print "please specify the mapping in your yaml file script aborting \n\n"
        #                                                sys.exit(8)
	#					
	#					
	#			else:
	#				print "please specify the mode list or expand in your yaml file script aborting \n\n"
	#				sys.exit(2)
	#	else:
	#		#command_list1=[raw_command_list[i]+"  ".format(i) for pk in command_list1]
	#		for pq in range(len(command_list1)):
	#			command_list1[pq]=command_list1[pq]+" "+raw_command_list[i]+" "	
	#			
	#print "\n\n "+raw_command+"\n\n"
					

	
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
	#filepath = "./example/ipclose.yaml"
	filepath = sys.argv[1]
	
	data = yaml_reader(filepath)
	#x = data['VLAN_POOL1']['VLAN_POOL_IPV4']['RANGE']
	#config_vlan(x)
