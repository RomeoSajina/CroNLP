import argparse
from gensim import utils
from gensim.models import FastText, Word2Vec

import logging
logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO, filename="info.log")
logger = logging.getLogger(__name__)


class WikiCorpus(object):
    """An interator that yields sentences (lists of str)."""

    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):

        with open(self.file_path, "r") as fh:
            text = fh.read()
            text = [x for x in text.split("\n") if len(x) > 0]

        for line in text:
            yield utils.simple_preprocess(line)


def save(name, words, vectors):

    import io
    import os
    os.makedirs("./weights", exist_ok=True)
    out_v = io.open("./weights/{0}_vec.tsv".format(name), "w", encoding="utf-8")
    out_m = io.open("./weights/{0}_meta.tsv".format(name), "w", encoding="utf-8")

    for i in range(len(vectors)):
        vec = vectors[i]
        word = words[i]
        out_m.write(word + "\n")
        out_v.write("\t".join([str(x) for x in vec]) + "\n")
    out_v.close()
    out_m.close()


def eval(args):
    text, test = args.text, args.test

    logger.info("======== Start evaluation on ({0}, {1}) =========".format(text, test))

    sentences = WikiCorpus(text)

    logger.info("Word2Vec (skip-gram):")
    logging.root.setLevel(logging.ERROR)
    word2vec_skipgram = Word2Vec(sentences=sentences, sg=1, size=100, min_count=1, iter=100, window=5)
    logging.root.setLevel(logging.INFO)
    word2vec_skipgram.wv.evaluate_word_analogies(test)

    logger.info("Word2Vec (cbow):")
    logging.root.setLevel(logging.ERROR)
    word2vec_cbow = Word2Vec(sentences=sentences, sg=0, size=100, min_count=1, iter=100, window=5)
    logging.root.setLevel(logging.INFO)
    word2vec_cbow.wv.evaluate_word_analogies(test)

    logger.info("FastText (skip-gram):")
    logging.root.setLevel(logging.ERROR)
    fasttext_skipgram = FastText(sentences, sg=1, size=100, min_count=1, iter=100, window=5)
    logging.root.setLevel(logging.INFO)
    fasttext_skipgram.wv.evaluate_word_analogies(test)

    logger.info("FastText (cbow):")
    logging.root.setLevel(logging.ERROR)
    fasttext_cbow = FastText(sentences, sg=0, size=100, min_count=1, iter=100, window=5)
    logging.root.setLevel(logging.INFO)
    fasttext_cbow.wv.evaluate_word_analogies(test)

    logger.info("GloVe (cbow):")
    logging.root.setLevel(logging.ERROR)
    from glove import GloVeModel
    glove = GloVeModel(embedding_size=100, context_size=5, min_occurrences=1)
    glove.fit_to_corpus(sentences)
    glove.train(num_epochs=100)

    # Short workaround
    tmp = Word2Vec(sentences=sentences, size=100, min_count=1, iter=0, window=5)
    for x in glove.words:
        tmp.wv[x] = glove.embedding_for(x)

    del tmp.wv.vectors_norm
    logging.root.setLevel(logging.INFO)
    tmp.wv.evaluate_word_analogies(test)

    if args.save:
        print("Saving embeddings...")
        save("word2vec_skipgram", word2vec_skipgram.wv.vectors, word2vec_skipgram.wv.index2word)
        save("word2vec_cbow", word2vec_cbow.wv.vectors, word2vec_cbow.wv.index2word)
        save("fasttext_skipgram", fasttext_skipgram.wv.vectors, fasttext_skipgram.wv.index2word)
        save("fasttext_cbow", fasttext_cbow.wv.vectors, fasttext_cbow.wv.index2word)
        save("glove", tmp.wv.vectors, tmp.wv.index2word)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="Corpus file", default="./data/output.txt")
    parser.add_argument("--test", help="Word analogies test file", default="./data/test.txt")
    parser.add_argument("--save", help="Save embeddings", action="store_true")
    args = parser.parse_args()

    eval(args)
