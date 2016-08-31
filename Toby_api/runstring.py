from lxml.etree import tostring
import pprint

def runstring(getstring):
    print (tostring(getstring,pretty_print=True))

def print_dict (x):
    pprint.pprint(x)
