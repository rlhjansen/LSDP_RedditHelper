

def lprint(iterable):
    for elem in iterable:
        if type(elem) == list:
            print("\t".join(elem))
        else:
            print(elem)

def minput(*args):
    input((args))

minput(5,2,4,8,6,5,9,1)
