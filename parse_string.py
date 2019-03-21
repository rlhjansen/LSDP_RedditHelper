""" This is a file which demonstrates function calls for the sentence/post/comment vectors

"""

from prepare_string import additive, multiplicative, prep
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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
    try:
        return cosine_similarity(single, others)
    except:
        return cosine_similarity(single.reshape(1,-1), others)

def difference_vector(post, comment):
    """ computes the difference in meaning space between two vectors
    """
    return post - comment

testQ = "Why did the chicken cross the road?"
testA = "because donald trump is a chicken and the road is code for america" + \
        "getting double crossed"

adQ, adA = additive(prep(testQ)), additive(prep(testA))
muQ, muA = multiplicative(prep(testQ)), multiplicative(prep(testA))


sim = cosine_sym_single(adQ,adA)
print(sim)
sim = cosine_sym_single(adQ,muA)
print(sim)
sim = cosine_sym_single(muQ,adA)
print(sim)
sim = cosine_sym_single(muQ,muA)
print(sim)
sim = cosine_sym_multi(np.vstack([adQ, muQ]), np.vstack([adA, muA]))
print(sim)
