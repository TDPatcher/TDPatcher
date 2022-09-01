import pickle
import os

repos = os.listdir('./todo2method_pair/')
unique_file_cnt = 0

with open('./multi_todo2method.out', 'w') as fout1, \
    open('./single_todo2method.out', 'w') as fout2:

    multi_todo2method_lst = []
    single_todo2method_lst = []

    for repo in repos:
        print(repo)
        with open('./todo2method_pair/' + repo, 'rb') as handler:
            repo_todo2method = pickle.load(handler)
        
        for k, v in repo_todo2method.items():
            # print(k)
            # print(v)
            todo_comment = k
            method_lst = v['method_lst']
            url_lst = v['url_lst']
            file_lst = v['file_lst']
            method_range_lst = v['method_range_lst']
            unique_method = []
            unique_commit = []
            unique_file = []

            if len(todo_comment.split(' ')) < 3:
                continue
            
            for e in method_lst: 
                method_name = e.split('@@')[0]
                unique_method.append(method_name)
                # unique_method.append(e)
            unique_method = list(set(unique_method))

            for e in url_lst:
                commit = e.split('/')[-1]
                unique_commit.append(commit)
            unique_commit = list(set(unique_commit))

            for e in file_lst:
                filename = e
                unique_file.append(filename)
            unique_file = list(set(unique_file))

            
            if len(method_lst) > 1:

                if len(unique_method) == 1 and len(unique_commit) > 1: 
                    continue 

                if len(unique_file) == 1:
                    unique_file_cnt += 1

                multi_todo2method_lst.append( (repo, todo_comment, method_lst, url_lst, file_lst, method_range_lst) )
                fout1.write(repo + '\t' + todo_comment + '\t' + str(method_lst) + '\t' + str(url_lst) + '\t' + str(method_range_lst) + '\t' + str(file_lst))      
                fout1.write('\n')
            else:
                single_todo2method_lst.append( (repo, todo_comment, method_lst, url_lst, file_lst, method_range_lst) )
                fout2.write(repo + '\t' + todo_comment + '\t' + str(method_lst) + '\t' + str(url_lst) + '\t' + str(method_range_lst) + '\t' + str(file_lst))      
                fout2.write('\n')
                pass


    with open('./multi_todo2method.pkl', 'wb') as handler:
        pickle.dump(multi_todo2method_lst, handler)

    with open('./single_todo2method.pkl', 'wb') as handler:
        pickle.dump(single_todo2method_lst, handler)

print( unique_file_cnt )
print( unique_file_cnt*1.0 / len(multi_todo2method_lst) )
# break

