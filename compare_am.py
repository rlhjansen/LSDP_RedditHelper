
import numpy as np
import pandas as pd
from general_easyness import lprint, writeformat_to_vec, minput, remove_special
from sklearn.metrics.pairwise import cosine_similarity
from terminaltables import AsciiTable
from operator import itemgetter
from prepare_string import prep, additive, multiplicative
from reddit_search import db_load
from random import shuffle


adata = np.array([np.array([i, i/2]) if i % 2 else np.array([i, i*2]) for i in range(6)])
mdata = np.array([np.array([i+1, (i*6)/2]) for i in range(6)])
iddata = ["a"+str(i) for i in range(6)]
data = [adata, mdata, iddata]


def load_real_vectors():
    adata = []
    mdata = []
    iddata = []
    for line in open("reddit_va.csv", "r").readlines():
        if line[-1] == "\n":
            line = line[:-1]
        data = line.split(";")
        adata.append(writeformat_to_vec(data[0]))
        mdata.append(writeformat_to_vec(data[1]))
        iddata.append(data[2])
    data = [np.array(adata), np.array(mdata), iddata]
    return data



def load_id_database():
    titles = ["man goes fishing" if i % 2 else "man plays soccer" for i in range(6)]
    subreddit = "outdoor"
    upvote_ratios = [10/(4/(i % 2+1)) for i in range(6)]
    scores = [10**i for i in range(6)]
    selftexts = ["bla"+str(i) for i in range(5)] + ["i love soccer and fishing"]
    comments = [["comment"+str(i) for i in range(j+1)] for j in range(6)]
    posts = [[titles[i], subreddit, upvote_ratios[i], scores[i], selftexts[i], comments[i]] for i in range(6)]
    DB = {"a"+str(i) : posts[i] for i in range(6)}
    return DB

POSTDATABASE = load_real_vectors()
IDDATABASE = db_load()[0]

def cosine_sym_single(wv1, wv2):
    """ wrapper function for cosine similarity

    created for the usecase of comparing a single pair of vectors

    : single :  meaning-vector, received from either additive or multiplicative
    : other :   vectors like single
    """
    return cosine_similarity(wv1.reshape(1,-1), wv2.reshape(1,-1))

def cosine_sym_multi(wvs1, wvs2):
    """
    : single :  meaning-vector, received from either additive or multiplicative
    : others :  multiple vectors like single, added together using numpy.vstack([...])
    """
    if len(wvs1.shape) != 1:
        if len(wvs2.shape) != 1:
            return cosine_similarity(wvs1, wvs2)
        else:
            return cosine_similarity(wvs1, wvs2.reshape(1,-1))
    else:
        if len(wvs2.shape) != 1:
            return cosine_similarity(wvs1.reshape(1,-1), wvs2)
        else:
            return cosine_similarity(wvs1.reshape(1,-1), wvs2.reshape(1,-1))


def difference_vector(post, comment):
    """ computes the difference in meaning space between two vectors
    """
    return comment - post

def makecosfunc(v1):
    def newcos(v2):
        return cosine_sym_multi(v1, v2)
    return newcos

def lfunc(func, somearray):
    return np.apply_along_axis(func, axis=1, arr=somearray)

def find_n_max_inds(somearray, n):
    return np.argsort(-somearray)[:n]

def weightfunc(postvotes, commentvotes):
    return 1

def tuplelist_to_db(somelist):
    ad = np.array([elem[0] for elem in somelist])
    mu = np.array([elem[1] for elem in somelist])
    id = np.array([elem[2] for elem in somelist])
    data = [ad, mu, id]
    return data


def best_post_additive(postembedding, n):
    newcos = makecosfunc(postembedding)
    subres = lfunc(newcos, POSTDATABASE[0])
    res = subres[:,0,0]
    return itemgetter(*(find_n_max_inds(res, n).tolist()))(POSTDATABASE[2])

def best_post_multiplicative(postembedding, n):
    newcos = makecosfunc(postembedding)
    res = lfunc(newcos, POSTDATABASE[1])[:,0,0]
    return itemgetter(*(find_n_max_inds(res, n).tolist()))(POSTDATABASE[2])

def best_comment(expected_comment_vector, cvecs, comments, n):
    newcos = makecosfunc(expected_comment_vector)
    res = lfunc(newcos, cvecs)[:,0,0]
    return itemgetter(*(find_n_max_inds(res, n).tolist()))(comments)

def get_eligible_responses(post_comment_pairs, embeddingfunction):
    weights = []
    pvecs = []
    cvecs = []
    comments = []
    for pcp in post_comment_pairs:
        post = pcp[0]
        pvec = embeddingfunction(prep(post[1], verbose=False))
        if not len(pcp[1]):
            pvecs.append(pvec)
            cvecs.append(embeddingfunction(prep("", verbose=False)))
            comments.append("")
            weights.append(1)

        for comment in pcp[1]:
            try:
                pvecs.append(pvec)
                weights.append(weightfunc(post[0], comment[0]))
                cvec = embeddingfunction(prep(comment[1], verbose=False))
                cvecs.append(cvec)
                comments.append(remove_special(comment[1]))
            except:
                print(pcp)
                raise ValueError("string index out of range")
    wvec = np.array(weights)
    pvecs = np.array(pvecs)
    cvecs = np.array(cvecs)
    distances = difference_vector(pvecs, cvecs)
    print(distances.shape, wvec.shape)
    answerdistance = distances * wvec[:, np.newaxis]
    # print("wvec", wvec.shape)
    # print("distances", distances.shape)
    # print("answer distances", answerdistance.shape)
    return cvecs, comments, answerdistance

def get_best_response(query, embeddingfunction, nposts=5):
    prep_query = eval(embeddingfunction)(prep(query, verbose=False))
    if embeddingfunction == "additive":
        res_ids = best_post_additive(prep_query, nposts)
    elif embeddingfunction == "multiplicative":
        res_ids = best_post_multiplicative(prep_query, nposts)
    else:
        raise ValueError("no valid embedding function")
    if isinstance(res_ids, str):
        res_ids = [res_ids]
    post_comment_pairs = get_pcp(res_ids)
    cvecs, comments, answerdistance = get_eligible_responses(post_comment_pairs, eval(embeddingfunction))
    expected_comment_vector = prep_query + answerdistance
    # lprint(comments)
    return best_comment(expected_comment_vector, cvecs, comments, nposts)

def get_pcp(ids):
    pcps = []
    for id in ids:
        pcp_raw = IDDATABASE.get(id)
        pcp = [[pcp_raw[3], pcp_raw[0] + " " + pcp_raw[4]], pcp_raw[5]]
        pcps.append(pcp)
    return pcps

def get_random_pcp(n):
    ids = list(IDDATABASE.keys())
    shuffle(ids)
    return get_pcp(ids[:n])

if __name__ == '__main__':
    query = "what is the best relic in the game?"
    query = "can you reccomend an algorithms for graph learning?"

    print("resulting respons additive:\n")
    res = get_best_response(query, "additive", nposts=1)
    if isinstance(res, str):
        print(res)
    else:
        lprint(res, extra_sep="")

    print("resulting respons multiplicative:\n")
    res = get_best_response(query, "multiplicative", nposts=2)
    lprint(res, extra_sep="")
