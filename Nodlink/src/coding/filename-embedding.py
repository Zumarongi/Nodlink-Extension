from gensim.models import FastText
from gensim.models.doc2vec import TaggedDocument
from argparse import ArgumentParser
import re
import pandas as pd
from nostril import nonsense
import string
from tools import sanitize_string


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--epoch",type = int,default=100)
    parser.add_argument("--e",type = int, default=256)
    parser.add_argument("--d",type = str, default='win10')
    args = parser.parse_args()
    epoch = args.epoch
    dataset = args.d
    embedding_size = args.e
    input_file1 = dataset + '/filename.txt'
    input_file2 = dataset + '/cmdline.txt'
    pathname = []
    corpus = []
    f1 = open(input_file1,'r',encoding='utf-8')
    while True:
        line = f1.readline()
        if not line:
            break
        if line == '\n' or line == 'None' or line == 'none':
            continue
    
        splitline = sanitize_string(line)#处理，如nodlink：V.B
        # print(splitline)

        corpus.append(splitline)
    f2 = open(input_file2,'r',encoding='utf-8')
    while True:
        line = f2.readline()
        if not line:
            break
        if line == '\n' or line == 'None' or line == 'none':
            continue
    
        splitline = sanitize_string(line)#处理，如nodlink：V.B
        # print(splitline)

        corpus.append(splitline)

    print('start embedding')
    model = FastText(min_count = 5, vector_size=embedding_size, workers= 30, alpha=0.01,window=3,negative=5)
    model.build_vocab(corpus)
    model.train(corpus,epochs=epoch,total_examples=model.corpus_count)
    model.save(dataset + '/filepath-embedding.model')
# model = word2vec.Word2Vec.load('line-embedding-cadets.model')

# print(model.wv['<unk>'])
# model = Doc2Vec.load('cmdline.model')

