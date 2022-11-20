import os
import pickle

base_dir = './train_set/'
# base_dir = './data_pairs/'
data_pairs = os.listdir(base_dir)

def get_data_pair_info( data_pair ):
    '''
    '''
    data_pair_info = {}
    all_files = os.listdir( base_dir + data_pair )
    todo_files = []
    notodo_files = []
    for f in all_files:
        if f.endswith('.td.pkl'):
            todo_files.append(f) 
        elif f.endswith('.ntd.pkl'):
            notodo_files.append(f)
    key = data_pair 
    value = {}
    value['todo_files'] = todo_files
    value['notodo_files'] = notodo_files
    data_pair_info[key] = value
    return data_pair_info 

def prepare_positive_pair( data_pair_info ):
    '''
    '''
    for k, v in data_pair_info.items():
        base_dir = k
        todo_files = v['todo_files'] 
        if len(todo_files) == 2:   
            todo_1 = base_dir + '/' + todo_files[0]   
            todo_2 = base_dir + '/' + todo_files[1] 
            return (todo_1, todo_2) 
    return None


positive_samples = []

for data_pair in data_pairs:
    # print(data_pair)
    data_pair_info = get_data_pair_info( data_pair )
    # print(data_pair_info)
    positive_pair = prepare_positive_pair( data_pair_info )

    if positive_pair:
        # print( positive_pair )
        positive_samples.append( positive_pair )
        # negative_pairs = prepare_negative_pairs( data_pair_info )
        # for negative_pair in negative_pairs:
            # print(negative_pair)
        #     negative_samples.append( negative_pair )
    # break

with open('./positive_samples.train.pkl', 'wb') as handler:
    pickle.dump(positive_samples, handler)

# with open('./negative_samples.pkl', 'wb') as handler:
#     pickle.dump(negative_samples, handler)

