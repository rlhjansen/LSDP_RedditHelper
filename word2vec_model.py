""" download & check model data.

http://vectors.nlpl.eu/repository/11/6.zip
"""


import os

model_name = "model.bin"

if os.path.exists(os.path.join(os.path.curdir, model_name)):
    import gensim
    print(gensim.__version__)
    # Load Google's pre-trained Word2Vec model.

    model = gensim.models.KeyedVectors.load_word2vec_format('./model.bin', binary=True)
    # model.init_sims(replace=True)
    checkwords = "litigate,cat,house,livelihood,bitch,lasagna".split(",")
    # lprint(model.vocab)
    for word in checkwords:
        try:
            model.word_vec(word, use_norm=False)
            print(word + " works")
        except:
            print("rekt" + word + "u maek mistoken")
