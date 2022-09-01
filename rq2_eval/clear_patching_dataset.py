import os 

# test_set_base = './test_set_result/'
test_set_base = './test_set_result/'

test_set_dirs = os.listdir( test_set_base )

for test_dir in test_set_dirs:
    print(test_dir)
    test_files = os.listdir( test_set_base + test_dir )
    for f in test_files:
        print(f)
        if f.endswith('.0'):
            os.remove(test_set_base + test_dir + '/' + f)
    # break

# for test_dir in test_set_dirs:
    # print(test_dir)
    # test_files = os.listdir( test_set_base + test_dir )
    # assert len(test_files) == 1
    # print(test_files)
    # if len(test_files) != 1:
    #     print(test_dir)
    #     print(test_files)
