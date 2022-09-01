import os
import pickle

def label_sample( functions ): 
    td_functions = []
    ntd_functions = [] 
    for f in functions: 
        if f.endswith('.td.pkl'):
            td_functions.append(f)
        elif f.endswith('.ntd.pkl'):
            ntd_functions.append(f)

    # print(len(td_functions))
    if len(td_functions) < 2:
        return None
    # assert len(td_functions) == 2
    anchor_td = td_functions[0]
    pos_td = td_functions[1]

    sample_result = []
    sample_result.append( (anchor_td, pos_td, 1) )
    for f in ntd_functions: 
        sample_result.append( (anchor_td, f, 0) )    
    return sample_result 


all_test_samples = os.listdir('./test_set') 

evaluation_set = []
for test_sample in all_test_samples:
    # print(e)
    sample_path = './test_set/' + test_sample 
    print(sample_path)
    all_functions = os.listdir(sample_path)
    # print(all_functions)
    sample_result = label_sample( all_functions ) 

    if sample_result is None:
        continue 
    for e in sample_result: 
        f0_path = sample_path + '/' + e[0]
        f1_path = sample_path + '/' + e[1]
        label = e[2]
        evaluation_set.append( (f0_path, f1_path, label) )
    # break

with open('./test_set.pkl', 'wb') as handler:
    pickle.dump(evaluation_set, handler)  

# print("evaluation_set:", len(evaluation_set))
