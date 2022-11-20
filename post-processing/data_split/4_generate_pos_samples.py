import ast
import os
import pickle
import json
import astunparse
import asttokens

with open('./anchor_positive_negative_samples.pkl', 'rb') as handler:
    anchor_positive_samples = pickle.load(handler)
print("anchor_positie_samples:", len(anchor_positive_samples))

anchor_samples_dict = {}
positive_samples_dict = {}
negative_samples_dict = {}

for k, v in anchor_positive_samples.items():
    print(k)
    # print(v)
    try:
        sample_index = k 
        todo_comment = v['anchor_todo_comment'].strip().lower()

        anchor_todo_statement = v['anchor_todo_statement'][1].strip().lower()  
        anchor_todo_context = [] 
        anchor_todo_context.append(v['anchor_function_name'].split('@')[0])
        for e in v['anchor_pre_context']: 
            anchor_todo_context.append(e[1].strip())
        for e in v['anchor_post_context']:
            anchor_todo_context.append(e[1].strip())
        anchor_todo_context = " ".join(anchor_todo_context)
        anchor_todo_comment_statement = todo_comment + " </s> "  + anchor_todo_statement

        # print("todo comment:", todo_comment)
        # print("anchor_todo_comment_statement:", anchor_todo_comment_statement)
        # print("anchor_todo_context:", anchor_todo_context)
        positive_todo_statement = v['positive_todo_statement'][1].strip().lower()
        positive_todo_context = []
        positive_todo_context.append(v['positive_function_name'].split('@')[0])
        for e in v['positive_pre_context']: 
            positive_todo_context.append(e[1].strip())
        for e in v['positive_post_context']:
            positive_todo_context.append(e[1].strip())
        positive_todo_context = " ".join(positive_todo_context)
        positive_todo_comment_statement = todo_comment + " </s> "  + positive_todo_statement
        
        negative_todo_statement = v['negative_todo_statement'][1].strip().lower()
        negative_todo_context = []
        negative_todo_context.append(v['negative_function_name'])
        for e in v['negative_pre_context']: 
            negative_todo_context.append(e[1].strip())
        for e in v['negative_post_context']:
            negative_todo_context.append(e[1].strip())
        negative_todo_context = " ".join(negative_todo_context)
        negative_todo_comment_statement = todo_comment + " </s> "  + negative_todo_statement
       
        key = sample_index
        anchor_samples_value = {} 
        anchor_samples_value['todo_comment'] = todo_comment 
        anchor_samples_value['anchor_todo_comment_statement'] = anchor_todo_comment_statement
        anchor_samples_value['anchor_todo_context'] = anchor_todo_context
        anchor_samples_dict[key] = anchor_samples_value 
        
        positive_samples_value = {} 
        positive_samples_value['todo_comment'] = todo_comment 
        positive_samples_value['positive_todo_comment_statement'] = positive_todo_comment_statement
        positive_samples_value['positive_todo_context'] = positive_todo_context
        positive_samples_dict[key] = positive_samples_value 

        negative_samples_value = {} 
        negative_samples_value['todo_comment'] = todo_comment 
        negative_samples_value['negative_todo_comment_statement'] = negative_todo_comment_statement
        negative_samples_value['negative_todo_context'] = negative_todo_context
        negative_samples_dict[key] = negative_samples_value 

    # print("positive_todo_comment_statement:", positive_todo_comment_statement)
    # print("positive_todo_context:", positive_todo_context)
    
    # anchor_f.write( anchor_todo_comment_statement + '\t' + anchor_todo_context + '\n') 
    # positive_f.write( positive_todo_comment_statement + '\t' + positive_todo_context + '\n') 
    # break
    except:
        continue

assert len(positive_samples_dict) == len(anchor_samples_dict)
assert len(negative_samples_dict) == len(anchor_samples_dict)
print("anchor_samples_dict:", len(anchor_samples_dict))
print("positive_samples_dict:", len(positive_samples_dict))
print("negative_samples_dict:", len(positive_samples_dict))

with open('./anchor_samples_dict.pkl', 'wb') as handler:
    pickle.dump(anchor_samples_dict, handler)

with open('./positive_samples_dict.pkl', 'wb') as handler:
    pickle.dump(positive_samples_dict, handler)

with open('./negative_samples_dict.pkl', 'wb') as handler:
    pickle.dump(negative_samples_dict, handler)

