from generate_jwt import gen_weak_jwt,isvalid

def man_payloads(init_payload, to_add):
    for key in to_add : 
        init_payload[key] = to_add[key]
    return init_payload


def create_jwt(legit_jwt,custom_payload:dict):
    try :
        parts = isvalid(legit_jwt)

    except Exception as e : 
        raise e
    
if __name__ == "__main__":
    init = {"iss": "joe","exp":5454544 ,"http://example.com/is_root": True}
    to_add = {"test":"TEST"}

    print(man_payloads(init,to_add))