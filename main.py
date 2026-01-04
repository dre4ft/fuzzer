

import argparse
 
from serveur.webui import runapi_server
from handler import do
"""
-h ==> fuzz header / add specifique header
-b ==> fuzz body / add specifique body
-X ==> to specify the method 

"""

import argparse

def initparser():
    parser = argparse.ArgumentParser(description="API Fuzzer")
    subparsers = parser.add_subparsers(
        dest="mode",
        required=True,
        help="Run mode"
    )

    # -------- CLI MODE --------
    cli = subparsers.add_parser("cli", help="Run fuzzer in CLI mode")

    cli.add_argument(
        "fuzzType",
        type=str,
        help="Specify the fuzzing type (range, wordlist, regex, rand)"
    )

    cli.add_argument(
        "url",
        type=str,
        help="Target URL (use FUZZ keyword)"
    )

    cli.add_argument(
        "--headers",
        type=str,
        default=None,
        help="Headers as JSON string (can include FUZZ)"
    )

    cli.add_argument(
        "--body",
        type=str,
        default=None,
        help="Body as JSON string (can include FUZZ)"
    )

    cli.add_argument(
        "--method",
        type=str,
        default="GET",
        help="HTTP method (GET by default)"
    )

    # -------- SERVER MODE --------
    server = subparsers.add_parser("server", help="Run API server")

    server.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Bind address"
    )

    server.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Bind port"
    )

    return parser


def main():
    parser = initparser()
    args = parser.parse_args()

    if args.mode == "cli":

        do(
            args
        )

    elif args.mode == "server":
        runapi_server(
            host=args.host,
            port=args.port
        )



if __name__ == "__main__":
   
    main()
    """
    class args: 
        fuzzType = "range,1-10"
        url = "http://localhost:8089/FUZZ"
        method : str = None 
        body : dict = None 
        headers : dict  = None 
    
    parser = initparser()
    args = parser.parse_args()
    print(do(args))
    """


    """
    url = "http://localhost:8080/FUZZ"
    url , valid = find(url)
    if valid:

        init(url,"post")
        manager("rand",10,10)
    """
     

