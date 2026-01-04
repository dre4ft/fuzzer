from fuzzer import superfuzzer3000
import argparse
from generate_jwt import gen_weak_jwt

def initparser():
    parser = argparse.ArgumentParser(description='fuzzer')
    parser.add_argument('jwt', type=str,help="provide a legit JWT")
    parser.add_argument('url',type=str , help="url of the target")
    parser.add_argument('--headers', type=str,default=None, help="add a customs header ")
    parser.add_argument('--body', type=str,default=None, help='add a custom body using a dict format ')
    parser.add_argument('--method', type=str,default=None, help='specify the HTTP Method (GET by default)')
    parser.parser.add_argument('--wordlist', type=str,default=None, help='specify the wordlist for HS256 bruteforce ')
    return parser





def do(args):
    legit_token = args.jwt
    













if __name__ == "__main__":
    parser = initparser()
    args = parser.parse_args()
    do(args)