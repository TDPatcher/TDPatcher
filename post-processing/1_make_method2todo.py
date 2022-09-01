import pickle
import os
import json
from pydriller import Repository

validate_fpath = '../pre-processing/validate_repo2commits.pickle'

with open(validate_fpath, 'rb') as handler:
    validate_repo2commits = pickle.load(handler)

print(len(validate_repo2commits))

def get_repo_parse_path(repo_id):
    repo_path = '../../Github/python_repos/' + repo_id 
    repo_name = os.listdir(repo_path)[0]
    repo_parse_path = repo_path + '/' + repo_name
    return repo_parse_path

def identify_todo_associated_method(changed_methods, todo_line_num):
    flex_lines = 2
    for method in changed_methods:
        # method_name = method.__dict__['name']
        # method_long_name = method.__dict__['long_name']
        # file_name = method.__dict__['filename']
        # parameters = method.__dict__['parameter'] 
        start_line = int(method.__dict__['start_line']) - flex_lines 
        end_line = int(method.__dict__['end_line']) + flex_lines 
        if int(todo_line_num) >= start_line and int(todo_line_num) <= end_line:
            return method
    else:
        return None
    pass

def get_method_info(changed_method):
    method_name = changed_method.__dict__['name']
    method_long_name = changed_method.__dict__['long_name']
    method_start_line = changed_method.__dict__['start_line']
    method_end_line = changed_method.__dict__['end_line']
    method_parameter = changed_method.__dict__['parameters']
    method_filename = changed_method.__dict__['filename']
    return method_name, method_long_name, method_parameter, method_start_line, method_end_line, method_filename

def get_target_url(repos_info, repo_id, commit):
    repo_url = repos_info[repo_id]['repo_clone_url']
    target_url = repo_url.split('.git')[0] + '/commit/' + commit
    return target_url

with open('./python_repos_info.json', 'r') as repos_info:
    repos_info = json.load(repos_info)

for k, v in validate_repo2commits.items():
    # print(k)
    # print(v)
    repo_id = k.split('.')[0]
    repo_parse_path = get_repo_parse_path(repo_id)
    print("==============")
    print(repo_parse_path)
    
    repo_method2todo = {}
    '''
    {
        key: method_name@@todo_line_num
        value:
        {
            'filename':
            'method_start_line':
            'method_end_line':
            'method_parameters':
            'method_long_name':
            'source_code':
            'source_code_before':
            'commmit':
            'target_url':
        }
    }
    '''
    try:
        for commit in Repository(repo_parse_path).traverse_commits():
            if commit.hash in v:
                for m in commit.modified_files:
                    # print(m.filename, ' has changed')
                    change_file = m.filename
                    commit_diff = m.diff
                    commit_diff_parsed = m.diff_parsed
                    commit_source_code = m.source_code
                    commit_source_code_before = m.source_code_before
                    # print(commit_diff_parsed)
                    parse_added = commit_diff_parsed['added']
                    changed_methods = m.changed_methods
                    for e in parse_added:
                        line_num = e[0]
                        line_detail = e[1].lower()
                        if "todo" in line_detail:
                            todo_comment = line_detail
                            todo_line_num = line_num
                            # identify the todo associated method 
                            todo_changed_method = identify_todo_associated_method(changed_methods, todo_line_num)
                            # print(todo_changed_method.__dict__)
                            # save method2todo  
                            if todo_changed_method is not None:
                                method_name, method_long_name, \
                                method_parameter, method_start_line, \
                                method_end_line, method_filename = get_method_info(todo_changed_method)
                                target_url = get_target_url(repos_info, repo_id, commit.hash)
                                print(target_url)
                                key = method_name + "@@" + str(todo_line_num)
                                print(key)
                                value = {}
                                value['filename'] = method_filename
                                value['method_start_line'] = method_start_line
                                value['method_end_line'] = method_end_line
                                value['method_parameters'] = method_parameter
                                value['method_name'] = method_name
                                value['method_long_name'] = method_long_name
                                value['source_code'] = commit_source_code
                                value['source_code_before'] = commit_source_code_before
                                value['commit'] = commit.hash
                                value['target_url'] = target_url
                                value['todo_comment'] = todo_comment
                                value['todo_line_num'] = todo_line_num
                                repo_method2todo[key] = value
                        
            else:
                continue
    except Exception as e:
        print("exception:", e)
        continue

    # print("length:", len(repo_method2todo))
    with open('./method2todo_pair/' + repo_id + '.pkl', 'wb') as handler:
        pickle.dump(repo_method2todo, handler)
    # with open()
    # break


