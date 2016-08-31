from jnpr.toby.init import init
from jnpr.toby.hldcl import device
from pprint import pprint as pp
from copy import deepcopy
from PASConfigEngine import Config_Generate_using_template_file
from nextpasverify import verify_checks_under_template
#from PASVerifyCmdEngine import parse_from_cmdline

'''def config_generate_using_template_file(file_name):
    generate_config_files(file_name)

def verify_checks_under_template_file(fname, set_of_tags = None):
    result = verify_checks(fname, set_of_tags)
    if result is False:
       raise Exception('One or More Testcase is FAILED')
    return result

'''

class Keyword_Resources:
	def __init__(self):
		topo_handle = None
	def Initialize_Verify_Engine_with_templates(self,input_dict):
		try:
			if input_dict['topo_handle']:
				self.topo_handle = deepcopy(input_dict['topo_handle'])
				pass
		except Exception:
			print ('No Topology handle is given')
		try:
			if input_dict['input_yaml_file']:
				pass
		except Exception:
			print ('No Verification yaml is given')
		try:
			if input_dict['input_yaml_file']:
				pass
		except Exception as exp:
			print ('No Templates files is given')
		pp(input_dict)

	def Initialize_Config_Engine_with_templates(self,input_dict):
		try:
			if input_dict['topo_handle']:
				pass
		except Exception:
			print ('No Topology handle is given')
		try:
			if input_dict['input_yaml_file']:
				pass
		except Exception:
			print ('No Verification yaml is given')
		pp(input_dict)


