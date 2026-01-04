from core import superfuzzer3000
import os
from stringen import from_rand,from_regex
import re
import json
"""
range ==> FUZZ deviens le range param == 1-X
wordlist ==> remplacer FUZZ by word in wordlist param == path of the file 
regex ==> FUZZ deviens un rand valide du regex param == regex,iter
rand ==> rand alphanum param == len,iter
"""

url = None
method = None
headers = None
body = None 
verbose = None 
typefuzz = None

def init(url_,method_=None,headers_=None,body_=None,verbose = None ):
    global url,method,headers, body 
    url = url_ if url_ else url 
    method = method_ if method_ else method 
    headers = headers_ if headers_ else headers 
    body = body_ if body_ else body 


def manager(typeFuzz, parameter1, parameter2 = None ):
    global typefuzz
    typefuzz = typeFuzz+","+parameter1+","+(parameter2 if parameter2 else "")
    typeFuzz = typeFuzz.lower()
    filename = from_rand(15)
    path = f"results/{filename}.json"
    initJSONFile(path)
    iden = 0
    if typeFuzz == "range":
        for resp in handle_range(parameter1):
            append(path,createrequest_data(iden,resp))
            iden = iden +1
    elif typeFuzz == "wordlist":
        for resp in handle_wl(parameter1):
            append(path,createrequest_data(iden,resp))
            iden = iden +1
    elif typeFuzz == "regex":
        if parameter2 :
            for resp in handle_regex(parameter1,parameter2):
                append(path,createrequest_data(iden,resp))
                iden = iden +1
        else :
            raise ValueError
    elif typeFuzz == "rand" :
        if parameter2 :
            for resp in handle_rand(parameter1,parameter2):
                append(path,createrequest_data(iden,resp))
                iden = iden +1
        else: 
            raise ValueError
    else :
        raise ValueError
    closeJSONfile(path)
    return filename 

"""

---- handler by type ------

"""

def handle_range(values):
    bornes = values.split("-")
    start = int(bornes[0])
    finish = int(bornes[1])
    for i in range(start,finish):
        yield callfuzzer(i)

def handle_wl(path):
    for line in read_file(path):
        yield callfuzzer(line)

def handle_regex(regex,iter):
    i = 0 
    iter = int(iter)
    for _ in range(0,iter):
        payload = from_regex(regex)
        yield callfuzzer(payload)
      

def handle_rand(len,iter):
    i = 0 
    iter = int(iter)
    for _ in range(0,iter):
        payload = from_rand(len)
        yield callfuzzer(payload)
        



"""

----- verbose managment ------

"""

def handle_verbose(function): 
    verbose = int(verbose)
    for resp in  function : 
            payload = resp[0]
            r = resp[1]
            if not verbose or verbose == 1 : 
                    if match_errors(r.status_code) != 4:
                        print(f"[*] the payload \"{payload}\" hit a HTTP {r.status_code} at {url}")
            if verbose == 2 : 
                print(f"[*] the payload \"{payload}\" hit a HTTP {r.status_code} at {url}")


def initJSONFile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write("[\n") 
    append(path,createcontext_data())

def closeJSONfile(path):
    with open(path, 'a', encoding='utf-8') as f:
            f.write("]") 
            
def append(path, data):
        try:
            json_line = json.dumps(data, ensure_ascii=False, indent=2)
            with open(path, 'a', encoding='utf-8') as f:

                if os.path.getsize(path) > 2:  
                    f.write(",\n")
                f.write(json_line)

            
        except Exception as e:
            print(f"[!] Erreur lors de l'écriture JSON : {e}")

def createcontext_data():
    context = {
        "target_url":url,
        "method":method,
        "headers":headers,
        "body":body,
        "fuzzing_type":typefuzz
    }
    return {"fuzz_context":context}


def createrequest_data(iden,fuzzresp):
    payload = fuzzresp[0]
    r=fuzzresp[1]
    return {   
            f"request {iden}":{
            "payload" :payload,
            "response":{
                "status" : r.status_code,
                "headers" : dict(r.headers),
                "body":r.text
            } 
        }
    }
 



"""

--- others ----

"""


def match_errors(status):
    status = str(status)
    info = re.compile("^1..$")
    succes = re.compile("^2..$")
    redirect = re.compile("^3..$")
    client_err = re.compile("^4..$")
    server_err = re.compile("^5..$")

    if info.match(status):
        return 1 
    elif succes.match(status):
        return 2
    elif redirect.match(status):
        return 3 
    elif client_err.match(status):
        return 4 
    elif server_err.match(status):
        return 5 
    else : 
        raise ValueError

def read_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                yield line.strip()
    else : 
        raise FileNotFoundError
    
def callfuzzer(payload):
    return payload, superfuzzer3000(url.replace("FUZZ",str(payload)),method,json.loads(headers.replace("FUZZ",str(payload))) if headers else headers,json.loads(body.replace("FUZZ",str(payload))) if body else body)