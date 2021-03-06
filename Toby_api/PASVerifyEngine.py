from __future__ import print_function
from yaml import load
import re
#from functions import *
from pprint import pprint
from jnpr.junos import Device
#from StringIO import StringIO
from lxml import etree
from io import StringIO
from io import BytesIO
from lxml.etree import tostring
from yaml import dump
import sys


def mix_range(s):
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l,h = list(map(int, i.split('-')))
            r += list(range(l,h+1))
    return r


def mix_range_with_letters(ranges):
    token_range_list=ranges.split(",")
    ranges_list=[]
    for each_token_range_list in token_range_list:
        m = re.search("\d+\-\d+", each_token_range_list)
        if m:
            actual_range=m.group(0)
            initial_range_len=len(ranges_list)
            ranges_list=ranges_list+mix_range(actual_range)
            for each_range_item in range(initial_range_len,len(ranges_list)):
                ranges_list[each_range_item]=each_token_range_list[:m.start()]+str(ranges_list[each_range_item])+each_token_range_list[m.end():]
        else:
            tmp_list = []
            tmp_list.append(each_token_range_list)
            ranges_list=ranges_list+tmp_list
    ranges_list = list(map(str,ranges_list))
    return ranges_list

def source_tamplate_data(data,testcase_name) :
    #import pdb;pdb.set_trace()
    file_list = data.get('USE_TMPL', [])
    source_file_data = []
    for each in range(0, len(file_list)):
        with open(file_list[each], 'r') as stream:
            try:
                tmpdata = load(stream)
            except Exception as exc:
                print(exc)
                print (file_list[each], "File Not able To Open ," \
                                        "Make sure File Present\n" \
                                        "Proceeding With Other Files")

        try:
            source_file_data.append(tmpdata['PAS_VERIFY_TMPL'])
        except Exception:
            print ("PAS_VERIFY_TMPL KeyWord Not Found " \
                   "Please Check Your Verify Tamplate yaml File,\n" \
                   " Check the Yaml Tamplate Format ")
    tmpl_file = None;
    for each_data in range(0, len(source_file_data)):
        tmp_keys = list(source_file_data[each_data].keys())
        if (testcase_name in tmp_keys):
            tmpl_file = each_data;
    if (tmpl_file == None):
        print ("Tamplate Not Found")
        return False
    else:
        return {testcase_name : source_file_data[tmpl_file][testcase_name]}

def form_tampl(tampl_data,each_testcase_data,testcasename):
    #import pdb;pdb.set_trace()
    tampl_each_data = tampl_data[testcasename]
    #print (tampl_data[testcasename].keys(),"----",each_testcase_data.keys())
    final_yaml = {}
    try :
        x = {'cmd':tampl_each_data['cmd']}
        final_yaml.update(x)
        #pprint(final_yaml)
    except Exception :
        print ("The cmd value not found in Tamplate for ",testcasename)
        return False
    modifier_present = re.findall(r'{{(.*?)}}', final_yaml['cmd'])
    # adding the Modifier
    if (len(modifier_present) > 0):
        tmp_mod = "mod_" + modifier_present[0]
        if modifier_present[0] in list(each_testcase_data.keys()) :
            final_yaml[modifier_present[0]]=(each_testcase_data[modifier_present[0]])
        elif modifier_present[0] in list(tampl_each_data.keys()):
            final_yaml[modifier_present[0]]=(tampl_data[modifier_present[0]])
        elif tmp_mod in list(each_testcase_data.keys()):
            #import pdb;
            #pdb.set_trace()
            final_yaml[tmp_mod]=(each_testcase_data[tmp_mod])
        elif tmp_mod in list(tampl_each_data.keys()):
            final_yaml[tmp_mod]=(tampl_data[tmp_mod])
        else:
            print ("Modifier present in cmd But no value found to proceed")
            return False

    # adding the TAG
    if 'TAG' in list(each_testcase_data.keys()) :
        final_yaml['TAG'] = each_testcase_data['TAG']
    elif 'TAG' in list(tampl_each_data.keys()) :
        final_yaml['TAG'] = tampl_data['TAG']

    #depending on xpath hierarchy moving forward
    #import pdb;
    #pdb.set_trace()
    if 'xpath' in list(tampl_each_data.keys()) :
        final_yaml['xpath'] = tampl_each_data['xpath']
    for x in list(each_testcase_data.keys()) :
        #import pdb;pdb.set_trace()
        if len(modifier_present) !=0:
            if x != 'TAG' and x!= modifier_present[0] and x!= "mod_" + modifier_present[0] and x != 'mode':
                if x not in list(tampl_each_data.keys()) and x in list(each_testcase_data.keys()):
                    final_yaml[x] = each_testcase_data[x]
                if x in list(tampl_each_data.keys()) and x in list(each_testcase_data.keys()):
                    final_yaml[x] = tampl_each_data[x]
                    try:
                        if 'value' in list(each_testcase_data[x].keys()):
                            final_yaml[x]['value'] = each_testcase_data[x]['value']
                        if 'operator' in list(each_testcase_data[x].keys()):
                            final_yaml[x]['operator'] = each_testcase_data[x]['operator']
                    except Exception:
                        print ("value or operator not given so going with tamplate value or operator")
        else :
            if x != 'TAG' and x!= 'mode':
                if x not in list(tampl_each_data.keys()) and x in list(each_testcase_data.keys()):
                    final_yaml[x] = each_testcase_data[x]
                if x in list(tampl_each_data.keys()) and x in list(each_testcase_data.keys()):
                    final_yaml[x] = tampl_each_data[x]
                    try:
                        if 'value' in list(each_testcase_data[x].keys()):
                            final_yaml[x]['value'] = each_testcase_data[x]['value']
                        if 'operator' in list(each_testcase_data[x].keys()):
                            final_yaml[x]['operator'] = each_testcase_data[x]['operator']
                    except Exception:
                        print ("value or operator not given so going with tamplate value or operator")
    return final_yaml


def replace_value_with_definition(main_data, replace_data,key_to_change):
    for key in list(main_data.keys()):
        if key == key_to_change:
            main_data[key] = replace_data


def evalute(expect_value,obtained_value,opr) :
    if(opr=="equal" or opr=="count"):
        if(type(obtained_value)==str):
            obtained_value.strip()
        #print "suraj",type(obtained_value),type(expect_value)
        if(str(expect_value)==str(obtained_value)) :
            return True
        else :
            return False
    elif(opr=="gt"):
        obtained_value.strip()
        #print "suraj","*",type(expect_value),type(obtained_value)
        if(expect_value<int(obtained_value)):
            return True
        else:
            return False
    elif(opr=="lt"):
        obtained_value.strip()
        if(expect_value>int(obtained_value)):
            return True
        else:
            return False

def final_process(data,tag,furdata,typ) :

    return_result = True
    tmptype = 0
    #pprint(data)
    #pprint (furdata)
    if 'value' in list(furdata.keys()) :
        print ("",tag)
        print ("  ----------------------")
        print ("\tEXPECTED VALUE :",furdata['value'])
        #print typ
        if typ==2 :
            tmptype =1
            nextdata=data[0]
        else :
            nextdata= data[0].find(tag)
        if('operator' in list(furdata.keys())):
            if(furdata['operator']=="count"):
                obtain_value=len(data)
            else :
                obtain_value =nextdata.text
        #print tostring(nextdata,pretty_print=True)
        print ("\tOBTAINED VALUE : ",obtain_value)
        print ("\tOPERATOR : ",furdata['operator'])
        result = evalute(furdata['value'],obtain_value,furdata['operator'])
        print ("\tRESULT : ",result)

        if (result == False):
            return_result = False
        #print result,"notry",return_result

        return return_result
    elif('operator' in list(furdata.keys())):
        opr = furdata['operator']
        if(opr=='count'):

            print (" ", tag)
            print ("  -----------------------")
            print ("\tOPERATOR : ", furdata['operator'])
            print ("\tRESULT : ",len(data))


        return return_result
    else :
        furkeys = list(furdata.keys())
        tmp=furkeys[0]
        #print "RAJ",tmp,furdata[tmp]
        for i in range(0,len(furkeys)):
            if furkeys[i]!="xpath":
                furdatap=furdata[furkeys[i]]
                #print "lolo",furdatap
                #print"hiiii",furkeys[i],len(data),tostring(data[0],pretty_print=True),"hii"
                if typ==2 :
                    datap=data
                else :
                    datap = data[0].xpath(tag)
                tagp = furkeys[i]
                final_process(datap,tagp,furdatap,1)


def replace_cmd(cmd,rep) :
    cmd = re.sub('{{[^>]+}}',rep,cmd)
    return cmd




def testcase_data(data,testcase) :
    #print data,testcase,"nice"
    cmd=data['cmd']
    path=None
    if 'xpath' in list(data.keys()):
        path=data['xpath']
    tmp = re.findall(r'{{(.*?)}}',cmd)
    #import pdb;pdb.set_trace()
    if(len(tmp)>0) :
        if tmp[0] in list(data.keys()):
            value = data[tmp[0]]
            #value = value['value']
        else :
            tmp_mod = "mod_"+tmp[0]
            value = data[tmp_mod]
            value = value['value']
    else :
        value = False
        tmp = False
    final_data={'rcmd':cmd , 'rpath': path ,'rvalue' : value, 'mod_list' : tmp}
    return final_data


def parse_from_cmdline(stanza,tampl,router,file_name, handle):
    with open(file_name, 'r') as stream:
        try:
            data = load(stream)
        except Exception as exc:
            print(exc)
    #data = load(file(file_name, 'r'))
    data= data['PAS_VERIFY_TMPL']
    data=data[tampl]
    tmpxx = re.findall(r'{{(.*?)}}', data['cmd'])
    tmp={
        "PAS_VERIFY": {
            "USE_TMPL": [file_name],
            router: {
                tampl:{}
            }
        }
    }
    test_tmp=stanza.split(' on ')
    #print test_tmp
    if len(test_tmp)>1 :
        interface_value = test_tmp.pop()
    total_testcases = test_tmp[0].split(' and ')
    for x in range(0,len(total_testcases)) :
        y=total_testcases[x].split(' ')
        testcase={
            y[0]: {
                "operator": y[1],
                "value": y[2]
            }
        }
        l= tmp['PAS_VERIFY']
        l=l[router]
        l[tampl].update(testcase)
    if (len(tmpxx) > 0):
        tmpx = "mod_" + tmpxx[0]
        interface_value = interface_value.split(" ")
        mod_data={tmpx: {"value": [interface_value[1]]}}
        l[tampl].update(mod_data)
    #print (tmp)
    with open('tmpdata.yaml','w') as outfile:
        dump(tmp, outfile, default_flow_style=True)
    x = verify_checks_under_template(handle,"tmpdata.yaml")
    return x



def dataprocessone(k,dut_data,dut_keys,testkeys,testundata,dev) :
    return_result = True
    testdata = testcase_data(dut_data[dut_keys[k]], dut_keys[k])
    mod_data = testdata['rvalue']
    #print type(mod_data),"hii",mod_data
    cmd = testdata['rcmd']
    path = testdata['rpath']
    mod_list = testdata['mod_list']
    if (mod_data == False):
        print ("cmd = ",cmd,"\n")
        processed_data = dev.cli(command=cmd,format="xml")
        if type(processed_data) ==str :
            print ("Unable to process the command Please check That command returns correct output OutPut")
            return False
        else:
            tree = etree.parse(BytesIO(tostring(processed_data)))
            r = tree.xpath(path)
            if(len(r)==0):
                print("Xpath is Not returning any thing Please check the cmd and xpath properly")
                return False
        for m in testkeys:
            if isinstance(testundata[m], dict):
                r_result = final_process(r, m, testundata[m], 1)
                if (r_result == False):
                    return_result = False
    else :
        for l in range(0, len(mod_data)):
            exe_cmd = replace_cmd(cmd, mod_data[l])
            print ("cmd = ", exe_cmd, "\n")
            processed_data = dev.cli(command=exe_cmd, format="xml")
            if type(processed_data) == str:
                print ("Unable to process the command Please check That command returns correct output OutPut")
                return_result = False
                continue
            else:
                tree = etree.parse(BytesIO(tostring(processed_data)))
                r = tree.xpath(path)
                if len(r) == 0:
                    print("Xpath is Not returning any thing Please check the cmd and xpath properly")
                    continue
            new_list = ["mod_" + x for x in mod_list]
            for m in testkeys:
                if isinstance(testundata[m], dict) and m not in new_list:
                    r_result=final_process(r, m, testundata[m], 1)
                    if (r_result == False):
                        return_result = False
    return return_result


def dataprocesstwo(k,dut_data,dut_keys,testkeys, testundata,dev):
    return_result= True
    testdata = testcase_data(dut_data[dut_keys[k]], dut_keys[k])
    mod_data = testdata['rvalue']
    cmd = testdata['rcmd']
    path = testdata['rpath']
    mod_list = testdata['mod_list']
    if mod_data == False:
        print ("cmd = ", cmd, "\n")
        processed_data = dev.cli(command=cmd, format="xml")
        if type(processed_data) == str:
            print ("Unable to process the command Please check That command returns correct output OutPut")
            return False
        else :
            tree = etree.parse(BytesIO(tostring(processed_data)))
        for m in testkeys:
            if isinstance(testundata[m],dict):
                path = testundata[m]['xpath']
                r = tree.xpath(path)
                if len(r) == 0:
                    print("", m)
                    print("  ----------------------")
                    print("  Xpath is Not returning any thing Please check the cmd and xpath properly\n")
                    return_result = False
                    continue
                r_result=final_process(r, m, testundata[m],2)
                if r_result == False:
                    return_result = False
    else:
        for l in range(0, len(mod_data)):
            exe_cmd = replace_cmd(cmd, mod_data[l])
            print ("cmd=", exe_cmd,"\n")
            processed_data = dev.cli(command=exe_cmd, format="xml")
            if type(processed_data) == str:
                print ("Unable to process the command Please check That command returns correct output OutPut")
                return_result = False
                continue
            else:
                tree = etree.parse(BytesIO(tostring(processed_data)))
            new_list = ["mod_" + x for x in mod_list]
            for m in testkeys:
                if isinstance(testundata[m], dict) and m not in new_list:
                    path = testundata[m]['xpath']
                    r = tree.xpath(path)
                    if len(r) == 0:
                        print("", m)
                        print("  ----------------------")
                        print("  Xpath is Not returning any thing Please check the cmd and xpath properly")
                        return_result = False
                        continue
                    r_result=final_process(r, m, testundata[m], 2)
                    if (r_result == False):
                        return_result = False
    return return_result


def verify_checks_under_template(t,file_to_parse, tag=None):
    """

    """
    print(type(t["resources"]['device0']['components']['primary']['dh']))
    return_result = True
    if tag:
        tag_list = tag.split(',')
    else:
        tag_list = []

    with open(file_to_parse, 'r') as stream:
        try:
            file_data = load(stream)
        except Exception as exc:
            print(exc)
            print (file_to_parse, "File Not able To Open ," \
                                  "Make sure File Present")
    try:
        data = file_data['PAS_VERIFY']
    except Exception:
        print ("PAS_VERIFY KeyWord Not Found " \
               "Please Check Your Verify yaml File," \
               "\n Check the Yaml Format ")
        return False
    data_keys = list(data.keys())
    #print ("suraj",type(data_keys),data_keys)

    # Entering to the Router For Execution
    for i in range(0,len(data_keys)):
        if data_keys[i] != "USE_TMPL":
            dut_data = data[data_keys[i]]
            router_pool = mix_range_with_letters(data_keys[i])
            for each_router in range(0,len(router_pool)):
                print ("Executing Testcases ON ", router_pool[each_router])
                print ("=================================================")
		#dev = Device(host=router_pool[each_router], user='regress', password='MaRtInI', gather_facts=False)
		#dev.open()
                dev=t["resources"][router_pool[each_router]]['components']['primary']['dh']
                #print(dir(dev),"suraj")
                all_test_data = data[data_keys[i]]
                all_testcases = list(all_test_data.keys())
                #print all_testcases,"hi"
                for each_testcase in range(0,len(all_testcases)):
                    each_testcase_data=all_test_data[all_testcases[each_testcase]]
                    each_testcase_keys = list(each_testcase_data.keys())
                    if ('xpath' not in each_testcase_keys) and ('cmd' not in each_testcase_keys):       #check for tamplate requried or not
                        tampl_data = source_tamplate_data(data,all_testcases[each_testcase])            #getting perticular tamplate datas of testcase
                        form_tampl_data = form_tampl(tampl_data,each_testcase_data,all_testcases[each_testcase])         #form The data from the testacase data and tamplate
                        replace_value_with_definition(all_test_data, form_tampl_data, all_testcases[each_testcase])        #replace for the normal flow
                        each_testcase_data = all_test_data[all_testcases[each_testcase]]            #redefining each_testcase_data and keys
                        each_testcase_keys = list(each_testcase_data.keys())
                        #pprint (all_test_data)

                    if len(tag_list)==0 :                #if tag is not present
                        #import pdb;pdb.set_trace()
                        print ("\t Entering TO ", all_testcases[each_testcase])
                        print ("-------------------------------------------")
                        if ('xpath' in each_testcase_keys) and ('cmd' in each_testcase_keys):
                            r_result = dataprocessone(each_testcase,all_test_data, all_testcases, each_testcase_keys,
                                                      each_testcase_data,dev)
                            if (r_result == False):
                                return_result = False
                        if ('xpath' not in each_testcase_keys) and ('cmd' in each_testcase_keys):
                            r_result = dataprocesstwo(each_testcase, all_test_data, all_testcases, each_testcase_keys,
                                                      each_testcase_data, dev)
                            if (r_result == False):
                                return_result = False
                    else:
                        for qq in range(0, len(tag_list)):
                            print ("ENTERING TO TAG : ", tag_list[qq])
                            for k in range(0, len(all_testcases)):
                                #testundata = all_test_data[all_testcases[k]]
                                testcase_tag = each_testcase_data.get('TAG', [])
                                if tag_list[qq] in testcase_tag:
                                    print ("ENtering TO ", all_testcases[k])
                                    if ('xpath' in each_testcase_keys) and ('cmd' in each_testcase_keys):
                                        r_result = dataprocessone(each_testcase, all_test_data, all_testcases,
                                                                  each_testcase_keys,
                                                                  each_testcase_data, dev)
                                        if (r_result == False):
                                            return_result = False
                                    if ('xpath' not in each_testcase_keys) and ('cmd' in each_testcase_keys):
                                        r_result = dataprocesstwo(each_testcase, all_test_data, all_testcases,
                                                                  each_testcase_keys,
                                                                  each_testcase_data, dev)
                                        if (r_result == False):
                                            return_result = False
    return return_result

#print (verify_checks_under_template("PAS_verify_demo.yaml"))
#print (parse_from_cmdline())






