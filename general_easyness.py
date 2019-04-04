import os
import numpy as np

inCharSet = "!@#$%^&*()[]{};:,./<>?\|`~-=_+\"\n"


def lprint(iterable, extra_sep="\n"):
    """ list-print,

    prints content of list below
    """
    for elem in iterable:
        if type(elem) == list:
            print("\t".join([str(e) for e in elem]), end=extra_sep)
        else:
            print(elem, end=extra_sep)


def minput(*args):
    input((args))


def vec_to_writeformat(vector):
    return str(str(list(vector))[1:-1])

def writeformat_to_vec(string_vector):
    return np.array([float(e) for e in string_vector.split(",")])

def remove_special(string):
    l = list(string)
    for i in range(len(l)):
        if not l[i].isalnum():
            l[i] = " "
    return "".join(l)


if __name__ == "__main__":
    # minput(5,2,4,8,6,5,9,1)
    t = np.array([1/(i+1) for i in range(300)])
    s = vec_to_writeformat(t)
    res = writeformat_to_vec(s)
    print(sum(t-res))
