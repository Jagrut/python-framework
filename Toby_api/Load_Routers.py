from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import re

handles = {}
dev = []
hosts = []

def Initialize_connections(get_handles):
	#print (get_handles)
	global handles
	global hosts
	global dev 
	handles = get_handles
	#print ("helloworld")
	#print (handles)
	for each_handle in list(handles['resources'].keys()):
		get_ip = handles['resources'][each_handle]['components']['primary']['re0']['mgt-ip']
		got_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",get_ip)
		hosts.append(got_ip.group())
	dev = hosts
	i=0
	try:
		for host in hosts:
			dev[i] = Device(host=hosts[i], user='regress', password='MaRtInI')
			dev[i].open()
			#import pdb;pdb.set_trace()
			#print dev[host].facts
			i = i + 1
	except Exception as err:
		print ("Cannot connect to Device:", err)
		print ("\n")
		return

def load_config_on_devices(fname = None ):
	#import pdb;pdb.set_trace()
	global handles 
	global hosts
	global dev
	print ("\n")
	i=0
	j=0
	#print ("to find")
	#print (handles)
	locallist = list(handles['resources'].keys())
	#router_index = 0
	for router in hosts:
		#import pdb; pdb.set_trace()
		#print ("find here")
		dev[i].bind( cu=Config )
		print ("Loading configuration changes on Device", hosts[i])
		print ("\n")
		#import pdb;pdb.set_trace()
		try:
			if fname:
				file_name = fname
				print ("loading " + file_name + " configuration on DUT " + router)
				with open(fname, 'r') as f:
					f_list = f.readlines()
					k=0
					for each_line in f_list:
						print ("Configuring Below command on ",hosts[k])
						print (each_line.strip())
						dev[k].cu.load(each_line.strip(), format='set')
						k = k + 1
			else:
				delimeter = locallist[j]
				file_name = delimeter+"_config.set"
				dev[i].cu.load(path=file_name, format="set", merge=True)
				j = j + 1
		except ValueError as err:
			print (err.message)
		except Exception as err:
			if err.rsp.find('.//ok') is None:
				rpc_msg = err.rsp.findtext('.//error-message')
				print ("Unable to load configuration changes: ", rpc_msg)
				print ("Unlocking the configuration on Device", hosts[i])
				print ("\n")
				#dev[i].close()
			return
		print ("\n")
		i = i+1

def Config_commit_on_devices():
	global handles 
	global hosts
	global dev
	devices = hosts
	print ("Trying to Commit the configurations on DUT's", devices)
	print ("\n")
	i = 0
	#print (devices,dev,"suraj")
	for host in devices:
		try:
			#print (host,dev[i],"NICE")
			dev[i].cu.commit()
			print ("Configuration is Committed Successfully on Device", devices[i])
		except CommitError:
			print ("Error: Unable to commit configuration on Device", devices[i])
			print ("\n")
		# End the NETCONF session and close the connection
		#dev[i].close()
		i = i + 1


def load_config_cmd_on_devices(fname):
	#import pdb;pdb.set_trace()
	global handles 
	global hosts
	global dev
	print ("\n")
	i=0
	j=0
	#print ("to find")
	#print (handles)
	locallist = list(handles['resources'].keys())
	#router_index = 0
	for router in hosts:
		#import pdb; pdb.set_trace()
		#print ("find here")
		#dev[i].bind( cu=Config )
		print ("Loading configuration changes on Device", hosts[i])
		print ("\n")
		#import pdb;pdb.set_trace()
		try:
			#print ("run trough python")
			file_name = fname
			#print ("loading " + file_name + " configuration on DUT " + router)
			cfg = Config(dev[i])
			print ("Configuring Below command on ",hosts[i])
			#print (each_line.strip())
			cfg.load(path=file_name, format="set", merge=True)
			#dev[k].cfg.load(each_line.strip(), format='set')
			#k = k + 1
			#j = j + 1
		except ValueError as err:
			print (err.message)
		except Exception as err:
			if err.rsp.find('.//ok') is None:
				rpc_msg = err.rsp.findtext('.//error-message')
				print ("Unable to load configuration changes: ", rpc_msg)
				print ("Unlocking the configuration on Device", hosts[i])
				print ("\n")
				#dev[i].close()
			return
		print ("\n")
		i = i+1

'''
t = {
  "resources": {
    "device1": {
      "interfaces": {
        "intf6_1": {
          "pic": "xe-0/0/6:1",
          "link": "connect2",
          "name": "xe-0/0/6:1"
        },
        "intf6_0": {
          "pic": "xe-0/0/6:0",
          "link": "connect1",
          "name": "xe-0/0/6:0"
        },
        "intf6_3": {
          "pic": "xe-0/0/6:3",
          "link": "connect4",
          "name": "xe-0/0/6:3"
        },
        "intf6_2": {
          "pic": "xe-0/0/6:2",
          "link": "connect3",
          "name": "xe-0/0/6:2"
        }
      },
      "components": {
        "primary": {
          "machine": "static",
          "name": "bedrock-scale2",
          "dh": "<jnpr.toby.hldcl.juniper.switching.ex.Qfx object at 0x7ffb6663ed30>",
          "re0": {
            "con-ip": "10.221.27.76",
            "isoaddr": "48.0005.80ff.f800.0000.0108.0001.0102.5507.6168.00",
            "domain": "englab.juniper.net",
            "name": "bedrock-scale2",
            "mgt-ip": "10.204.43.136/20",
            "mgt-ipv6": "abcd::10:204:43:136",
            "osname": "JunOS"
          },
          "make": "juniper",
          "os": "JunOS",
          "model": "qfx5100-24q"
        }
      }
    },
    "device0": {
      "interfaces": {
        "intf24_0": {
          "pic": "xe-0/0/24:0",
          "link": "connect1",
          "name": "xe-0/0/24:0"
        },
        "intf24_1": {
          "pic": "xe-0/0/24:1",
          "link": "connect2",
          "name": "xe-0/0/24:1"
        },
        "intf24_2": {
          "pic": "xe-0/0/24:2",
          "link": "connect3",
          "name": "xe-0/0/24:2"
        },
        "intf24_3": {
          "pic": "xe-0/0/24:3",
          "link": "connect4",
          "name": "xe-0/0/24:3"
        }
      },
      "components": {
        "primary": {
          "machine": "static",
          "name": "blr-pinnacle-scale01",
          "dh": "<jnpr.toby.hldcl.juniper.switching.ex.Qfx object at 0x7ffb6b250128>",
          "re0": {
            "con-ip": "10.221.27.77",
            "isoaddr": "47.0005.80ff.f800.0000.0108.0001.0102.5507.6168.00",
            "domain": "englab.juniper.net",
            "name": "blr-pinnacle-scale01",
            "mgt-ip": "10.204.33.192/20",
            "mgt-ipv6": "abcd::10:204:33:192",
            "osname": "JunOS"
          },
          "make": "juniper",
          "os": "JunOS",
          "model": "QFX5200-32C-AFO"
        }
      }
    }
  }
}


Initialize_connections(t)
load_config_on_devices()
Config_commit_on_devices()
load_config_cmd_on_devices('english_config.set')
Config_commit_on_devices()'''
