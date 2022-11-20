import ast
import os
import pickle
import json
import astunparse
import asttokens
import random

random.seed(7)

with open('./positive_samples.train.pkl', 'rb') as handler:
    positive_samples = pickle.load(handler)

def load_function(fpath):
    '''
    '''
    with open(fpath, 'rb') as handler:
        function = pickle.load(handler)
    return function

def get_function_source_code( todo_function ):
    source_code = [] 
    for k, v in todo_function.items():
        function_name = k
        source_code_lines = v['source_code']
        for e in source_code_lines:
            if e[1].strip() == '': 
                continue 
            elif e[1].strip().startswith('#'):
                continue
            elif e[1].strip().startswith('"""'):
                continue
            elif e[1].strip().startswith("'''"):
                continue
            else:
                source_code.append(e)
    return source_code 

def get_base_lineno( todo_function ):
    base_lineno = 1
    for k, v in todo_function.items():
        base_lineno = v['source_code'][0][0] - 1
        return base_lineno
    return base_lineno

def get_todo_comment( todo_function ):
    for k, v in todo_function.items():
        todo_line = v['todo_comment']
        todo_lineno = int(todo_line[0])
        todo_comment = todo_line[1].strip()
        return todo_lineno, todo_comment
    return None

def get_pre_todo_context( source_code, todo_lineno):
    line_limit = 10 
    if todo_lineno - line_limit < source_code[0][0]:
        start_lineno =  source_code[0][0]
    else:
        start_lineno = todo_lineno - line_limit 
    pre_todo_context = []
    for e in source_code:
        if e[0] >= start_lineno and e[0] < todo_lineno:
            pre_todo_context.append( e )
    return pre_todo_context[-2:]           

def get_post_todo_context( source_code, todo_lineno):
    line_limit = 10  
    if todo_lineno + line_limit > source_code[-1][0]:
        end_lineno = source_code[-1][0]
    else:
        end_lineno = todo_lineno + line_limit 
    after_todo_context = []
    for e in source_code:
        if e[0] > todo_lineno and e[0] <= end_lineno:
            after_todo_context.append( e )
    return after_todo_context[:3]           
         

def get_line_range(node, base_lineno):
    min_lineno = node.lineno
    max_lineno = node.lineno
    for node in ast.walk(node):
        if hasattr(node, "lineno"):
            min_lineno = min(min_lineno, node.lineno)
            max_lineno = max(max_lineno, node.lineno)
    return (min_lineno + base_lineno, max_lineno + 1 + base_lineno)

def get_merged_context(pre_context, post_context):
    context = []
    for e in pre_context:
        context.append(e) 
    for e in post_context:
        context.append(e)
    merged_context = "".join(context)
    return merged_context

def get_todo_statement(pre_context, post_context):
    todo_statement = ""
    if len(post_context) > 0:
        todo_statement = post_context[0]
        return todo_statement, pre_context, post_context[1:]
    elif len(pre_context) > 0:
        todo_statement = pre_context[-1]
        return todo_statement, pre_context[:-1], post_context
    return todo_statement, pre_context, post_context
        
def get_all_ntd_files( fpath ):
    
    ntd_files = []
    all_files = os.listdir(fpath)
    for f in all_files:
        if f.endswith('.ntd.pkl'):
            ntd_files.append(f)
    return ntd_files

# data_pairs = os.listdir('./data_pairs/')
# with open('./positive_samples.pkl', 'rb') as handler:
#     positive_samples = pickle.load(handler)
# anchor_positive_samples = {}
# anchor_negative_samples = {}
anchor_pos_neg_samples = {}

for i, e in enumerate(positive_samples[:]):
    print(e)
    anchor_todo_fpath = './train_set/' + e[0]
    positive_todo_fpath = './train_set/' + e[1]
    
    # print(anchor_todo_fpath)
    # print(positive_todo_fpath)
    anchor_todo_fname = e[0].split('/')[1].split('.')[0]
    positive_todo_fname = e[1].split('/')[1].split('.')[0]

    anchor_todo_dir = '/'.join(anchor_todo_fpath.split('/')[:-1])
    print(anchor_todo_dir)
    ntd_files = get_all_ntd_files( anchor_todo_dir )

    if len(ntd_files) > 0:
        # selected_ntd_file = random.choice(ntd_files)
        selected_ntd_file = ntd_files[0]
        negative_todo_fpath = anchor_todo_dir + '/' + selected_ntd_file 
        negative_todo_fname = selected_ntd_file.split('.')[0]
    else:
        print("+=+=+=+=")
        negative_todo_fpath = anchor_todo_dir + '/' + positive_todo_fname + '.td.pkl' 
        negative_todo_fname = positive_todo_fname 
    # print("negative_todo_fpath:", negative_todo_fpath, negative_todo_fname)

    anchor_todo_function = load_function( anchor_todo_fpath )
    anchor_todo_src_code = get_function_source_code(anchor_todo_function) 
    anchor_todo_lineno, anchor_todo_comment = get_todo_comment( anchor_todo_function )
    anchor_pre_todo_context = get_pre_todo_context( anchor_todo_src_code, anchor_todo_lineno)
    anchor_post_todo_context = get_post_todo_context( anchor_todo_src_code, anchor_todo_lineno)
    # update
    anchor_todo_statement, \
    anchor_pre_context, \
    anchor_post_context = get_todo_statement(anchor_pre_todo_context, anchor_post_todo_context)

    # anchor_merged_context = get_merged_context(anchor_pre_todo_context, anchor_post_todo_context)
    # print(anchor_todo_src_code)
    print("========================================")
    print("anchor function name:", anchor_todo_fname)
    print("anchor todo commet:", anchor_todo_comment)
    print("anchor todo lineno:", anchor_todo_lineno)
    print("anchor todo statement:", anchor_todo_statement)
    print("anchor pre_context:", anchor_pre_context)
    print("anchor post_context:", anchor_post_context)


    positive_todo_function = load_function( positive_todo_fpath )
    positive_todo_src_code = get_function_source_code(positive_todo_function) 
    positive_todo_lineno, positive_todo_comment = get_todo_comment( positive_todo_function )
    positive_pre_todo_context = get_pre_todo_context( positive_todo_src_code, positive_todo_lineno)
    positive_post_todo_context = get_post_todo_context( positive_todo_src_code, positive_todo_lineno)
    positive_todo_statement, \
    positive_pre_context, \
    positive_post_context = get_todo_statement(positive_pre_todo_context, positive_post_todo_context)

    # print(anchor_todo_src_code)
    print("========================================")
    print("positive function name:", positive_todo_fname)
    print("positive todo commet:", positive_todo_comment)
    print("positive todo lineno:", positive_todo_lineno)
    print("positive todo statement:", positive_todo_statement)
    print("positive pre_context:", positive_pre_context)
    print("positive post_context:", positive_post_context)

    negative_todo_function =  load_function( negative_todo_fpath )
    negative_todo_src_code = get_function_source_code(negative_todo_function) 
    # print(negative_todo_src_code)
    negative_todo_lineno = int(random.choice(negative_todo_src_code)[0])
    negative_todo_comment = anchor_todo_comment
    negative_pre_todo_context = get_pre_todo_context( negative_todo_src_code, negative_todo_lineno)
    negative_post_todo_context = get_post_todo_context( negative_todo_src_code, negative_todo_lineno)
    negative_todo_statement, \
    negative_pre_context, \
    negative_post_context = get_todo_statement(negative_pre_todo_context, negative_post_todo_context)
    # print(anchor_todo_src_code)
    print("========================================")
    print("negative function name:", negative_todo_fname)
    print("negative todo commet:", negative_todo_comment)
    print("negative todo lineno:", negative_todo_lineno)
    print("negative todo statement:", negative_todo_statement)
    print("negative pre_context:", negative_pre_context)
    print("negative post_context:", negative_post_context)
    
    key = i
    value = {}
    value['anchor_function_name'] = anchor_todo_fname
    value['anchor_todo_comment'] = anchor_todo_comment
    value['anchor_todo_lineno'] = anchor_todo_lineno
    value['anchor_todo_statement'] = anchor_todo_statement
    value['anchor_pre_context'] = anchor_pre_context
    value['anchor_post_context'] = anchor_post_context

    value['positive_function_name'] = positive_todo_fname
    value['positive_todo_comment'] = positive_todo_comment
    value['positive_todo_lineno'] = positive_todo_lineno
    value['positive_todo_statement'] = positive_todo_statement
    value['positive_pre_context'] = positive_pre_context
    value['positive_post_context'] = positive_post_context

    value['negative_function_name'] = negative_todo_fname
    value['negative_todo_comment'] = negative_todo_comment
    value['negative_todo_lineno'] = negative_todo_lineno 
    value['negative_todo_statement'] = negative_todo_statement 
    value['negative_pre_context'] = negative_pre_context  
    value['negative_post_context'] = negative_post_context 

    anchor_pos_neg_samples[key] = value


with open('./anchor_positive_negative_samples.pkl', 'wb') as handler:   
    pickle.dump(anchor_pos_neg_samples, handler)

