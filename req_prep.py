import sys
from general_easyness import write_requirements


if __name__ == "__main__":
    if sys.argv[1:]:
        requirements = sys.argv[1:]
    else:
        requirements = [
            "gensim",
            "numpy",
            "praw"
        ]
    write_requirements(requirements)
