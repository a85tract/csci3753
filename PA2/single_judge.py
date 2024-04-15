from pwn import *
import os
import shutil
import subprocess

# context.log_level = 'DEBUG'

SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

standard_output = [b'zOMkAYdTMMePttU', b'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP', b'Q2Smt08UdcI7W5EHcfS5v4Dscdy3w4ZAmEs2fLCjSvHOZQayNc', b'Hello,_World!', b'lUBpSkvajBzeeIHxw5ebwPjmJl4Ufs2fvXUiuEe0yHwaNW1nwa0123456789']
error_list = []
score_dict = {}

def file_read(p,size):
        p.sendline(b"r")
        p.sendline(str(size).encode())
        return "DEBUG"

def file_write(p,data):
    p.sendline(b"w")
    p.sendline(data)

def file_seek(p,offset, whence):
    p.sendline(b"s")
    p.sendline(str(offset).encode())
    p.sendline(str(whence).encode())

def score(out_file):

    answer_list = []
    out_message = "all output:\n"

    # Test 1
    shutil.copyfile('./random.txt.bak', './random.txt')
    p = process(argv=['./stu','./random.txt'])
    file_read(p,15)
    output = p.recvall(timeout=0.1)
    if standard_output[0] in output:
        print("\033[92mTested 1 - Passed\033[0m")
    else:
        print("\033[91mTested 1 - Failed\033[0m")
        print("student output: ", output)
        print("standard output: ", standard_output[0])
    p.close()
    # answer_list.append(ans)
    # answer_list.append(b"*******ERROR*******")

    # Test 2
    shutil.copyfile('./random.txt.bak', './random.txt')
    p = process(argv=['./stu','./random.txt'])
    file_write(p,b"P"*60) # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
    file_seek(p,20, SEEK_SET)
    file_read(p,35)
    output = p.recvall(timeout=0.1)
    if standard_output[1] in output:
        print("\033[92mTested 2 - Passed\033[0m")
    else:
        print("\033[91mTested 2 - Failed\033[0m")
        print("student output: ", output)
        print("standard output: ", standard_output[1])
    p.close()

    # Test 3
    shutil.copyfile('./random.txt.bak', './random.txt')
    p = process(argv=['./stu','./random.txt'])
    file_seek(p,-50, SEEK_END)
    file_read(p,50)
    output = p.recvall(timeout=0.1)
    if standard_output[2] in output:
        print("\033[92mTested 3 - Passed\033[0m")
    else:
        print("\033[91mTested 3 - Failed\033[0m")
        print("student output: ", output)
        print("standard output: ", standard_output[2])
    p.close()

    # Test 4
    shutil.copyfile('./random.txt.bak', './random.txt')
    p = process(argv=['./stu','./random.txt'])
    file_seek(p,1000, SEEK_SET)
    file_write(p,b"Hello,_World!")
    file_seek(p,1000, SEEK_SET)
    file_read(p,13) # str should be cut off by "\x00"
    output = p.recvall(timeout=0.1)
    if standard_output[3] in output:
        print("\033[92mTested 4 - Passed\033[0m")
    else:
        print("\033[91mTested 4 - Failed\033[0m")
        print("student output: ", output)
        print("standard output: ", standard_output[3])
    p.close()

    # Test 5
    shutil.copyfile('./random.txt.bak', './random.txt')
    p = process(argv=['./stu','./random.txt'])
    file_seek(p,5000, SEEK_SET)
    file_write(p,b"0123456789abcdef")
    file_seek(p,4950, SEEK_SET)
    file_read(p,60)
    output = p.recvall(timeout=0.1)
    if standard_output[4] in output:
        print("\033[92mTested 5 - Passed\033[0m")
    else:
        print("\033[91mTested 5 - Failed\033[0m")
        print("student output: ", output)
        print("standard output: ", standard_output[4])
    p.close()
    

    
if __name__ == "__main__":
    current_directory = os.getcwd()
    source_folder = "./PA2_submit"
    output_folder = "./output_logs"
    single_test = ["behy7142.c"]
    for filename in single_test:
        print(f"Testing {filename}")
        r = subprocess.run(["gcc", "-o", "stu", f"{source_folder}/{filename}"])
        if r.returncode != 0:
            print(f"Error: {filename}")
            error_list.append(filename)
            continue
        try:
            score(output_folder+"/"+filename+".log")
        except:
            print(f"Error: {filename}")
            error_list.append(filename)
            continue
        # input()
        print("="*90)
        # os.remove('./stu')