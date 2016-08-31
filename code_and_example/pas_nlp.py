from pprint import pprint
import re
import time
import datetime
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
        print("in mix_range_with_letters start")
        ranges_list=[]
        for each_token_range_list in token_range_list:
                m = re.search("\d+\-\d+", each_token_range_list)
                print("match condition m\n\n")
                pprint(m)
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
        pprint(ranges_list)
        return ranges_list


def configsetgenerator(str1,str2):
     command_list1=[]
     if(isinstance(str1,dict)):
         command_list1.append("set "+str2)
         command_list1=concate_hash(command_list1,str1,"")
         file_list="english_config.set"
         groups_list=[]
         for each_comm in command_list1:
                            if(re.search(r'.*group.*',each_comm)):
                                    command_splitted=each_comm.split(" ")
                                    if not(command_splitted[2] in groups_list):
                                          groups_list.append(command_splitted[2].strip())
         with open(file_list,'w') as outfile:
                            for each_comm in command_list1:
                                   outfile.write(re.sub(' +',' ',each_comm)+"\n")
         with open(file_list,'a') as outfile:
                            for each_comm in groups_list:
                                   outfile.write("\nset apply-groups "+each_comm+"\n")
         return file_list

     tmp_list1=str1.split("and")
     command_list1=command_list1*(len(tmp_list1))
     
     for each_tmp_list1 in tmp_list1:
         old_size=0
         new_size=0
         tmp_str1=each_tmp_list1.strip()
         tmp_list2=tmp_str1.split("as")

         print("tmp_list2 start")
         pprint(tmp_list2)
         print("tmp_list2 end")
         for each_tmp_list2 in tmp_list2:
             expanded_list=mix_range_with_letters(each_tmp_list2.strip())
             print("expanded_list start")
             pprint(expanded_list)
             print("expanded_list end")
             if(old_size==0 and new_size==0):
                    old_size=len(command_list1)
                    command_list1.append("set "+str2+" "+expanded_list[0])
                    new_size=len(command_list1)
                    print("old_size=="+str(old_size)+"\n"+"new_size=="+str(new_size)+"\n")
                    print("0 0")
                    pprint(command_list1)
             else:
                    print("old_size=="+str(old_size)+"\n"+"new_size=="+str(new_size)+"\n")
                    for each_item in range(old_size,new_size):
                        command_list1[each_item]=command_list1[each_item]+" "+expanded_list[0]
                    print("not 0 0")
                    pprint(command_list1)
             print("")
             if(len(expanded_list)>1):
                for each_item in range(1,len(expanded_list)):
                    if((new_size-old_size)==1):
                          command_list1.append("set "+str2+" "+expanded_list[each_item])
                    else:
                          for each_list_item in range(old_size,new_size):
                              command_list1[each_list_item]=command_list1[each_list_item]+" "+expanded_list[each_list_item]

                new_size=len(command_list1)
     pprint(command_list1)

 
    # pprint(command_list1)               
             
     file_list="english_config.set"
     groups_list=[]
     for each_comm in command_list1:
                        if(re.search(r'.*group.*',each_comm)):
                                command_splitted=each_comm.split(" ")
                                if not(command_splitted[2] in groups_list):
                                      groups_list.append(command_splitted[2].strip())
     with open(file_list,'w') as outfile:
                        for each_comm in command_list1:
                               outfile.write(re.sub(' +',' ',each_comm)+"\n")
     with open(file_list,'a') as outfile:
                        for each_comm in groups_list:
                               outfile.write("\nset apply-groups "+each_comm+"\n")
     return file_list    

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
   
def configdeletegenerator(str1,str2):
     command_list1=[]
     if(isinstance(str1,dict)):
         command_list1.append("delete "+str2)
         command_list1=concate_hash(command_list1,str1,"")
         file_list="english_config.set"
         groups_list=[]
         for each_comm in command_list1:
                            if(re.search(r'.*group.*',each_comm)):
                                    command_splitted=each_comm.split(" ")
                                    if not(command_splitted[2] in groups_list):
                                          groups_list.append(command_splitted[2].strip())
         with open(file_list,'w') as outfile:
                            for each_comm in command_list1:
                                   outfile.write(re.sub(' +',' ',each_comm)+"\n")
         #with open(file_list,'a') as outfile:
         #                   for each_comm in groups_list:
         #                          outfile.write("\nset apply-groups "+each_comm+"\n")
         return file_list



     tmp_list1=str1.split("and")
     command_list1=command_list1*(len(tmp_list1))
     print("tmp_list1 start")
     pprint(tmp_list1)
     print("tmp_list1 end")
     for each_tmp_list1 in tmp_list1:
         old_size=0
         new_size=0
         tmp_str1=each_tmp_list1.strip()
         tmp_list2=tmp_str1.split("as")

         print("tmp_list2 start")
         pprint(tmp_list2)
         print("tmp_list2 end")
         for each_tmp_list2 in tmp_list2:
             expanded_list=mix_range_with_letters(each_tmp_list2.strip())
             print("expanded_list start")
             pprint(expanded_list)
             print("expanded_list end")
             if(old_size==0 and new_size==0):
                    old_size=len(command_list1)
                    command_list1.append("delete "+str2+" "+expanded_list[0])
                    new_size=len(command_list1)
                    print("old_size=="+str(old_size)+"\n"+"new_size=="+str(new_size)+"\n")
                    print("0 0")
                    pprint(command_list1)
             else:
                    print("old_size=="+str(old_size)+"\n"+"new_size=="+str(new_size)+"\n")
                    for each_item in range(old_size,new_size):
                        command_list1[each_item]=command_list1[each_item]+" "+expanded_list[0]
                    print("not 0 0")
                    pprint(command_list1)
             print("")
             if(len(expanded_list)>1):
                for each_item in range(1,len(expanded_list)):
                    if((new_size-old_size)==1):
                          command_list1.append("delete "+str2+" "+expanded_list[each_item])
                    else:
                          for each_list_item in range(old_size,new_size):
                              command_list1[each_list_item]=command_list1[each_list_item]+" "+expanded_list[each_list_item]
                              
                new_size=len(command_list1)   
     pprint(command_list1)
     
     file_list=""
     file_list="english_config.set"
     with open(file_list,'w') as outfile:
                        for each_comm in command_list1:
                               outfile.write(re.sub(' +',' ',each_comm)+"\n")
     return file_list

configsetgenerator("hello-interval and dead-interval as 80 and jk","group PAS_OSPF protocol ospf area 0.0.0.0",)
configdeletegenerator("hello-interval as 40 and dead-interval as 80","group PAS_OSPF protocol ospf area 0.0.0.0")
configdeletegenerator("ae2-5 as 40 and dead-interval as 80","group PAS_OSPF protocol ospf area 0.0.0.0")
