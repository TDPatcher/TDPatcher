import os
import pickle

with open('./multi_todo2method.pkl', 'rb') as handler:
    multi_todo2method = pickle.load(handler)

print("length of multi_todo2method:", len(multi_todo2method))

base_dir = './multi_todo_files/'

for e in multi_todo2method:
    repo = e[0]
    todo_comment = e[1]
    method_lst = e[2]
    url_lst = e[3]
    file_lst = e[4]
    method_range_lst = e[5]
    
    repo_id = repo.split('.')[0] 
    for url, method, filename in zip(url_lst, method_lst, file_lst):
        commit = url.split('/')[-1]
        print(repo_id, commit, method, filename)
        print(url)
        
        tgt_dir = repo_id + '/' + commit + '##' + method
        if not os.path.exists('./multi_todo_files/' + tgt_dir):
            os.makedirs(base_dir + tgt_dir)
        
        with open('./method2todo_pair/' + repo, 'rb') as handler:
            repo_method2todo = pickle.load(handler)
        
        source_code = repo_method2todo[method]['source_code']
        with open('./multi_todo_files/' + tgt_dir + '/' + filename, 'w') as fout:
            fout.write( source_code )

        # print(source_code)
    # print(tgt_dir)
    # break
print("Finished!")


