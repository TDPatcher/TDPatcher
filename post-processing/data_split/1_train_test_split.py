import os
import random
import pickle

random.seed(2022)

base_dir = '../function_prepare/data_pairs/'
data_samples = os.listdir(base_dir)


# split by project-wise
project_ids = []
for data_sample in data_samples:
    project_id = data_sample.strip().split('#@')[0]
    # print(project_id)
    project_ids.append( project_id )
    # break

unique_project_ids = list(set(project_ids))
print("total projects:", len(unique_project_ids))

test_samples = random.sample(unique_project_ids, int(len(unique_project_ids)*0.1) )
print("test projects:", len(test_samples))
# print(test_samples)
# test_samples = random.sample(data_samples, int(len(data_samples)*0.5) )

if not os.path.exists('./train_set'):
    os.makedirs('./train_set')

if not os.path.exists('./test_set'):
    os.makedirs('./test_set')

if not os.path.exists('./valid_set'):
    os.makedirs('./valid_set')

train_project_ids = []
for e in data_samples:
    # print(e)
    project_id = e.strip().split('#@')[0]
    if project_id in test_samples:
    # if e in test_samples:
        # src_path = './data_pairs/' + e 
        # tgt_path = './test_set/' + e
        # cp_cmd = "cp -r " + src_path + " " + tgt_path
        # os.system(cp_cmd)
        
        # if len(os.listdir(base_dir + e)) <= 50:
            # copy the sample to test_set
        src_path = base_dir + e 
        tgt_path = './test_set/' + e
        cp_cmd = "cp -r " + src_path + " " + tgt_path
        os.system(cp_cmd)
    else:
        # copy the sample to train_set 
        src_path = base_dir + e 
        tgt_path = './train_set/' + e
        cp_cmd = "cp -r " + src_path + " " + tgt_path
        os.system(cp_cmd)
        train_project_ids.append(project_id)
    # break

'''
valid_samples = random.sample(train_project_ids, len(test_samples))
for e in data_samples:
    project_id = e.strip().split('#@')[0]
    if project_id in valid_samples:
        src_path = './train_set/' + e 
        tgt_path = './valid_set/' + e
        mv_cmd = "mv " + src_path + " " + tgt_path
        os.system(cp_cmd)
'''
