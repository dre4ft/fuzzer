def find(url : str)->str:
    l = len(url)
    i = 0
    to_return = ""
    fuzzfinded = False 
    while i<l:
        if url[i] == 'F':
            if i+1 < l and url[i+1] == 'U':
                if i+2<l and url[i+2] == 'Z':
                    if i+3<l and url[i+3] == 'Z':
                        to_return = to_return+"{payload}"
                        fuzzfinded = True
                        i = i + 4
                        continue 
        to_return = to_return+url[i]
        i=i+1
    
    return to_return,fuzzfinded
