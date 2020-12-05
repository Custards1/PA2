def parse_header(msg : str):
    it = 0
    res = list()
    head = None
    for word in msg.split('|'):
        if it == 0:
            head=word
            it+=1
        else:
            res.append(word)

    return (head,res)
def build_raw_response(number:int,string:str):
    return str(number)+'|'+string.replace("|","")
def build_raw_response_from_list(tag,args):
    res = str(tag).replace("|","")+'|'
    for i in args:
        res += i.replace("|","")+'|'
    res += '\n'
    return res
