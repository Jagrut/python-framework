from pprint import pprint
from netaddr import *
import sys
def generate_ip(ip_addr,ip_count,ip_step=None):
        ip_addr_list=[]
        suffix=0
        network_host=ip_addr.split('/')
        ip = IPNetwork(ip_addr)
        count=0
        if not(len(network_host)==1):
             suffix=1
                
        if(ip_step==None):
                if(suffix==0):
                         print("You haven't define step either mask aborting scipt\n\n")
                         sys.exit(1)
 
                while(count<ip_count):
                        if(suffix==1):
                               ip_addr_list.append(str(ip.ip+count*(ip.size))+"/"+str(network_host[1]))
                        else:
                               ip_addr_list.append(str(ip.ip+count*(ip.size)))
                        count=count+1
        else:
                step_ip=IPAddress(ip_step)
                num_to_increase=int(step_ip)
                while(count<ip_count):
                        if suffix==0:
                                ip_addr_list.append(str(ip.ip+count*num_to_increase))
                        else:
                                ip_addr_list.append(str(ip.ip+count*num_to_increase)+"/"+network_host[1])
                        count=count+1
        pprint(ip_addr_list)
        return ip_addr_list
#generate_ip('1.1.0.1/24',100,'0.1.0.0')                   ## step_value==0.1.0.0
#generate_ip('1.1.0.1/24',300)                              ## without step_value only mask
#generate_ip('fd00:face:1:1::1/64',100,'0:1::')            ## step_value==0:1::
generate_ip('fd00:face:1:1::1/64',100)                    ## without step_value only mask
