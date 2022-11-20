import pickle

with open('./similarity_scores.pkl', 'rb') as handler:
    similarity_scores = pickle.load(handler)

threshold = 0.8

def measure_threshold( threshold ):
    correct_case = 0 
    for e in similarity_scores:
        if e[0] >= threshold and e[1] < threshold:
            correct_case += 1
    return (correct_case*1.0) / len(similarity_scores)

for threshold in [0.1, 0.2, 0.4, 0.5, 0.55, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64,  0.65, 0.7, 0.75, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]:
    print(threshold)
    print(measure_threshold(threshold))

