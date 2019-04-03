from compare_am import get_random_pcp, get_best_response
from general_easyness import lprint, remove_special



def get_baseline(n):
    """ Establishes a baseline through comparing with the most upvoted answer to a

    post. results can be seen in reddit_qa.csv
    """
    questions = []
    answers = []
    qap = ["Questions,Top Answers,Chosen Answer Additive, Chosen Answer multiplicative, control score additive, control score multiplicative,reitze score additive,reitze score multiplicative,jochem score additive, jochem score multiplicative"]
    i = 0
    for pcp in get_random_pcp(n):
        question  = remove_special(pcp[0][1])
        answers = pcp[1]
        if answers == []:
            best_answer = ""
        else:
            best_answer = remove_special(answers[0][1])
        questions.append(question)
        answers.append(best_answer)
        a_add = get_best_response(question, "additive", nposts=1)
        a_mul = get_best_response(question, "multiplicative", nposts=1)
        combined = [question, best_answer, a_add, a_mul, str(int(best_answer==a_add)), str(int(best_answer==a_mul)),"","","",""]
        qap.append(",".join(combined))
    reddit_qa = "reddit_qa.csv"
    f = open(reddit_qa, "w+")
    for pair in qap:
        f.write(pair+"\n")
    f.close()


def get_answers_queryfile(filename):
    """ generates answers to questions from an input file

    output for us to judge is in our_qa.csv
    """
    f = open(filename, "r")
    w = open("our_qa.csv", "w+")
    w.write("Questions,Chosen Answer Additive, Chosen Answer multiplicative, reitze score additive,reitze score multiplicative,jochem score additive, jochem score multiplicative\n")
    for line in f.readlines():
        if line[-1] == "\n":
            line = line[:-1]
        question  = remove_special(line)
        a_add = get_best_response(question, "additive", nposts=1)
        a_mul = get_best_response(question, "multiplicative", nposts=1)
        combined = [question, a_add, a_mul, "","","",""]
        w.write(",".join(combined)+"\n")
    f.close()
    w.close()

filename = "our_questions.txt"
get_answers_queryfile(filename)
get_baseline(100)
