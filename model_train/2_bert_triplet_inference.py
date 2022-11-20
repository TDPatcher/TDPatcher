from sentence_transformers import SentenceTransformer, LoggingHandler, InputExample
from sentence_transformers import SentenceTransformer, SentencesDataset, LoggingHandler, losses
from sentence_transformers import models, util, datasets, evaluation, losses
import logging
import os
import gzip
import math
import pickle
from torch.utils.data import DataLoader
from datetime import datetime

def load_samples(fpath):
    samples = []
    with open(fpath, 'r') as f:
        for line in f:
            samples.append(line.strip())
    return samples


model = SentenceTransformer('./checkpoint/17820')
# model = SentenceTransformer('./output/roberta-base-2022-07-25_00-35-24')

# sentences = ['This framework generates embeddings for each input sentence', \
#              'Sentences are passed as a list of string.',\
#              'The quick brown fox jumps over the lazy dog.']

anchor_samples = load_samples('./anchor_samples.validate')
print("anchor_samples:", len(anchor_samples))
anchor_embeddings = model.encode(anchor_samples)
print("anchor_embeddings:", anchor_embeddings.shape)

positive_samples = load_samples('./positive_samples.validate')
print("positive_samples:", len(positive_samples))
positive_embeddings = model.encode(positive_samples)
print("positive_embeddings:", positive_embeddings.shape)

negative_samples = load_samples('./negative_samples.validate')
print("negative_samples:", len(negative_samples))
negative_embeddings = model.encode(negative_samples)
print("negative_embeddings:", negative_embeddings.shape)

with open('./anchor_embeddings.pkl', 'wb') as handler:
    pickle.dump(anchor_embeddings, handler)

with open('./positive_embeddings.pkl', 'wb') as handler:
    pickle.dump(positive_embeddings, handler)

with open('./negative_embeddings.pkl', 'wb') as handler:
    pickle.dump(negative_embeddings, handler)

