import rstr
import random


possibilities = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTIVWXYZ0123456789"


def from_regex(regex:str):
    return rstr.xeger(regex)

def from_rand(length:int):
    min =0
    i = 0 
    max = len(possibilities)
    to_return = ""
    length = int(length)
    while i<=length:
        current = random.randint(min,max-1)
        to_return = to_return+possibilities[current]
        i = i+1
    return to_return