
import numpy as np
import pandas as pd
from general_easyness import lprint, writeformat_to_vec, minput, remove_special
from sklearn.metrics.pairwise import cosine_similarity
from terminaltables import AsciiTable
from operator import itemgetter
from prepare_string import prep, additive, multiplicative
from reddit_search import db_load
from random import shuffle




def load_real_vectors():
    adata = []
    mdata = []
    iddata = []
    for line in open("allreddit_va.csv", "r").readlines():
        if line[-1] == "\n":
            line = line[:-1]
        data = line.split(";")
        adata.append(writeformat_to_vec(data[0]))
        mdata.append(writeformat_to_vec(data[1]))
        iddata.append(data[2])
    data = [np.array(adata), np.array(mdata), iddata]
    return data




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

FALSECOUNTER = 0
def get_eligible_responses(post_comment_pairs, embeddingfunction, n):
    global FALSECOUNTER
    weights = []
    pvecs = []
    cvecs = []
    comments = []
    count = 0
    for pcp in post_comment_pairs:
        post = pcp[0]
        pvec = embeddingfunction(prep(post[1], verbose=False))
        continues = []
        try:
            if not pcp[1]:
                FALSECOUNTER += 1
                continue
            else:
                for i, c in enumerate(pcp[1]):
                    try:
                        pcp[1][i][1]
                    except:
                        continues.append(i)
                        FALSECOUNTER += 1
                        continue
        except:
            print(pcp)
            print("wtf")
            raise ValueError()

        for i, comment in enumerate(pcp[1]):
            if i in continues:
                continue
            if not comment:
                continue
            try:
                pvecs.append(pvec)
                weights.append(weightfunc(post[0], comment[0]))
                cvec = embeddingfunction(prep(comment[1], verbose=False))
                cvecs.append(cvec)
                comments.append(remove_special(comment[1]))
            except:
                print("pcp", pcp)
                print("\n\n\n\n\n\n\n\n")
                print("pcp1", pcp[1])
                print("\n\n\n\n\n\n\n\n")
                print("comment", comment)
                raise ValueError("actually mistook")
        count += 1
        if count == n:
            break

            # print(pcp)
            # print()
    wvec = np.array(weights)
    pvecs = np.array(pvecs)
    cvecs = np.array(cvecs)
    distances = difference_vector(pvecs, cvecs)
    answerdistance = distances * wvec[:, np.newaxis]
    answerdistance = np.sum(distances * wvec[:, np.newaxis], axis=0)

    print(answerdistance.shape)
    # print("wvec", wvec.shape)
    # print("distances", distances.shape)
    # print("answer distances", answerdistance.shape)
    return cvecs, comments, answerdistance

def get_best_response(query, embeddingfunction, nposts=5):
    pnposts = nposts*30
    prep_query = eval(embeddingfunction)(prep(query, verbose=False))
    if embeddingfunction == "additive":
        res_ids = best_post_additive(prep_query, pnposts)
    elif embeddingfunction == "multiplicative":
        res_ids = best_post_multiplicative(prep_query, pnposts)
    else:
        raise ValueError("no valid embedding function")
    if isinstance(res_ids, str):
        res_ids = [res_ids]
    post_comment_pairs = get_pcp(res_ids)
    cvecs, comments, answerdistance = get_eligible_responses(post_comment_pairs, eval(embeddingfunction), nposts)
    expected_comment_vector = prep_query + answerdistance
    # lprint(comments)
    print("exp comment", expected_comment_vector.shape)
    print(FALSECOUNTER)
    return best_comment(expected_comment_vector, cvecs, comments, 1)

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
