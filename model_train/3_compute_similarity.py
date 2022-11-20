import pickle
from numpy import dot
from numpy.linalg import norm
from scipy.spatial import distance

with open('./anchor_embeddings.pkl', 'rb') as handler:
    anchor_embeddings = pickle.load(handler)

with open('./positive_embeddings.pkl', 'rb') as handler:
    positive_embeddings = pickle.load(handler)

with open('./negative_embeddings.pkl', 'rb') as handler:
    negative_embeddings = pickle.load(handler)

def cos_sim(a, b):
    return dot(a, b)/(norm(a)*norm(b))

# print(len(anchor_embeddings))
similarity_scores = []
for i in range(len(anchor_embeddings)):
    anchor_vector = anchor_embeddings[i]
    positive_vector = positive_embeddings[i] 
    negative_vector = negative_embeddings[i]
    # print(type(anchor_vector), anchor_vector.shape)
    pos_cos_sim = 1 - distance.cosine(anchor_vector, positive_vector)
    # pos_cos_sim = 1 - distance.euclidean(anchor_vector, positive_vector)
    # pos_cos_sim = cos_sim(anchor_vector, positive_vector)

    neg_cos_sim = 1 - distance.cosine(anchor_vector, negative_vector)
    # neg_cos_sim = 1 - distance.euclidean(anchor_vector, negative_vector)
    # neg_cos_sim = cos_sim(anchor_vector, negative_vector)
    print(pos_cos_sim, neg_cos_sim)
    similarity_scores.append( (pos_cos_sim, neg_cos_sim) )
    # break

with open('./similarity_scores.pkl', 'wb') as handler:
    pickle.dump(similarity_scores, handler)


