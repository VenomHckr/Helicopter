from random import randint as rand

def randbool(r, mxr):
    t = rand(0, mxr)
    return t <= r

def randcell(w, h):
    return (rand(0, h - 1), rand(0, w - 1))