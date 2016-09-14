import re
from pprint import pprint
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
                removed_if_required=re.search(r'-[a-zA-Z]+',each_token_range_list)
                if(removed_if_required):
                   each_token_range_list=each_token_range_list[:removed_if_required.start()+1]+each_token_range_list[removed_if_required.start()+1:removed_if_required.end()].replace(each_token_range_list[removed_if_required.start()+1:removed_if_required.end()],"")+each_token_range_list[removed_if_required.end():]
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
mix_range_with_letters("R0,R1-10,ae2,ae5-8,R0_R1_1-4_IF,R0-R4,device0-4,device8")
