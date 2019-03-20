import os
import importlib

i = importlib.import_module("matplotlib.text")


def library_props(library_name):
    module = importlib.import_module(library_name)
    return library_name + "==" + eval("module.__version__")

def import_library(library_name):
    exec("import " + library_name)
    print(eval(library_name+".__version__"))

def write_requirements(libraries):
    f_name = "requirements.txt"
    f_out = open(f_name, "w+")
    for library in libraries:
        import_library(library)
        f_out.write(library_props(library) + os.linesep)


def lprint(iterable):
    for elem in iterable:
        if type(elem) == list:
            print("\t".join(elem))
        else:
            print(elem)

def minput(*args):
    input((args))


if __name__ == '__main__':
    minput(5,2,4,8,6,5,9,1)
