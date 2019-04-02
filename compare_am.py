
import numpy as np
import pandas as pd
from general_easyness import lprint
from sklearn.metrics.pairwise import cosine_similarity
from terminaltables import AsciiTable
from operator import itemgetter

adata = np.array([np.array([i, i/2]) if i % 2 else np.array([i, i*2]) for i in range(6)])
mdata = np.array([np.array([i+1, (i*6)/2]) for i in range(6)])
iddata = ["a"+str(i) for i in range(6)]
data = [adata, mdata, iddata]


def load_real_vectors():
    df = pd.read_csv("reddit_va.csv", delimiter=",", header=None, names=["adata", "mdata", "id"])
    adata = df["adata"]
    mdata = df["mdata"]
    iddata = df["id"]
    data = [adata, mdata, iddata]
    return data



def load_id_database():
    titles = ["man goes fishing" if i % 2 else "man plays soccer" for i in range(6)]
    subreddit = "outdoor"
    upvote_ratios = [10/(4/(i % 2+1) for i in range(6)]
    scores = [10**i for i in range(6)]
    selftexts = ["bla"+str(i) for i in range(5)] + ["i love soccer and fishing"]
    comments = [["comment"+str(i) for i in range(j+1)] for j in range(6)]
    posts = [[titles[i], subreddit, upvote_ratios[i], scores[i], selftexts[i], comments[i] for i in range(6)]
    DB = {"a"+str(i) : posts[i] for i in range(6)}
    return DB

POSTDATABASE = load_real_vectors()
IDDATABASE = load_id_database()

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

def additive(something):
    """placeholder"""
    return something

def multiplicative(something):
    """placeholder"""
    return something

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
    res = lfunc(newcos, POSTDATABASE[0])[:,0,0]
    return itemgetter(*(find_n_max_inds(res, n).tolist()))(database[2])

def best_post_multiplicative(postembedding, n):
    newcos = makecosfunc(postembedding)
    res = lfunc(newcos, POSTDATABASE[1])[:,0,0]
    return itemgetter(*(find_n_max_inds(res, n).tolist()))(database[2])

def best_comment(expected_comment_vector, cvecs, comments):
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
        pvec = embeddingfunction(prep(post[1]))
        for comment in pcp[1]:
            weights.append(weightfunc(post[0], comment[0]))
            cvec = embeddingfunction(prep(comment[1]))
            pvecs.append(pvec)
            cvecs.append(cvec)
            comments.append(comment[1])
    wvec = np.array(weights)
    pvecs = np.array(p_vecs)
    cvecs = np.array(c_vecs)
    distances = difference_vector(p_vecs, c_vecs)
    weighted_dists = np.multiply(wdistances, wvec)
    answerdistance = np.sum(weightfunc, axis=1)
    return c_vecs, comments, answerdistance

def get_best_response(query, embeddingfunction, nposts=5):
    prep_query = eval(embeddingfunction)(prep(query))
    if embeddingfunction == "additive":
        res_ids = best_post_additive(prep_query, nposts)
    elif embeddingfunction == "multiplicative":
        res_ids = best_post_multiplicative(prep_query, nposts)
    post_comment_pairs = get_pcp(res_ids)
    cvecs, comments, answerdistance = get_eligible_responses(post_comment_pairs, eval(embeddingfunction))
    expected_comment_vector = eval(embeddingfunction)(prep_query) + answerdistance
    return best_comment(expected_comment_vector, cvecs, comments)

def get_pcp(ids):
    pcps = []
    for id in ids:
        pcp_raw = IDDATABASE.get(id)
        pcp = [[pcp_raw[3], pcp_raw[0] + " " + pcp_raw[4]], pcp_raw[5]]
        pcps.append(pcp)
    return pcps


print(get_best_response(query, "additive", nposts=3))

# testa = np.array([[data[0][i], data[1][i], data[2][i]] for i in range(len(data[0]))] , dtype=[('x', float), ('+', float), ('id', str)])
# print(res.argsort()[-3:])
# print(AsciiTable(testa).table)
