import os
import re
import json
from nltk.tokenize import sent_tokenize

def get_issue_id_regex():
    reexp = r'(#[\da-fA-F]+|[\da-fA-F]{30,})|(#-?[0-9]\d*)'
    return reexp

def get_brackets_regex():
    '''
    brackets regex used to delete brackets in commit messages
    ''' 
    reexp = r'^(\[.*?\]\s+(-\s+|)|\S+?(:|\s+-|\s+:)\s+|-\s+)' 
    return reexp

def remove_brackets(msg):
    '''
    Remove brackets in commit messages and try to get more vdo.
    '''
    bra_pattern = get_brackets_regex()
    new_msg = re.sub(bra_pattern, "", msg)
    return new_msg

def replace_issue_id(summary):
    '''
    replace commit id
    '''
    sum_pattern = get_issue_id_regex()
    new_summary = re.sub(sum_pattern, "<issue_id>", summary)
    return new_summary

def tokenize_by_punctuation(msg):
    '''
    '''
    punctuation = r'([!"#$%&\'()*+,-./:;<=>?@\[\]^`{|}~]|\\(?!n))'
    new_msg = re.sub(punctuation, r' \1 ', msg)
    id_regex = r'< (commit_id|issue_id) >'
    new_msg = re.sub(id_regex, r'<\1>', new_msg)
    new_msg = " ".join(re.sub(r'\n', ' <nl> ', new_msg).split())
    return new_msg

def tokenize_summary(summary):
    return tokenize_by_punctuation(summary)

def commit_processer(msg):
    ## get the first sentence
    ## remove issue id 
    ## Max length for summary. Default is 50
    msg = sent_tokenize(msg.strip().replace('\n', '. '))
    first_sent = msg[0]
    first_sent = replace_issue_id(first_sent)
    first_sent = remove_brackets(first_sent)
    first_sent = tokenize_summary(first_sent)
    return first_sent

base_dir = '../todo_diff/todo_diff/'
diff_todo_files = os.listdir(base_dir)

keywords = ['todo', 'to do']

with open('../Github/repos_sum/python_repos_info.json', 'r') as repos_info:
    repos_info = json.load(repos_info)


# with open('./todo_commits.out', 'w') as fout:
for f in diff_todo_files: 
    with open(base_dir + f, 'r') as diff_todo_file:
        diff_todo_dict = json.load(diff_todo_file)
    
    repoid = f.split('_')[0]
    print(f, repoid)
    with open('./todo_commits/' + repoid + '.commits', 'w') as fout:
        for k, v in diff_todo_dict.items(): 
            try:
                repo_file = v['repo_file']
                commit_diff = v['commit_diff']
                commit_now = v['commit_now']
                commit_parent = v['commit_parent']
                commit_msg = v['commit_msg']
                commit_msg_pro = commit_processer(commit_msg)
                commit_diff_pro = v['commit_diff_pro'].lower()

                repo_id = repo_file.rstrip('.json')
                repo_url = repos_info[repo_id]['repo_clone_url']
                target_url = repo_url.split('.git')[0] + '/commit/' + commit_now 

                if any(word in commit_diff_pro for word in keywords): 
                        fout.write(repo_file + '\t' \
                                    + commit_now + '\t' \
                                    + commit_parent + '\t' \
                                    + commit_msg_pro + '\t' \
                                    + commit_diff_pro + '\t' \
                                    + target_url)
                        fout.write('\n')

            except:
                continue
    # break

