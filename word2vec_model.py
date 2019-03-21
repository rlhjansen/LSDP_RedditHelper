
import os

model_name_zipped = "GoogleNews-vectors-negative300.bin.gz"
model_name = "GoogleNews-vectors-negative300.bin"

print(os.path.exists(os.path.join(os.path.curdir, model_name_zipped)))
print(os.path.exists(os.path.join(os.path.curdir, model_name_zipped)))

if not os.path.exists(os.path.join(os.path.curdir, model_name_zipped)):
    from urllib.request import urlretrieve
    # Download the file from `url` and save it locally under `file_name`:
    download_url = "https://github.com/mmihaltz/word2vec-GoogleNews-vectors/raw/master/GoogleNews-vectors-negative300.bin.gz"
    urlretrieve(download_url, model_name_zipped)


if not os.path.exists(os.path.join(os.path.curdir, model_name)):
    import gzip
    import shutil
    with gzip.open(model_name_zipped, 'rb') as f_in, open(model_name, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


if os.path.exists(os.path.join(os.path.curdir, model_name)):
    import gensim
    print(gensim.__version__)
    # Load Google's pre-trained Word2Vec model.

    model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
    # model.init_sims(replace=True)
    print(model.word_vec('office', use_norm=False))
