import pickle
import os

repos = os.listdir('./method2todo_pair')

for repo in repos:
    print(repo)
    repo_todo2method = {}
    with open('./method2todo_pair/' + repo, 'rb') as handler:
        repo_method2todo = pickle.load(handler) 

    if len(repo_method2todo) < 1: 
        continue 

    for k, v in repo_method2todo.items():
        # print(k)
        # print(v)
        method = k
        todo_comment = v['todo_comment'].strip().lower()
        if '#' in todo_comment or "'''" in todo_comment or '"""' in todo_comment:
            target_url = v['target_url']
            todo_file = v['filename'] 
            method_range = (v['method_start_line'], v['method_end_line']) 
            if todo_comment not in repo_todo2method: 
                key = todo_comment
                value = {}
                value['method_lst'] = [method]
                value['url_lst'] = [target_url]
                value['file_lst'] = [todo_file]
                value['method_range_lst'] = [method_range]
                repo_todo2method[key] = value
            else:
                repo_todo2method[todo_comment]['method_lst'].append(method)
                repo_todo2method[todo_comment]['url_lst'].append(target_url)
                repo_todo2method[todo_comment]['file_lst'].append(todo_file)
                repo_todo2method[todo_comment]['method_range_lst'].append(method_range)
                # break
     
    # print(repo_todo2method) 
    with open('./todo2method_pair/' + repo, 'wb') as handler:
        pickle.dump(repo_todo2method, handler)
    # break



