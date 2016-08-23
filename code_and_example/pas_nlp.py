from pprint import pprint
import re
import time
import datetime
def configsetgenerator(str1,str2,str3):
     command_list1=[]
     command_list1.append("set "+str2)
     tmp_list1=str1.split("and")
     command_list1=command_list1*(len(tmp_list1))
     i=0
     tmp_list=[]
     regex = re.compile(r"\s*r\s*", flags=re.I)
     targets_str=""
     map_device_ind_list=regex.split(str3)
     if '' in map_device_ind_list:
             map_device_ind_list.remove('')
     for each_generate_list in map_device_ind_list :
             tmp_list=tmp_list+mixrange(each_generate_list)
     print("\n\ntmp_list start\n\n")
     pprint(tmp_list)
     print("\n\ntmp_list end\n\n")

     for each_tmp_list1 in tmp_list1:
         tmp_str1=each_tmp_list1.strip()
         #if(re.search(r'config.*',tmp_str1)):
         #m=re.search(r'config.*',tmp_str1) 
         #command_list1.append("set "+str2)
         #tmp_str1=re.sub(r'config','', tmp_str1)
         #tmp_str1=tmp_str1.strip();
         #command_list1=command_list1*(len(tmp_list1))
         #if(re.search(r'delete.*',tmp_str1)):
         #m=re.search(r'config.*',tmp_str1)
         #command_list1.append("delete "+str2)
         #tmp_str1=re.sub(r'delete','', tmp_str1)
         #tmp_str1=tmp_str1.strip();
         #command_list1=command_list1*(len(tmp_list1))
         tmp_list2=tmp_str1.split("as")
         for each_tmp_list2 in tmp_list2:
             tmp_str2=each_tmp_list2.strip()
             command_list1[i]=command_list1[i]+" "+tmp_str2
         i=i+1
     file_list=[]
     for each_file in tmp_list:
        #if(each_file in total_targets):
        #        with open("R"+str(each_file)+"english_config.set", 'a') as outfile:
        #                     for each_comm in command_list1:
                                    #outfile.write(each_comm+"\n")
        #                            outfile.write(re.sub(' +',' ',each_comm)+"\n")
                             #print(colored("\n"+each_need+" tag successfully writen to the "+"R"+str(each_fil     e)+"file  \n",'green'))


        #else:
        #        total_targets.append(each_file)
                file_list.append("R"+str(each_file)+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d__%H:%M:%S')+"english_config.set", 'w')
                with open(file_list[len(file_list)-1]) as outfile:
                        for each_comm in command_list1:
                               #outfile.write(each_comm+"\n")
                               outfile.write(re.sub(' +',' ',each_comm)+"\n")
     return file_list    
     #pprint(command_list1)
     #return command_list1
def configdeletegenerator(str1,str2,str3):
     command_list1=[]
     command_list1.append("delete "+str2)
     tmp_list1=str1.split("and")
     command_list1=command_list1*(len(tmp_list1))
     tmp_list=[]
     i=0
     regex = re.compile(r"\s*r\s*", flags=re.I)
     targets_str=""
     map_device_ind_list=regex.split(str3)
     if '' in map_device_ind_list:
             map_device_ind_list.remove('')
     for each_generate_list in map_device_ind_list :
             tmp_list=tmp_list+mixrange(each_generate_list)
     print("\n\ntmp_list start\n\n")
     pprint(tmp_list)
     print("\n\ntmp_list end\n\n")
     for each_tmp_list1 in tmp_list1:
         tmp_str1=each_tmp_list1.strip()
         #if(re.search(r'config.*',tmp_str1)):
         #m=re.search(r'config.*',tmp_str1) 
         #command_list1.append("set "+str2)
         #tmp_str1=re.sub(r'config','', tmp_str1)
         #tmp_str1=tmp_str1.strip();
         #command_list1=command_list1*(len(tmp_list1))
         #if(re.search(r'delete.*',tmp_str1)):
         #m=re.search(r'config.*',tmp_str1)
         #command_list1.append("delete "+str2)
         #tmp_str1=re.sub(r'delete','', tmp_str1)
         #tmp_str1=tmp_str1.strip();
         #command_list1=command_list1*(len(tmp_list1))
         tmp_list2=tmp_str1.split("as")
         for each_tmp_list2 in tmp_list2:
             tmp_str2=each_tmp_list2.strip()
             command_list1[i]=command_list1[i]+" "+tmp_str2
         i=i+1
     
     file_list=[]
     for each_file in tmp_list:
        #if(each_file in total_targets):
        #        with open("R"+str(each_file)+"english_config.set", 'a') as outfile:
        #                     for each_comm in command_list1:
                                    #outfile.write(each_comm+"\n")
        #                            outfile.write(re.sub(' +',' ',each_comm)+"\n")
                             #print(colored("\n"+each_need+" tag successfully writen to the "+"R"+str(each_fil     e)+"file  \n",'green'))


        #else:
        #        total_targets.append(each_file)
                file_list.append("R"+str(each_file)+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d__%H:%M:%S')+"english_config.set", 'w')
                with open(file_list[len(file_list)-1]) as outfile:
                        for each_comm in command_list1:
                               #outfile.write(each_comm+"\n")
                               outfile.write(re.sub(' +',' ',each_comm)+"\n")
     return file_list
     #pprint(command_list1)

     #return command_list1
PASconfigsetgenerator("hello-interval and dead-interval as 80 and jk","group PAS_OSPF protocol ospf area 0.0.0.0",)
PASconfigdeletegenerator("hello-interval as 40 and dead-interval as 80 and jk","group PAS_OSPF protocol ospf area 0.0.0.0")
