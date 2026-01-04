

import argparse
 
from serveur.webui import runapi_server
from handler import do
"""
-h ==> fuzz header / add specifique header
-b ==> fuzz body / add specifique body
-X ==> to specify the method 

"""

def initparser():
    parser = argparse.ArgumentParser(description='fuzzer')
    parser.add_argument('fuzzType', type=str,help="specify the fuzzing type")
    parser.add_argument('url',type=str , help="url of the target")
    parser.add_argument('--headers', type=str,default=None, help="add a custom header which can carry a fuzzing payload using the same syntax")
    parser.add_argument('--body', type=str,default=None, help='add a custom header using a dict format which can carry a fuzzing payload using the same syntax')
    parser.add_argument('--method', type=str,default=None, help='specify the HTTP Method (GET by default)')
    return parser




if __name__ == "__main__":
   

    #runapi_server()
    """
    class args: 
        fuzzType = "range,1-10"
        url = "http://localhost:8089/FUZZ"
        method : str = None 
        body : dict = None 
        headers : dict  = None 
    """
    parser = initparser()
    args = parser.parse_args()
    print(do(args))
    #"""


    """
    url = "http://localhost:8080/FUZZ"
    url , valid = find(url)
    if valid:

        init(url,"post")
        manager("rand",10,10)
    """
     

