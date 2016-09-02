import yaml
import os
import json
from #p#print import pprint
import sys
import re
import itertools
from netaddr import *
from collections import defaultdict
import six
#from termcolor import colored
#from .general_class_for_handle import Handles
router_group_dict=defaultdict(list)
total_targets=[]
dict1={}
log_location_path="" 
import time
import datetime
import os
def getname(tmp_str):
    #print("\nin getname function j\n")
    ifpart=re.search(r'_IF.*?\_',tmp_str).group(0)
    lookup_list=tmp_str.split(ifpart)
    #p#print(dict1)
    if(re.search(r'name',ifpart,re.I)):
        return dict1['resources'][lookup_list[0]]["interfaces"][lookup_list[1]]['name']
    elif(re.search(r'pic',ifpart,re.I)):
        return dict1['resources'][lookup_list[0]]["interfaces"][lookup_list[1]]['pic']
    elif(re.search(r'link',ifpart,re.I)):
        return dict1['resources'][lookup_list[0]]["interfaces"][lookup_list[1]]['link']
    else:
        return dict1['resources'][lookup_list[0]]["interfaces"][lookup_list[1]]['name']

def initialize_config_engine(handle=None,log_location=None):
    global dict1
    if not(handle==None):
       dict1=handle
    global log_location_path
    if(log_location==None):
       log_location_path=os.popen("pwd").read()[:-1]
    else:
       log_location_path=log_location

def PAS_Config_Generator(str1,str2):
     command_list1=[]
     timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
     if(isinstance(str1,dict)):
         command_list1.append("set "+str2)
         command_list1=concate_hash(command_list1,str1,"")
         file_list="english"
         groups_list=[]
         for each_comm in command_list1:
                            if(re.search(r'.*group.*',each_comm)):
                                    command_splitted=each_comm.split(" ")
                                    if not(command_splitted[2] in groups_list):
                                          groups_list.append(command_splitted[2].strip())
         with open(log_location_path+"/"+file_list+"_"+timestamp+"_config.set",'w') as outfile:
                            for each_comm in command_list1:
                                   outfile.write(re.sub(' +',' ',each_comm)+"\n")
         with open(log_location_path+"/"+file_list+"_"+timestamp+"_config.set",'a') as outfile:
                            for each_comm in groups_list:
                                   outfile.write("\nset apply-groups "+each_comm+"\n")
         return file_list+"_"+timestamp+"_config.set"

     tmp_list1=str1.split("and")
     command_list1=command_list1*(len(tmp_list1))
     
     for each_tmp_list1 in tmp_list1:
         old_size=0
         new_size=0
         tmp_str1=each_tmp_list1.strip()
         tmp_list2=tmp_str1.split("as")

         #print("tmp_list2 start")
         #p#print(tmp_list2)
         #print("tmp_list2 end")
         for each_tmp_list2 in tmp_list2:
             expanded_list=mix_range_with_letters(each_tmp_list2.strip())
             #print("expanded_list start")
             #p#print(expanded_list)
             #print("expanded_list end")
             if(old_size==0 and new_size==0):
                    old_size=len(command_list1)
                    command_list1.append("set "+str2+" "+expanded_list[0])
                    new_size=len(command_list1)
                    #print("old_size=="+str(old_size)+"\n"+"new_size=="+str(new_size)+"\n")
                    #print("0 0")
                    #p#print(command_list1)
             else:
                    #print("old_size=="+str(old_size)+"\n"+"new_size=="+str(new_size)+"\n")
                    for each_item in range(old_size,new_size):
                        command_list1[each_item]=command_list1[each_item]+" "+expanded_list[0]
                    #print("not 0 0")
                    #p#print(command_list1)
             #print("")
             if(len(expanded_list)>1):
                for each_item in range(1,len(expanded_list)):
                    if((new_size-old_size)==1):
                          command_list1.append("set "+str2+" "+expanded_list[each_item])
                    else:
                          for each_list_item in range(old_size,new_size):
                              command_list1[each_list_item]=command_list1[each_list_item]+" "+expanded_list[each_list_item]

                new_size=len(command_list1)
     #p#print(command_list1)

 
    # #p#print(command_list1)               
             
     file_list="english"
     groups_list=[]
     for each_comm in command_list1:
                        if(re.search(r'.*group.*',each_comm)):
                                command_splitted=each_comm.split(" ")
                                if not(command_splitted[2] in groups_list):
                                      groups_list.append(command_splitted[2].strip())
     with open(log_location_path+"/"+file_list+"_"+timestamp+"_config.set",'w') as outfile:
                        for each_comm in command_list1:
                               outfile.write(re.sub(' +',' ',each_comm)+"\n")
     with open(log_location_path+"/"+file_list+"_"+timestamp+"_config.set",'a') as outfile:
                        for each_comm in groups_list:
                               outfile.write("\nset apply-groups "+each_comm+"\n")
     return file_list+"_"+timestamp+"_config.set"    

def concate_hash(command_list,hash_to_expand,path):
    if(isinstance(hash_to_expand,dict)):
       hash_keys=hash_to_expand.keys()
       for each_hash_key in hash_keys:
           if(isinstance(hash_to_expand[each_hash_key],dict)):
              #path=path+" "+each_hash_key
              concate_hash(command_list,hash_to_expand[each_hash_key],path+" "+each_hash_key)
           elif(isinstance(hash_to_expand[each_hash_key],list)):
              tmp_list=hash_to_expand[each_hash_key]
              for each_item in tmp_list:
                  command_list.append((path+" "+ str(each_hash_key) + " " + str(each_item)).strip() )
           else:
              command_list.append((path+" "+str(each_hash_key)+" "+str(hash_to_expand[each_hash_key])).strip())
    return command_list
   
def PAS_Delete_Generator(str1,str2):
     command_list1=[]
     timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
     if(isinstance(str1,dict)):
         command_list1.append("delete "+str2)
         command_list1=concate_hash(command_list1,str1,"")
         file_list="english"
         groups_list=[]
         for each_comm in command_list1:
                            if(re.search(r'.*group.*',each_comm)):
                                    command_splitted=each_comm.split(" ")
                                    if not(command_splitted[2] in groups_list):
                                          groups_list.append(command_splitted[2].strip())
         with open(log_location_path+"/"+file_list+"_"+timestamp+"_config.set",'w') as outfile:
                            for each_comm in command_list1:
                                   outfile.write(re.sub(' +',' ',each_comm)+"\n")
         #with open(file_list,'a') as outfile:
         #                   for each_comm in groups_list:
         #                          outfile.write("\nset apply-groups "+each_comm+"\n")
         return file_list+"_"+timestamp+"_config.set"



     tmp_list1=str1.split("and")
     command_list1=command_list1*(len(tmp_list1))
     #print("tmp_list1 start")
     #p#print(tmp_list1)
     #print("tmp_list1 end")
     for each_tmp_list1 in tmp_list1:
         old_size=0
         new_size=0
         tmp_str1=each_tmp_list1.strip()
         tmp_list2=tmp_str1.split("as")

         #print("tmp_list2 start")
         #p#print(tmp_list2)
         #print("tmp_list2 end")
         for each_tmp_list2 in tmp_list2:
             expanded_list=mix_range_with_letters(each_tmp_list2.strip())
             #print("expanded_list start")
             #p#print(expanded_list)
             #print("expanded_list end")
             if(old_size==0 and new_size==0):
                    old_size=len(command_list1)
                    command_list1.append("delete "+str2+" "+expanded_list[0])
                    new_size=len(command_list1)
                    #print("old_size=="+str(old_size)+"\n"+"new_size=="+str(new_size)+"\n")
                    #print("0 0")
                    #p#print(command_list1)
             else:
                    #print("old_size=="+str(old_size)+"\n"+"new_size=="+str(new_size)+"\n")
                    for each_item in range(old_size,new_size):
                        command_list1[each_item]=command_list1[each_item]+" "+expanded_list[0]
                    #print("not 0 0")
                    #p#print(command_list1)
             #print("")
             if(len(expanded_list)>1):
                for each_item in range(1,len(expanded_list)):
                    if((new_size-old_size)==1):
                          command_list1.append("delete "+str2+" "+expanded_list[each_item])
                    else:
                          for each_list_item in range(old_size,new_size):
                              command_list1[each_list_item]=command_list1[each_list_item]+" "+expanded_list[each_list_item]
                              
                new_size=len(command_list1)   
     #p#print(command_list1)
     
     file_list="english"
     with open(log_location_path+"/"+file_list+"_"+timestamp+"_config.set",'w') as outfile:
                        for each_comm in command_list1:
                               outfile.write(re.sub(' +',' ',each_comm)+"\n")
     return file_list+"_"+timestamp+"_config.set"

def generate_ip(ip_addr,ip_step,ip_count):
        ip_addr_list=[]
        ip_addr_list.append(ip_addr)
        prefix=0
        network_host=ip_addr.split('/')
        if(ip_step=='x'):
                if(len(network_host)==1):
                        #print("You haven't define step either mask aborting scipt\n\n")
                        sys.exit(1)
                else:
                        network_host[0]=network_host[0]+"/0"
                        ip = IPNetwork(ip_addr)
                        count=1
                        while(count<ip_count):
                                ip_addr_list.append(str(ip.ip+count*(ip.size))+"/"+str(network_host[1]))
                                count=count+1
        if not(ip_step=='x'):
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

def yaml_reader(filepath):
    file = open(filepath,"r")
    data=yaml.load(file)
    #print("data keys\n\n")
    #p#print(data)
    #print("data keys now real\n\n")
    list1=list(data.keys()) 
    needylist=[]
    for each_list1 in list1:
        if (isinstance(data[each_list1],dict) or isinstance(data[each_list1],list)) :
                needylist.append(each_list1)
                        
    #p#print(list(data.keys()))
    #sys.exit(2)
    if 'PAS_CONFIGS' in needylist:
        needylist.remove('PAS_CONFIGS')
    if 'PAS_CONFIG_MAPS' in needylist:
        needylist.remove('PAS_CONFIG_MAPS')
    #print("needy list start \n")
    #p#print(needylist)
    #print("needy list end \n")
    static_cmd_dict={}
    if ("PAS_CONFIGS" in list1):
        pas_config_tags=list(data["PAS_CONFIGS"].keys())
        for each_pas_config_tag in pas_config_tags:
                command_set=data["PAS_CONFIGS"][each_pas_config_tag]
                if(isinstance(command_set,dict)):
                        #print("\ncommand set keys start\n")
                        #p#print(command_set)
                        if("GRPID" in list(command_set.keys())):
                                static_cmd_dict[each_pas_config_tag]="set groups "+command_set["GRPID"]
                                del command_set['GRPID']
                        else:
                                static_cmd_dict[each_pas_config_tag]="set groups "+each_pas_config_tag
                        tag_keys=list(command_set.keys())
                        for each_tag_key in tag_keys:
                                if isinstance(command_set[each_tag_key],list):
                                        #static_cmd_dict[each_pas_config_tag]=static_cmd_dict[each_pas_config_tag]+" "+each_tag_key
                                        if not(command_set[each_tag_key]=="LIST_HOLDER"):
                                        	static_cmd_dict[each_pas_config_tag]=static_cmd_dict[each_pas_config_tag]+" "+each_tag_key
                                        tmp_static_cmd_str=static_cmd_dict[each_pas_config_tag]
                                        static_cmd_dict[each_pas_config_tag]=static_cmd_dict[each_pas_config_tag]+" " + command_set[each_tag_key][0]+"\n"
                                        for command_set_itr in range(1,len(command_set[each_tag_key])):
                                                static_cmd_dict[each_pas_config_tag]=static_cmd_dict[each_pas_config_tag]+tmp_static_cmd_str+" " + command_set[each_tag_key][command_set_itr]+"\n"
        #print("before static cmd dict\n\n")
        #p#print(static_cmd_dict)
        #print("after static cmd dict\n\n")
        #print(colored("\nPAS_config tag successfully generated now writing to the file\n",'green'))
        if("PAS_CONFIG_MAPS" in list1):
                maps_device=data["PAS_CONFIG_MAPS"]
                map_list=list(maps_device.keys())
                tmp_list=[]
                for each_map_device in map_list:
                        tmp_list=mix_range_with_letters(each_map_device)

                        if(isinstance(maps_device[each_map_device],list)):
                                
                                for write_data in range(len(maps_device[each_map_device])) :
                                        static_cmd_dict_splitted=static_cmd_dict[maps_device[each_map_device][write_data]].split(" ")
                                        for every_device in tmp_list:
                                                append_or_not=0
                                                if(str(every_device) in list(router_group_dict.keys())):
                                                        list_of_tags=router_group_dict[str(every_device)]
                                                        for each_list_of_tags in list_of_tags:
                                                                if not(each_list_of_tags==static_cmd_dict_splitted[2]):
                                                                        append_or_not=1
                                                        if(append_or_not==1):
                                                                router_group_dict[str(every_device)].append(static_cmd_dict_splitted[2])
                                                                static_cmd_dict[maps_device[each_map_device][write_data]]=static_cmd_dict[maps_device[each_map_device][write_data]]+"\nset apply-groups "+ static_cmd_dict_splitted[2]
                                                else:
                                                        router_group_dict[str(every_device)].append(static_cmd_dict_splitted[2])
                                                        static_cmd_dict[maps_device[each_map_device][write_data]]=static_cmd_dict[maps_device[each_map_device][write_data]]+"\nset apply-groups "+ static_cmd_dict_splitted[2]
                                        PAS_STATIC_CMDS(static_cmd_dict[maps_device[each_map_device][write_data]],tmp_list,maps_device[each_map_device][write_data])
                                        targets_str=""
                                        for each_targets in tmp_list:
                                             targets_str=targets_str+str(each_targets)+","
                                        #print("\n"+maps_device[each_map_device][write_data]+" group successfully generated for "+targets_str+"  \n") 
                        else:
                                targets_str=""
                                map_devices_list=str(maps_device[each_map_device]).split(",")
                                for write_data in range(len(map_devices_list)) :
                                        static_cmd_dict_splitted=static_cmd_dict[map_devices_list[write_data]].split(" ")
                                        for every_device in tmp_list:
                                                append_or_not=0
                                                if(str(every_device) in list(router_group_dict.keys())):
                                                        list_of_tags=router_group_dict[str(every_device)]
                                                        for each_list_of_tags in list_of_tags:
                                                                if not(each_list_of_tags==static_cmd_dict_splitted[2]):
                                                                        append_or_not=1                                                                
                                                if(append_or_not==1):
                                                        router_group_dict[str(every_device)].append(static_cmd_dict_splitted[2])
                                                else:
                                                        router_group_dict[str(every_device)].append(static_cmd_dict_splitted[2])
                                        PAS_STATIC_CMDS(static_cmd_dict[map_devices_list[write_data]],tmp_list,map_devices_list[write_data])
                                        targets_str=""
                                        #print("tag name \n"+map_devices_list[write_data]+"\n")
                                        #print("targets_str=="+targets_str+"\n")
                                        for each_targets in tmp_list:
                                             targets_str=targets_str+str(each_targets)+","
                                        #print("targets_str middle=="+targets_str+"\n")
                                        #print("\n"+map_devices_list[write_data]+" group successfully generated for "+targets_str[:-1]+"  \n") 
                                        targets_str=""
                                        #print("at the end targets_str===")
                                        #print("targets_str=="+targets_str+"\n")
                        tmp_list=[]               
                                        
 
        else:
                #print("you have defined PAS_CONFIG KEY but forgot to create PAS_CONFIG_MAPS keys aborting script\n\n")                        
                sys.exit(23) 
    #print("\nrouter_group_dict start\n")
    #p#print(router_group_dict)
    #print("\nrouter gorup_dict end\n")
    for each_need in needylist:
        #print("\n inside main for loop start\n")
        command_list1=[]
        
        needylist_dict=data[each_need]
        needylist_keys=list(needylist_dict.keys())


        if "GRPID" in list(data[each_need].keys()):
                str_tmp="set groups "+data[each_need]["GRPID"]+" "
                needylist_keys.remove("GRPID")
        else:
                str_tmp="set groups "+each_need+" "
        command_list1.append(str_tmp)
        
        
        if ("TARGETS" in needylist_keys):
                tmp_list=mix_range_with_letters(data[each_need]["TARGETS"])
                for each_outer_needylist_keys in needylist_keys:
                        if not (re.search(r"\s*target\s*",each_outer_needylist_keys,re.IGNORECASE)):
                                recursive_modifier(data[each_need],each_need,each_outer_needylist_keys,command_list1,tmp_list)
                                needylist_keys.remove(each_outer_needylist_keys)        
                needylist_keys.remove("TARGETS")
        where_is_list(data[each_need],needylist_keys,each_need,command_list1)
        
    #print("\nrouter_group_dict start\n")
    #p#print(router_group_dict)
    #print("\nrouter gorup_dict end\n")
    group_list_to_append=list(router_group_dict.keys())
    for each_group_list_to_append in group_list_to_append:
        s=set(router_group_dict[each_group_list_to_append])
        for each_target in total_targets :
               if(re.search(each_group_list_to_append,each_target)):
                    with open(log_location_path+"/"+each_target+"_config.set", 'a') as outfile:
                        while s:
                              outfile.write("\nset apply-groups "+ s.pop()+" \n")
    targets_str=""
    if '' in group_list_to_append:
         group_list_to_append.remove('')
    for each_targets in group_list_to_append:
         targets_str=targets_str+str(each_targets)+","
    #print("\n file successfully generated are "+targets_str[:-1]+"  \n")
    return data
def where_is_list(data,needylist_keys,each_need,command_list1):
        #print("\ninside where_is_list \n")
        for iter_needylist_keys in needylist_keys:
                recursive_list=[]
                if(isinstance(data[iter_needylist_keys],dict)):
                        recursive_list=list(data[iter_needylist_keys].keys())
                        if ("LIST_HOLDER" in recursive_list):
                                recursive_modifier(data[iter_needylist_keys],each_need,"LIST_HOLDER",tmp_list)
                                recursive_list.remove("LIST_HOLDER")

                if (re.search(r"\s*target\s*",iter_needylist_keys,re.IGNORECASE)):
                        last_underscore=iter_needylist_keys.rfind('_')
                        actual_range=iter_needylist_keys[last_underscore+1:]
                        tmp_list=mix_range_with_letters(actual_range)

                        if(isinstance(data[iter_needylist_keys],list)):
                                #print("\ncalling recursive_modifier from inside where_is_list")
                                recursive_modifier(data,each_need,iter_needylist_keys,command_list1,tmp_list)
                        else:
                                if(len(recursive_list)>=1):
                                        #print("\nrecursive call to where_is_list\n")
                                        where_is_list(data[iter_needylist_keys],recursive_list,each_need,command_list1)
def PAS_STATIC_CMDS(Data,Targets,tag_name) :
        NoOfTargets=len(Targets)
        #print("\nin PAS_STATIC_CMDS start\n")
        #p#print(Data)
        #print("\nin PAS_STATIC_CMDS end\n")
        create_new_file=0
        while(NoOfTargets!=0) :
                for  each_target in total_targets  :
                       if(re.search(Targets[(NoOfTargets-1)],each_target)):
                             create_new_file=1
                             file=str(log_location_path+"/"+each_target+"_config.set")
                             text_file=open(file,"a")
                             text_file.write(Data)
                             text_file.close()
                               #for each_comm in command_list1:
                               #       #outfile.write(each_comm+"\n")
                               #       outfile.write(re.sub(' +',' ',each_comm)+"\n")
                if(create_new_file==0):
                        timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
                        total_targets.append(Targets[(NoOfTargets-1)]+"_"+timestamp)
                        file=str(log_location_path+"/"+Targets[(NoOfTargets-1)]+"_"+timestamp+"_config.set", 'a')
                        text_file = open(file, "w")
                        text_file.write(Data)
                        text_file.close()
                #text_file.write(Data)
                #text_file.close()
                #print(colored("\n"+tag_name+" successfully written to the"+"R"+str(Targets[(NoOfTargets-1)])+" file\n",'green')) 
                NoOfTargets-=1


def mixrange(s):
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l,h = list(map(int, i.split('-')))
            r+= list(range(l,h+1))
    return r

def mix_range_with_letters(ranges):
        token_range_list=ranges.split(",")
        #print("in mix_range_with_letters start")
        ranges_list=[]
        for each_token_range_list in token_range_list:
                m = re.search("\d+\-\d+", each_token_range_list)
                #print("match condition m\n\n")
                #p#print(m)
                if(m):
                     actual_range=m.group(0)
                     initial_range_len=len(ranges_list)
                     ranges_list=ranges_list+mixrange(actual_range)
                     for each_range_item in range(initial_range_len,len(ranges_list)):
                             ranges_list[each_range_item]=each_token_range_list[:m.start()]+str(ranges_list[each_range_item])+each_token_range_list[m.end():]
                else:
                     tmp_list=[]
                     tmp_list.append(each_token_range_list)
                     ranges_list=ranges_list+tmp_list
        #p#print(ranges_list)
        return ranges_list


def recursive_modifier(data,each_need,needylist_key,command_list1,targets):
        static_cmd_dict={}
        tmp_str=list(command_list1)
        #command_list1=[]
        cmt_cnt=0
        hash_key_list=[]
        hierarchical=0
        hash_value_list=[]
        went_in_to_generate_cmd=0
        is_target_specific_modifier=0
        target_modifier_dict={}
        target_specific_dict={}
        if(isinstance(data[needylist_key],list)):
                needylist_key_len=len(data[needylist_key])
                for each_and_every_cmd in range(needylist_key_len):
                        if(isinstance(data[needylist_key][each_and_every_cmd],dict)):
                                each_and_every_cmd_keys=list(data[needylist_key][each_and_every_cmd].keys())
                                for iterate_keys in each_and_every_cmd_keys:
                                        if(re.search(r'.*mod_(\w)',iterate_keys)):
                                                matchobj= re.search(r'.*mod_(\w+)',iterate_keys)
                                                static_cmd_dict[matchobj.group(1)]=each_and_every_cmd
                                                                                        
                #print("\n static_cmd_dict start \n")
                #p#print(static_cmd_dict)
                #print("\n static_cmd_dict end \n")        
                for each_and_every_cmd in range(needylist_key_len):
                        command_list1=list(tmp_str)
                        #print("\nchecking dictionary or list start\n\n")
                        #p#print(data[needylist_key][each_and_every_cmd])
                        #print("\nchecking dictionary or list end \n\n")
                        if(isinstance(data[needylist_key][each_and_every_cmd],dict)):
                                #print("\n it's a dictionary \n")
                                each_and_every_cmd_keys=list(data[needylist_key][each_and_every_cmd].keys())
                                for iterate_keys in each_and_every_cmd_keys:
                                        if not(re.search(r'.*mod_(\w)',iterate_keys) or re.search(r'.*mod_\((\w)',iterate_keys)):
                                                raw_command=iterate_keys
                                                #print("\nraw_command===="+raw_command+"\n")
                                                went_in_to_generate_cmd=1
                                                raw_command_list=raw_command.split(' ')
                                                #print("\n raw_command_list start\n")
                                                #p#print(raw_command_list)
                                                #print("\n raw_command_list end\n")
                                                inside_modifier_keys=[]
                                                for i in range(len(raw_command_list)):
                                                        if(re.search(r'.*{{(\w+)}}',raw_command_list[i])):
                                                                #print("matched a number \n\n=="+str(i)+"\n\n")
                                                                #print("\n raw_command_list of i =="+raw_command_list[i]+"\n")
                                                                p=re.compile(r'.*?{{(\w+)}}')
                                                                mod_num_list=p.findall(raw_command_list[i])
                                                                #print("\nmod_num_list start\n")
                                                                #p#print(mod_num_list)
                                                                #print("\nmod_num_list end\n")
                                                                mod_num_list_index=1
                                                                for each_mod_num_list in mod_num_list:
                                                                        matchobj=re.search(r'.*?(\w+)',each_mod_num_list)
                                                                        num=matchobj.group(1)
                                                                        #print("\ninside mod_num_list for loop matchobj.group"+num+"\n")
                                                                        modifier_data={}
                                                                        modifier_keys=[]
                                                                        if(isinstance(data[needylist_key][each_and_every_cmd][iterate_keys],dict)):
                                                                                #print("\nin data[needylist_key][each_and_every_cmd][iterate_keys]== dict\n")        
                                                                                if(data[needylist_key][each_and_every_cmd][iterate_keys] is not None):
                                                                                        inside_modifier_keys=list(data[needylist_key][each_and_every_cmd][iterate_keys].keys())
                                                                                hash_structure_exists=0
                                                                                for each_inside_modifier_keys in inside_modifier_keys:
                                                                                        #print("in for loop each_inside_modifier_keys hash structure checking")
                                                                                        ranges_list=[]
                                                                                        if(re.search(r'.*mod_\(.*'+num+'.*',each_inside_modifier_keys)):
                                                                                                
                                                                                                splitted_iterate_keys=each_inside_modifier_keys.split(',')
                                                                                                hash_struct_keys=list(data[needylist_key][each_and_every_cmd][iterate_keys][each_inside_modifier_keys].keys())
                                                                                                hash_key_list=[]
                                                                                                hash_value_list=[]
                                                                                                for each_hash_struct_keys in hash_struct_keys:
                                                                                                        hash_key_list.append(each_hash_struct_keys)
                                                                                                        hash_value_list.append(data[needylist_key][each_and_every_cmd][iterate_keys][each_inside_modifier_keys][each_hash_struct_keys])
                                                                                                #print("\nhash_key_list start\n")
                                                                                                #p#print(hash_key_list)
                                                                                                #print("\nhash_key_list end\n")
                                                                                                #print("\nhash_value_list start\n")
                                                                                                #p#print(hash_value_list)        
                                                                                                #print("\nhash_value_list end\n")
        
                                                                                                #print("in for loop each_inside_modifier_keys hash structure found checking")
                                                                                                splitted_each_inside_modifier_keys=each_inside_modifier_keys.split(',')
                                                                                                hash_structure_exists=1
                                                                                                #print("\nnum++==  "+num+"\n")
                                                                                                #print("\nsplitted_each_inside_modifier_keys++==  ")
                                                                                                #p#print(splitted_each_inside_modifier_keys)
                                                                                                if(splitted_each_inside_modifier_keys[0][5:]==num):
                                                                                                        hash_trace=0
                                                                                                        for each_hash_list in hash_key_list:
                                                                                                                hash_value_len=len(mix_range_with_letters(hash_value_list[hash_trace]))
                                                                                                                hash_trace=hash_trace+1
                                                                                                                for repeat_till in range(hash_value_len):
                                                                                                                        ranges_list.append(each_hash_list)
                                                                                                        #print("\ninside hash structure ranges_list start\n")
                                                                                                        #p#print(ranges_list)
                                                                                                        #print("\ninside hash structure ranges_list end\n")

                                                                                                elif(splitted_each_inside_modifier_keys[1][:-1]==num):               
                                                                                                        for each_hash_list in hash_value_list:
                                                                                                                ranges_list=ranges_list+mix_range_with_letters(each_hash_list)
                                                                                                #for each_range_item in range(len(ranges_list)):
                                                                                                #     #print("\n for replacement loop \n")
                                                                                                #     if(re.search(r'_IF.*?\_',ranges_list[each_range_item].strip())):
                                                                                                #         ranges_list[each_range_item]=getname(ranges_list[each_range_item].strip())

                                                                                                #print("now append the commands\n")
                                                                                                if (len(command_list1)!=len(ranges_list)):
                                                                                                        command_list1=command_list1*len(ranges_list)
                                                                                                for tracerack in range(len(command_list1)):
                                                                                                        if(mod_num_list_index==len(mod_num_list)):
                                                                                                              command_list1[tracerack]=command_list1[tracerack]+" "+ re.sub(r'{{'+num+'}}', ranges_list[tracerack], raw_command_list[i])
                                                                                                        else:
                                                                                                              command_list1[tracerack]=command_list1[tracerack]+" "+ re.sub(r'{{'+num+'}}.*', ranges_list[tracerack], raw_command_list[i])
                                                                                                              
                                                                                                raw_command_list[i]=re.sub(r'{{'+num+'}}', "", raw_command_list[i])

                                                                                if(hash_structure_exists==0):
                                                                                        if('mod_'+str(num)  in inside_modifier_keys):
                                                                                                modifier_data=data[needylist_key][each_and_every_cmd][iterate_keys]['mod_'+str(num)]
                                                                                                modifier_keys=list(modifier_data.keys())
                                                                                        elif(str(num) in list(static_cmd_dict.keys())):
                                                                                                modifier_data=data[needylist_key][int(static_cmd_dict[num])]['mod_'+str(num)]
                                                                                                modifier_keys=list(modifier_data.keys())
                                                                                        else:
                                                                                                #print("modifier key "+num+" is missing in "+each_need +" group aborting script\n\n")
                                                                                                sys.exit(50)
                                                                       
                                                                        elif(isinstance(data[needylist_key][each_and_every_cmd][iterate_keys],list)):
                                                                            #print("\nmight be a modifier in array\n")
                                                                            list_found=data[needylist_key][each_and_every_cmd][iterate_keys]
                                                                            #print("\nlist iterate_kyes \n")
                                                                            #p#print(data[needylist_key][each_and_every_cmd][iterate_keys])
                                                                            #print("\nlist iterate_keys end\n")   
                                                                            for each_item in range(len(list_found)):
                                                                                #print("\n inside for loop\n")
                                                                                if(isinstance(data[needylist_key][each_and_every_cmd][iterate_keys][each_item],dict)):
                                                                                     #print("\nin is dictionary\n")
                                                                                     tmp_keys=data[needylist_key][each_and_every_cmd][iterate_keys][each_item].keys()
                                                                                     #print("\n tmp_keys \n")
                                                                                     #p#print(tmp_keys)
                                                                                     if ('mod_'+str(num) in tmp_keys):
                                                                                        #print("\nmodifier matched in list_found\n")
                                                                                        modifier_data=data[needylist_key][each_and_every_cmd][iterate_keys][each_item]['mod_'+str(num)]
                                                                                        modifier_keys=list(modifier_data.keys())
                                                                                
                                                                                
                                                                                                         
                                                                        else:
                                                                                if(str(num) in list(static_cmd_dict.keys())):
                                                                                        modifier_data=data[needylist_key][int(static_cmd_dict[num])]["mod_"+str(num)]
                                                                                        modifier_keys=list(modifier_data.keys())
                                                                                else:
                                                                                        #print("modifier key "+num+" is missing in "+each_need +" group aborting script\n\n")
                                                                                        sys.exit(50)
                                                                        #print("\nmodifier data start\n")
                                                                        #p#print(modifier_data)
                                                                        #print("\nmodifier data end\n")
                                                                        #print("\nmodifier keys start\n")
                                                                        target_specific_list=[]
                                                                        modifier_targets=[]
                                                                        target_specific_list=concate_hash(target_specific_list,modifier_data,"")
                                                                        #target_specific_list_dummy=target_specific_list+[]
                                                                        #tmp_device_name=""
                                                                        #for each_target_dummy in range(target_specific_list):
                                                                        #    splitted_target_or_not=each_target_dummy.strip().split(' ')
                                                                            
                                                                        #print("\ntarget_specific_list start\n")
                                                                        #p#print(target_specific_list)
                                                                        #print("\ntarget_specific_list end\n")
                                                                        deleted_list=[]
                                                                        for each_target_specific_list in target_specific_list:
                                                                            splitted_target_or_not=each_target_specific_list.strip().split(' ')
                                                                            tmp_bkup=command_list1+[]
                                                                            if(len(splitted_target_or_not)>2):
                                                                               is_target_specific_modifier=1
                                                                               device_name=splitted_target_or_not[0].strip()
                                                                               device_name_list=mix_range_with_letters(device_name)
                                                                               target_specific_dict[splitted_target_or_not[1]]=splitted_target_or_not[2]
                                                                               #print("\ntarget_specific_dict start\n")
                                                                               #p#print(target_specific_dict)
                                                                               #print("\ntarget_specific_dict end\n")
                                                                               if not(splitted_target_or_not[0] in deleted_list):
                                                                                     del modifier_data[splitted_target_or_not[0]]
                                                                                     deleted_list.append(splitted_target_or_not[0])
                                                                               for new_hash_formats in target_specific_list:
                                                                                   modifier_target_modified=new_hash_formats.split(' ')
                                                                                   if(len(modifier_target_modified)==2):
                                                                                     target_specific_dict[modifier_target_modified[0]]=modifier_target_modified[1]
                                                                                   elif(splitted_target_or_not[0].strip()==modifier_target_modified[0].strip()):
                                                                                     target_specific_dict[modifier_target_modified[1]]=modifier_target_modified[2]
                                                                                     

                                                                               #print("\nbefore calling generate cmds target_specific_dict start\n")
                                                                               #p#print(target_specific_dict)
                                                                               #print("\nbefore calling generate cmds target_specific_dict end\n")

                                                                               if not(each_target_specific_list==target_specific_list[len(target_specific_list)-1]): 
                                                                                      tmp_bkup=generatecmds_from_modifier_data_and_value(target_specific_dict,list(target_specific_dict.keys()),tmp_bkup,mod_num_list_index,mod_num_list,raw_command_list,i,'last')
                                                                               else:
                                                                                      tmp_bkup=generatecmds_from_modifier_data_and_value(target_specific_dict,list(target_specific_dict.keys()),tmp_bkup,mod_num_list_index,mod_num_list,raw_command_list,i)
                                                                             
                                                                               for each_device in device_name_list:
                                                                                   target_modifier_dict_keys=target_modifier_dict.keys()
                                                                                   if(each_device in target_modifier_dict_keys):
                                                                                       tmp_command_list=target_modifier_dict[each_device]
                                                                                       target_modifier_dict[each_device]=tmp_command_list+tmp_bkup
                                                                                   else:
                                                                                       target_modifier_dict[each_device]=tmp_bkup
                                                                               #command_list1=[]
                                                                               #print("\neach_device target_modifier_dict "+each_device+"\n")
                                                                               #p#print(target_modifier_dict)
                                                                               #print("\neach_device target_modifier_dict "+each_device+"\n")
                                                                               
                                                                        #p#print(modifier_keys)
                                                                        #print("\nmodifier keys end\n")
                                                                        #print("reading modifier values\n\n")
                                                                        if(is_target_specific_modifier==0):
                                                                            command_list1=generatecmds_from_modifier_data_and_value(modifier_data,modifier_keys,command_list1,mod_num_list_index,mod_num_list,raw_command_list,i)
                                                                        mod_num_list_index=mod_num_list_index+1
                                                        else:
                                                                if(is_target_specific_modifier==0): 
                                                                    for pq in range(len(command_list1)):
                                                                            command_list1[pq]=command_list1[pq]+" "+raw_command_list[i]+" "
                                                                    #print("in fffffff not match else\n")
                                                                    #p#print(command_list1)
                                                                else:
                                                                    mod_specific_targets=target_modifier_dict.keys()
                                                                    for each_target in mod_specific_targets:
                                                                        command_list1=target_modifier_dict[each_target]
                                                                        for pq in range(len(command_list1)):
                                                                            command_list1[pq]=command_list1[pq]+" "+raw_command_list[i]+" "
                                                                        target_modifier_dict[each_target]=command_list1
                                                                        #print("in fffffff not match else\n")
                                                                        #p#print(command_list1)
                                                                #if(len(each_and_every_cmd_keys)==1 and isinstance(data[needylist_key][each_and_every_cmd][iterate_keys],list) and i==(len(raw_command_list)-1)):
                                                                #        recursive_modifier(data[needylist_key][each_and_every_cmd],each_need,iterate_keys,command_list1,targets)
                                                                #        hierarchical=1
                                                                #        continue
                                                #target_array=targets.split(",")
                                                if("LIST_HOLDER" in inside_modifier_keys):
                                                    #print("\n recursively vrf list called see this\n")
                                                    if(is_target_specific_modifier==0):
                                                        recursive_modifier(data[needylist_key][each_and_every_cmd][iterate_keys],each_need,"LIST_HOLDER",command_list1,targets)
                                                    else:
                                                        mod_specific_targets=target_modifier_dict.keys()
                                                        for each_target in mod_specific_targets:
                                                            command_list1=target_modifier_dict[each_target]
                                                            target_specific_list=[]
                                                            target_specific_list.append(each_target[1:])
                                                            recursive_modifier(data[needylist_key][each_and_every_cmd][iterate_keys],each_need,"LIST_HOLDER",command_list1,target_specific_list)

                                                    hierarchical=1
                                                    #continue 
                                                if(len(each_and_every_cmd_keys)==1 and isinstance(data[needylist_key][each_and_every_cmd][iterate_keys],list)):
                                                    #print("\n hierarchical vrf lst called see this\n")
                                                    if(is_target_specific_modifier==0):
                                                        recursive_modifier(data[needylist_key][each_and_every_cmd],each_need,iterate_keys,command_list1,targets)
                                                    else:
                                                        mod_specific_targets=target_modifier_dict.keys()
                                                        for each_target in mod_specific_targets:
                                                            command_list1=target_modifier_dict[each_target]
                                                            target_specific_list=[]
                                                            target_specific_list.append(each_target[1:])
                                                            recursive_modifier(data[needylist_key][each_and_every_cmd],each_need,iterate_keys,command_list1,target_specific_list)

                                                    #recursive_modifier(data[needylist_key][each_and_every_cmd],each_need,iterate_keys,command_list1,targets)
                                                    hierarchical=1
                                                    #continue
 
                                                if(hierarchical==0):
                                                      #print(colored("\n"+each_need+" tag successfully generated now writing to the files  \n",'green'))
                                                      if(is_target_specific_modifier==0):
                                                           write_to_targets(command_list1,targets)
                                                      else:
                                                           mod_specific_targets=target_modifier_dict.keys()
                                                           for each_target in mod_specific_targets:
                                                               #print("\neach_target "+each_target+"\n")
                                                               #p#print(target_modifier_dict)
                                                               #print("\neach_target "+each_target+"end\n")
                                                               
                                                               command_list1=target_modifier_dict[each_target]
                                                               target_specific_list=[]
                                                               target_specific_list.append(each_target.strip())
                                                               write_to_targets(command_list1,target_specific_list)      
                                                if(is_target_specific_modifier==0):
                                                     command_list1=[]
                                                else:
                                                     mod_specific_targets=target_modifier_dict.keys()
                                                     for each_target in mod_specific_targets:
                                                         target_modifier_dict[each_target]=[]
                                                     command_list1=[]
                                                hierarchical=0
                                        if(each_and_every_cmd_keys[len(each_and_every_cmd_keys)-1]==iterate_keys and len(command_list1)>0 and hierarchical==0 and went_in_to_generate_cmd==0):
                                                #print("in array hierarchy")
                                                if(is_target_specific_modifier==0):
                                                     write_to_targets(command_list1,targets)              
                                                else:
                                                     mod_specific_targets=target_modifier_dict.keys()
                                                     for each_target in mod_specific_targets:
                                                         command_list1=target_modifier_dict[each_target]
                                                         target_specific_list=[]
                                                         target_specific_list.append(each_target.strip()) 
                                                         write_to_targets(command_list1,target_specific_list)


                                                #write_to_targets(command_list1,targets)        
                        else:
                                                #print("not a dictionary\n")
                                                if(isinstance(data[needylist_key][each_and_every_cmd],list)):
                                                        #print("\n\nlist found in data[needylist_key][each_and_every_cmd]\n\n")
                                                        raw_command=data[needylist_key][each_and_every_cmd]
                                                        #p#print(raw_command)
                                                        sys.exit(121)
                                                raw_command=data[needylist_key][each_and_every_cmd]
                                                #print("\nraw_command=="+raw_command+"\n")
                                                raw_command_list=raw_command.split(' ')
                                                for i in range(len(raw_command_list)):
                                                        if(re.search(r'.*{{(\w+)}}',raw_command_list[i])):
                                                                went_in_to_generate_cmd=1
                                                                #print("matched a number \n\n=="+str(i)+"\n\n")
                                                                p=re.compile(r'.*?{{(\w+)}}')
                                                                mod_num_list=p.findall(raw_command_list[i])
                                                                #print("\n mod_num_list start \n")
                                                                #p#print(mod_num_list)
                                                                #print("\n mod_num_list end \n")
                                                                mod_num_list_index=1
                                                                for each_mod_num_list in mod_num_list:
                                                                        matchobj=re.search(r'.*?(\w+)',each_mod_num_list)
                                                                        
                                                                        num=matchobj.group(1)
                                                                        #print("\ninside each_mod_num_list for loop match object"+matchobj.group(1)+"\n")
                                                                        modifier_data={}
                                                                        modifier_keys=[]
                                                                        if(str(num) in list(static_cmd_dict.keys())):
                                                                                modifier_data=data[needylist_key][int(static_cmd_dict[num])]["mod_"+num]
                                                                                modifier_keys=list(modifier_data.keys())
                                                                        else:
                                                                                #print("modifier key "+num+" is missing in "+each_need +" group aborting script\n\n")
                                                                                sys.exit(50)
                                                                        #print("\n modifier_data start\n")
                                                                        #p#print(modifier_data)
                                                                        #print("\n modifier_data end\n")
                                                                        #print("\n modifier_keys start\n")
                                                                        target_specific_list=[]
                                                                        modifier_targets=[]
                                                                        target_specific_list=concate_hash(target_specific_list,modifier_data,"")
                                                                        #print("\nelse target_specific_list start\n")
                                                                        #p#print(target_specific_list)
                                                                        #print("\nelse target_specific_list end\n")
 
                                                                        for each_target_specific_list in target_specific_list:
                                                                            splitted_target_or_not=each_target_specific_list.strip().split(' ')
                                                                            tmp_bkup=command_list1+[]
                                                                            if(len(splitted_target_or_not)>2):
                                                                               is_target_specific_modifier=1
                                                                               device_name=splitted_target_or_not[0]
                                                                               device_name_list=mix_range_with_letters(device_name)
                                                                               target_specific_dict[splitted_target_or_not[1]]=splitted_target_or_not[2]
                                                                               del modifier_data[splitted_target_or_not[0]]
                                                                               for new_hash_formats in target_specific_list:
                                                                                   modifier_target_modified=new_hash_formats.split(' ')
                                                                                   if(len(modifier_target_modified)==2):
                                                                                     target_specific_dict[modifier_target_modified[0]]=modifier_target_modified[1]
                                                                               if not(each_target_specific_list==target_specific_list[len(target_specific_list)-1]):
                                                                                  tmp_bkup=generatecmds_from_modifier_data_and_value(target_specific_dict,list(target_specific_dict.keys()),tmp_bkup,mod_num_list_index,mod_num_list,raw_command_list,i,'last')
                                                                               else:
                                                                                  tmp_bkup=generatecmds_from_modifier_data_and_value(target_specific_dict,list(target_specific_dict.keys()),tmp_bkup,mod_num_list_index,mod_num_list,raw_command_list,i)
                                                                               for each_device in device_name_list:
                                                                                   target_modifier_dict_keys=target_modifier_dict.keys()
                                                                                   if(each_device in target_modifier_dict_keys):
                                                                                       tmp_command_list=target_modifier_dict[each_device]
                                                                                       target_modifier_dict[each_device]=tmp_command_list+tmp_bkup
                                                                                   else:
                                                                                       target_modifier_dict[each_device]=tmp_bkup
                                                                                   #print("\neach_device target_modifier_dict "+each_device+"\n")
                                                                                   #p#print(target_modifier_dict)
                                                                                   #print("\neach_device target_modifier_dict "+each_device+"\n")
                                                                        #p#print(modifier_keys)
                                                                        #print("\n modifier_keys end\n")
                                                                        #print("reading modifier values\n\n")
                                                                        if(is_target_specific_modifier==0):
                                                                             command_list1=generatecmds_from_modifier_data_and_value(modifier_data,modifier_keys,command_list1,mod_num_list_index,mod_num_list,raw_command_list,i)        
                                                                        mod_num_list_index=mod_num_list_index+1
                                                        else:
                                                                
                                                                #for pq in range(len(command_list1)):
                                                                #        command_list1[pq]=command_list1[pq]+" "+raw_command_list[i]+" "        
                                                                ##print("\n command_list start in else not match fffff\n") 
                                                                ##p#print(command_list1)
                                                                ##print("\n command_list start in else not match fffff\n")
                                                                if(is_target_specific_modifier==0):
                                                                    for pq in range(len(command_list1)):
                                                                            command_list1[pq]=command_list1[pq]+" "+raw_command_list[i]+" "
                                                                    #print("in fffffff not match else\n")
                                                                    #p#print(command_list1)
                                                                else:
                                                                    mod_specific_targets=target_modifier_dict.keys()
                                                                    for each_target in mod_specific_targets:
                                                                        command_list1=target_modifier_dict[each_target]
                                                                        for pq in range(len(command_list1)):
                                                                            command_list1[pq]=command_list1[pq]+" "+raw_command_list[i]+" "
                                                                        target_modifier_dict[each_target]=command_list1
                                                                        #print("in fffffff not match else\n")
                                                                        #p#print(command_list1)
                                                if(is_target_specific_modifier==0):
                                                           write_to_targets(command_list1,targets)
                                                else:
                                                     mod_specific_targets=target_modifier_dict.keys()
                                                     for each_target in mod_specific_targets:
                                                         command_list1=target_modifier_dict[each_target]
                                                         target_specific_list=[]
                                                         target_specific_list.append(each_target.strip())
                                                         write_to_targets(command_list1,target_specific_list)
                                                #write_to_targets(command_list1,targets)
                                                #print("")
                                                if(is_target_specific_modifier==0):
                                                     command_list1=[]
                                                else:
                                                     mod_specific_targets=target_modifier_dict.keys()
                                                     for each_target in mod_specific_targets:
                                                         target_modifier_dict[each_target]=[]
                                                     command_list1=[]

                                                #command_list1=[]                                                
                targets_str=""
                for each_targets in targets:
                     targets_str=targets_str+str(each_targets)+","
                #print("\n"+each_need+" group successfully generated for "+targets_str[:-1]+"  \n")
                                                
        static_cmd_dict={}

def write_to_targets(command_list1,targets):
  for each_file in targets:
           ##print(colored("\n"+each_need+" tag successfully generated now writing to the files\n",'green'))
           static_cmd_dict_splitted=command_list1[0].split(" ")
           append_or_not=0
           if(str(each_file) in list(router_group_dict.keys())):
                   list_of_tags=router_group_dict[str(each_file)]
                   for each_list_of_tags in list_of_tags:
                           if not(each_list_of_tags==static_cmd_dict_splitted[2]):
                                  append_or_not=1
           if(append_or_not==1):
                         router_group_dict[str(each_file)].append(static_cmd_dict_splitted[2])
           else:
                   router_group_dict[str(each_file)].append(static_cmd_dict_splitted[2])
           #print("now writing to the file")
           create_new_file=0
           for each_target in total_targets :
               if(re.search(each_file,each_target)):
                   create_new_file=1
                   with open(log_location_path+"/"+each_target+"_config.set", 'a') as outfile: 
                           for each_comm in command_list1:
                                  #outfile.write(each_comm+"\n")
                                  outfile.write(re.sub(' +',' ',each_comm)+"\n")
                           ##print(colored("\n"+each_need+" tag successfully writen to the "+"R"+str(each_file)+"file  \n",'green'))
           if(create_new_file==0):
                   timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
                   total_targets.append(each_file+"_"+timestamp)
                   with open(log_location_path+"/"+str(each_file)+"_"+timestamp+"_config.set", 'w') as outfile: 
                           for each_comm in command_list1:
                                  #outfile.write(each_comm+"\n")
                                  outfile.write(re.sub(' +',' ',each_comm)+"\n")
                           ##print(colored("\n"+each_need+" tag successfully writen to the "+"R"+str(each_file)+"file  \n",'green'))


                
def generatecmds_from_modifier_data_and_value(modifier_data,modifier_keys,command_list1,mod_num_list_index,mod_num_list,raw_command_list,i,optional=None):

   if("VALUE" in modifier_keys):
           unindentified=modifier_data["VALUE"]
           if(unindentified.find('.')!=-1 or unindentified.find(':')!=-1):
                    if((not("LINK" in modifier_keys)) or modifier_data["LINK"]=='one2one'):
                            if((not("TYPE" in modifier_keys)) or modifier_data["TYPE"]=="ip"):
                                   #print("\n call start in else one2one ipv4 or ipv6 next ip function mapping is one2one== \n\n")
                                   if (len(command_list1)==1):
                                           #print("inside if not equal to count 1 \n\n")
                                           if("COUNT" in modifier_keys):
                                                   command_list1=command_list1*(int(modifier_data["COUNT"]))
                                           else:
                                                   #print("as a first ip modifier key you must define a Count key in a "+each_need+" group aborting script \n")
                                                   sys.exit(100)
                                           #print("commmand_list1 len==="+str(len(command_list1))+"\n\n")
                                   #print("\nafter if\n")
                                   command_track=0
                                   ip_addr=modifier_data["VALUE"];
                                   ip_step='x'
                                   ip_count=0
                                   if "STEP" in modifier_keys:
                                           ip_step=modifier_data["STEP"];
                                   if "COUNT" in modifier_keys:
                                           ip_count=int(modifier_data["COUNT"]);
                                   #print("\ncalling ip addr list method \n")
                                   ip_addr_list=generate_ip(ip_addr,ip_step,len(command_list1))
                                   #print("\ncalling ip addr list method end \n")
                                   ip_count=len(command_list1)
                                   for address in ip_addr_list:
                                           if(command_track==ip_count):
                                                   break
                                           #print("generated address is=="+address+"\n\n")
                                           if(mod_num_list_index==len(mod_num_list)):
                                                command_list1[command_track]=command_list1[command_track]+" "+ re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', address, raw_command_list[i])
                                           else:
                                                command_list1[command_track]=command_list1[command_track]+" "+ re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}.*', address, raw_command_list[i])
                                           command_track=command_track+1
                                   if(optional==None):
                                         raw_command_list[i]=re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', "", raw_command_list[i])
                                   #print("\n command_list start\n")
                                   #p#print(command_list1)
                                   #print("\n command_list end\n")
                           
                    else:
                           if((not("TYPE" in modifier_keys)) or modifier_data["TYPE"]=="ip"):
                                   #print("call start in else one2many ipv4 or ipv6 next ip function mapping is one2many== \n\n")
                                   if not ("COUNT" in modifier_keys):
                                           #print("in one2many link relation count must defined aborting script \n\n")
                                           sys.exit(150)
                                   initial_len=len(command_list1)
                                   command_tracker=0
                                   command_list1=command_list1*int(modifier_data["COUNT"])
                                   list_tracker=0
                                   ip_addr_list=generate_ip(ip_addr,ip_step,len(command_list1))
                                   for address in ip_addr_list:
                                           if(command_tracker==int(modifier_data["COUNT"])):
                                                   break
                                           #print("generated address is=="+address+"\n\n")
                                           for ukl in range(list_tracker,list_tracker+initial_len):
                                                   if(mod_num_list_index==len(mod_num_list)):
                                                         command_list1[ukl]=command_list1[ukl]+" "+re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', address, raw_command_list[i]) 
                                                   else:
                                                         command_list1[ukl]=command_list1[ukl]+" "+re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}.*', address, raw_command_list[i]) 
                                           list_tracker=list_tracker+initial_len
                                           command_tracker=command_tracker+1
                                   if(optional==None):
                                          raw_command_list[i]=re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', "", raw_command_list[i])
                                                   
                                           
                                   #print("after one2many operation \n\n")
                                   #p#print(command_list1)
                           
                   ##one2many has ended here##
   
           else:
                   if( (not("MODE" in modifier_keys)) or modifier_data["MODE"]=='expand'):
                           ranges=modifier_data["VALUE"]
                           ranges_list=mix_range_with_letters(ranges)
                           #print("\n ranges_list start \n")
                           #p#print(ranges_list)
                           #for each_range_item in range(len(ranges_list)):
                           #        #print("for replacement loop")
                           #        if(re.search(r'_IF.*?\_',ranges_list[each_range_item].strip())):
                           #            ranges_list[each_range_item]=getname(ranges_list[each_range_item].strip())
                           #print("\n ranges_list end \n")
                           if((not("LINK" in modifier_keys)) or modifier_data["LINK"]=='one2one'):
                                   #print("\n inside value one2one expand mode \n")
                                   #p#print(command_list1)
                                   #print("\n command list1 end")
                                   if(len(ranges_list)!=len(command_list1)):
                                           command_list1=command_list1*len(ranges_list)
                                   for each_command in range(len(command_list1)):
                                           #command_list1[each_command]=command_list1[each_command]+raw_command_list[i]+ranges_list[each_command]
                                           if(mod_num_list_index==len(mod_num_list)):
                                                command_list1[each_command]=command_list1[each_command]+ re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', ranges_list[each_command], raw_command_list[i])
                                           else:
                                                command_list1[each_command]=command_list1[each_command]+ re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}.*', ranges_list[each_command], raw_command_list[i])
                                   if(optional==None):
                                        raw_command_list[i]=re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', "", raw_command_list[i])
                                   #print("\ncommand_list1 start \n")
                                   #p#print(command_list1)
                                   #print("\ncommand_list1 end \n")
                           else:
                                   #print("\n inside value one2many expand mode \n")
                                   initial_len=len(command_list1)
                                   command_tracker=0
                                   real_index=0
                                   add_num=initial_len
                                   command_list1=command_list1*len(ranges_list)
                                   for each_command in range(len(command_list1)):
                                           if(mod_num_list_index==len(mod_num_list)):
                                                command_list1[each_command]=command_list1[each_command]+ re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', str(ranges_list[real_index]), raw_command_list[i])
                                           else:
                                                command_list1[each_command]=command_list1[each_command]+ re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}.*', str(ranges_list[real_index]), raw_command_list[i])
                                           command_tracker=command_tracker+1
                                           if(command_tracker==initial_len):
                                                   real_index=real_index+1
                                                   initial_len=initial_len+add_num
                                   if(optional==None):
                                          raw_command_list[i]=re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', "", raw_command_list[i])
                                   #print("\ncommand_list1 start \n")
                                   #p#print(command_list1)
                                   #print("\ncommand_list1 end \n")
                   
                   else:
                           ranges=modifier_data["VALUE"]
                           ranges_list=mix_range_with_letters(ranges)
                           
                           #print("\nranges_list start\n")
                           #p#print(ranges_list)
                           #print("\nranges_list end\n")
                           #for each_range_item in range(len(ranges_list)):
                           #        #print("\n for replacement loop \n")
                           #        if(re.search(r'_IF.*?\_',ranges_list[each_range_item].strip())):
                           #            ranges_list[each_range_item]=getname(tmp_str)
 
                           if((not("LINK" in modifier_keys)) or modifier_data["LINK"]=='one2one'):
                                   #print("\n inside value one2one list mode \n")
                                   if(len(ranges_list)!=len(command_list1)):
                                           command_list1=command_list1*len(ranges_list)
                                   for each_command in range(len(command_list1)):
                                           if(mod_num_list_index==len(mod_num_list)):
                                                 command_list1[each_command]=command_list1[each_command]+re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', ranges_list[each_command], raw_command_list[i])
                                           else:
                                                 command_list1[each_command]=command_list1[each_command]+re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}.*', ranges_list[each_command], raw_command_list[i])
                                   if(optional==None):
                                        raw_command_list[i]=re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', "", raw_command_list[i])
   
                                   #print("\ncommand_list1 start \n")
                                   #p#print(command_list1)
                                   #print("\ncommand_list1 end \n")
                           else:
                                   #print("\n inside value one2many list mode \n")
                                   initial_len=len(command_list1)
                                   command_tracker=0
                                   real_index=0
                                   add_num=initial_len
                                   command_list1=command_list1*len(ranges_list)
                                   for each_command in range(len(command_list1)):
                                           if(mod_num_list_index==len(mod_num_list)):
                                                command_list1[each_command]=command_list1[each_command]+re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', ranges_list[each_command], raw_command_list[i])
                                           else:
                                                command_list1[each_command]=command_list1[each_command]+re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}.*', ranges_list[each_command], raw_command_list[i])
                                           command_tracker=command_tracker+1
                                           if(command_tracker==initial_len):
                                                   real_index=real_index+1
                                                   initial_len=initial_len+add_num
                                   if(optional==None):
                                         raw_command_list[i]=re.sub(r'{{'+mod_num_list[mod_num_list_index-1]+'}}', "", raw_command_list[i])
                                   #print("\ncommand_list1 start \n")
                                   #p#print(command_list1)
                                   #print("\ncommand_list1 end \n")
   return command_list1

#def Config_Generate_using_template_file(filepath):
#         #global dict1
#         #dict1=global_dict
#         ##p#print(dict1)
#         ##p#print(Handles.pas_handle)
#         data = yaml_reader(filepath)
#         return total_targets
if  __name__ == "__main__" :
         #filepath = "./example/ipclose.yaml"
         filepath = sys.argv[1]
         initialize_config_engine(None,None)
         data = yaml_reader(filepath)
		
		
		
#configsetgenerator('hello-interval as 20 and dead-interval as 80', 'group OSPF_CONFIG protocols ospf area 0.0.0.0')
