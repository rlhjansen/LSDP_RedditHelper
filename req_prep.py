import sys
import os
import importlib


def library_props(library_name):
    module = importlib.import_module(library_name)
    try:
        s = library_name + "==" + eval("module.__version__")
        print(s)
        return s
    except AttributeError:
        print(library_name, "no versioning, only master")
        return library_name


def import_library(library_name):
    exec("import " + library_name)

def write_requirements(libraries):
    f_name = "requirements.txt"
    f_out = open(f_name, "w+")
    for library in libraries:
        import_library(library)
        f_out.write(library_props(library) + os.linesep)


if __name__ == "__main__":
    if sys.argv[1:]:
        requirements = sys.argv[1:]
    else:
        requirements = [
            "gensim",
            "numpy",
            "praw",
            "nltk",
            "autocorrect",
            "sklearn",
            "tqdm",
            "stopit"
        ]

write_requirements(requirements)
