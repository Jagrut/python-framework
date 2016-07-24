import itertools
from pprint import pprint

def mixrange(s):
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l,h = map(int, i.split('-'))
            r+= range(l,h+1)
    return r


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


for address in ip_range('192.168.1-2.1-12,15,17,19/24'):  
	print(address)
