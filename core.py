import requests 

"""
def basic_fuzzer(url, payload):
    response = requests.get(url.format(payload = payload),verify=False)
    if response.status_code == 200:
        print(f"[*] the payload {payload} hit a HTTP 200 at {url}")
    else :
        print(f"[*] the payload \"{payload}\" hit a HTTP {response.status_code} at {url}")

"""

def basic_fuzzer(url, payload):
    response = superfuzzer3000(url,payload,body={"test":"true"})
    if response.status_code == 200:
        print(f"[*] the payload {payload} hit a HTTP 200 at {url}")
    else :
        print(f"[*] the payload \"{payload}\" hit a HTTP {response.status_code} at {url}")





def superfuzzer3000(url,method=None,header : dict =None,body : dict =None, verbose = None):
    """
    verbose : 
    1 = print info if status code != 4XX
    2 = print all info
     
    """
    method = method.lower() if method else None
    if not method or method == "get": 
        r = requests.get(url,headers=header,data=body,verify=False)
    elif method == "post":
        r = requests.post(url,headers=header,data=body,verify=False)
    elif method == "put":
        r = requests.put(url,headers=header,data=body,verify=False)
    elif method == "patch":
        r = requests.patch(url,headers=header,data=body,verify=False)
    elif method == "delete":
        r = requests.delete(url,headers=header,data=body,verify=False)
    else : 
        raise Exception("method unavalible")

    return  r 