import pickle
import os

def load_evaluation_set():
    with open('./test_set.pkl', 'rb') as handler:
        evaluation_set = pickle.load(handler) 
    return evaluation_set   

def get_function(fpath):
    with open(fpath, 'rb') as handler:
        function = pickle.load(handler)
    return function 

def get_function_source_code(function):
    source_code = []
    for k, v in function.items():
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

def get_todo_comment( todo_function ):
    for k, v in todo_function.items():    
        todo_line = v['todo_comment']
        # todo_lineno = int(todo_line[0])
        todo_comment = todo_line[1].strip()
        return todo_comment
    return None
        
def get_todo_lineno( todo_function ):
    for k, v in todo_function.items():    
        todo_line = v['todo_comment']
        todo_lineno = int(todo_line[0])
        return todo_lineno
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

def get_todo_code_block(pre_context, post_context):
    todo_statement = ""
    if len(post_context) > 0:
        todo_statement = post_context[0]
        return todo_statement, pre_context, post_context[1:]
    elif len(pre_context) > 0:
        todo_statement = pre_context[-1]
        return todo_statement, pre_context[:-1], post_context
    return todo_statement, pre_context, post_context     

def prepare_model_input(function_name, todo_comment, statement, pre_context, post_context):
    # print("statement:", statement)
    # print(":", statement)
    context = []
    context.append(function_name)
    for e in pre_context:
        context.append(e[1].strip())
    for e in post_context:
        context.append(e[1].strip())
    context = " ".join(context)
    todo_comment_statement = todo_comment.strip().lower() + " </s> "  + statement[1].strip().lower()
    return todo_comment_statement, context

def get_block_range(e, pre_context, post_context):
    '''
    '''
    block_range = [] 
    block_range.append(int(e[0]))
    for e in pre_context:
        block_range.append(int(e[0]))
    for e in post_context:
        block_range.append(int(e[0]))
    min_lineno = min(block_range) 
    max_lineno = max(block_range)
    return (min_lineno, max_lineno)

def get_candidate_code_blocks(function_src_code):
    '''
    code_blocks:{
        key:
        value: {
            "statement":
            "pre_context":
            "post_context":
        }
    }
    '''
    code_blocks = {}
    for i, e in enumerate(function_src_code):
        # print(e)
        statement = e # e[1].strip().lower() 
        pre_context = get_pre_todo_context(function_src_code, e[0])
        post_context = get_post_todo_context(function_src_code, e[0])[:2]
        block_range = get_block_range(e, pre_context, post_context)
        # print("=====================")
        # print("statement:", statement)
        # print("pre context:", pre_context)
        # print("post context:", post_context)
        # print("line range:", block_range)
        key = str(block_range[0]) +  '_' + str(block_range[1])
        # print(key)
        value = {}
        value['statement'] = statement
        value['pre_context'] = pre_context 
        value['post_context'] = post_context
        code_blocks[key] = value 
    return code_blocks 

def get_todo_info(function):
    for k, v in function.items():
        if v['todo_comment'][1]:
            todo_lineno = int(v['todo_comment'][0]) 
            # print(v['todo_comment'])
            todo_comment = v['todo_comment'][1].strip().lower()
        else:
             todo_lineno = -1
             todo_comment = "None"
    return todo_lineno, todo_comment      
    

evaluation_set = load_evaluation_set()
print(len(evaluation_set))

for e in evaluation_set:
    print(e)
    f0_path = e[0]
    f1_path = e[1]
    label = e[2]
    f0_function_name = e[0].split('/')[3].split('.')[0].split('@')[0]
    if '@' in e[1]:
        f1_function_name = e[1].split('/')[3].split('.')[0].split('@')[0]
    else:
        f1_function_name = e[1].split('/')[3].split('.')[0]

    eval_dir = './test_set_prepared/' + e[0].split('/')[2] + '/'
    if not os.path.exists(eval_dir):
        os.makedirs(eval_dir)
    
    with open(eval_dir + f1_function_name + '.test.' + str(label), 'w') as fout:
        try:
            fout.write(str(label) + '\n')
            f0 = get_function(f0_path)
            # print(f0)
            f0_src_code = get_function_source_code(f0)
            # print(f0_src_code)

            f0_todo_comment = get_todo_comment( f0 )
            f0_todo_lineno = get_todo_lineno( f0 )
            # print(f0_function_name, f0_todo_comment, f0_todo_lineno)
            f0_pre_todo_context = get_pre_todo_context(f0_src_code, f0_todo_lineno)
            f0_post_todo_context = get_post_todo_context(f0_src_code, f0_todo_lineno)

            f0_statement, \
            f0_pre_context, f0_post_context = get_todo_code_block(f0_pre_todo_context, f0_post_todo_context)
            # print("f0_statement:", f0_statement)
            # print("f0_pre_context:", f0_pre_context)
            # print("f0_post_context:", f0_post_context)

            f0_input = prepare_model_input(f0_function_name, \
                                           f0_todo_comment, \
                                           f0_statement, \
                                           f0_pre_context, \
                                           f0_post_context)

            f0_todo_info = get_todo_info(f0)
            fout.write(f0_path + '\n')
            fout.write(str(f0_todo_info[0]) + '\n')
            fout.write(str(f0_todo_info[1]) + '\n')
            # print("f0_todo_info:", f0_todo_info)
            # print("f0_todo_input:", f0_input)
            
            f1 = get_function(f1_path)
            # print(f1)
            f1_src_code = get_function_source_code(f1)
            # print(f1_src_code)
            f1_todo_info = get_todo_info(f1)
            # print(f1_todo_info)
            fout.write(f1_path + '\n') 
            fout.write(str(f1_todo_info[0]) + '\n')
            fout.write(str(f1_todo_info[1]) + '\n')
            

            f1_block_inputs = []
            candidate_code_blocks = get_candidate_code_blocks(f1_src_code)
            for k, v in candidate_code_blocks.items():
                f1_statement = v['statement']
                f1_pre_context = v['pre_context']
                f1_post_context = v['post_context']
                f1_block_input = prepare_model_input(f1_function_name, \
                                                       f0_todo_comment, \
                                                       f1_statement, \
                                                       f1_pre_context, \
                                                       f1_post_context)

                fout.write(str(k) + '\t' + f0_input[0] + '\t' + f0_input[1] + '\t'
                           + f1_block_input[0] + '\t' + f1_block_input[1] ) 
                fout.write('\n')

        except Exception as e:
            print(e)
            continue

        # f1_src_code = get_function_source_code(f1)
        # print(f1_src_code)

    # break

