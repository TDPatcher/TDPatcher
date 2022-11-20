import os
import random
import pickle

random.seed(2022)

base_dir = '../function_prepare/data_pairs/'
data_samples = os.listdir(base_dir)

all_project_ids = []
for data_sample in data_samples: 
    project_id = data_sample.strip().split('#@')[0]
    all_project_ids.append( project_id )

test_dir = './test_set/'
test_samples = os.listdir(test_dir)
test_project_ids = []
for data_sample in test_samples:
    project_id = data_sample.strip().split('#@')[0]
    test_project_ids.append(project_id)

all_project_ids = list(set(all_project_ids))
test_project_ids = list(set(test_project_ids))
print("total projects:", len(all_project_ids))
print("test projects:", len(test_project_ids))

train_valid_project_ids = list(set(all_project_ids) - set(test_project_ids))
print("train valid projects:", len(train_valid_project_ids))

valid_project_ids = random.sample(train_valid_project_ids, 174)
print("valid projects:", len(valid_project_ids))
train_project_ids = list(set(train_valid_project_ids) - set(valid_project_ids))
print("train projects:", len(train_project_ids))

if not os.path.exists('./train_set'):
    os.makedirs('./train_set')

# if not os.path.exists('./test_set'):
#     os.makedirs('./test_set')

if not os.path.exists('./valid_set'):
    os.makedirs('./valid_set')

for e in data_samples:
    # print(e)
    project_id = e.strip().split('#@')[0]
    if project_id in valid_project_ids:
    # if e in test_samples:
        # src_path = './data_pairs/' + e 
        # tgt_path = './test_set/' + e
        # cp_cmd = "cp -r " + src_path + " " + tgt_path
        # os.system(cp_cmd)
        
        # if len(os.listdir(base_dir + e)) <= 50:
            # copy the sample to test_set
        src_path = base_dir + e 
        tgt_path = './valid_set/' + e
        cp_cmd = "cp -r " + src_path + " " + tgt_path
        os.system(cp_cmd)
    elif project_id in train_project_ids:
        # copy the sample to train_set 
        src_path = base_dir + e 
        tgt_path = './train_set/' + e
        cp_cmd = "cp -r " + src_path + " " + tgt_path
        os.system(cp_cmd)
    # break








