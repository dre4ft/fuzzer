from managefuzz import init, manager
from findkeyword import find
import os 

def parse_fuzztype(fuzztype):
    as_list = fuzztype.split(',')
    length = len(as_list)
    if as_list[0] == "regex" and length < 3: 
        i = 1 
        while i < length : 
            current = as_list[i]
            as_list[i] = ','+current
            if current[len(current)-1] == '$' : 
                j = 1 
                second = ""
    
                while j <=i :
                    second = second + as_list[j]
                    j = j +1 
                as_list = [as_list[0], second, as_list[length-1]]
                length = 3
                break 
            i = i+1
    return as_list , length

def do(args):
    gen_results_folder()
    isin_url = 'FUZZ' in args.url
    isin_headers = False
    if args.headers :
        isin_headers = 'FUZZ' in args.headers
    isin_body = False
    if args.body :
        isin_body = 'FUZZ' in args.body 
    how_to_FUZZ , length = parse_fuzztype(args.fuzzType)
    if isin_url or isin_body or isin_headers:
        init(args.url,args.method,args.headers if args.headers else None,args.body if args.body else None )
        if length == 2 :
            return manager(how_to_FUZZ[0],how_to_FUZZ[1])
        elif length == 3 :
            return manager(how_to_FUZZ[0],how_to_FUZZ[1],how_to_FUZZ[2])
        else : 
            raise Exception("invalid fuzzing format")
    else : 
        print("no placeholder to fuzz founded")  


def gen_results_folder():
    path = "./results"
    if not os.path.exists(path):
        os.mkdir(path)