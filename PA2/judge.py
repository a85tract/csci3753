from pwn import *
import os
import shutil
import subprocess
import csv

# context.log_level = 'DEBUG'

SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

standard_output = [b'zOMkAYdTMMePttU', b'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP', b'Q2Smt08UdcI7W5EHcfS5v4Dscdy3w4ZAmEs2fLCjSvHOZQayNc', b'Hello,_World!', b'lUBpSkvajBzeeIHxw5ebwPjmJl4Ufs2fvXUiuEe0yHwaNW1nwa0123456789']
error_list = []
score_dict = {}

def write_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def read_csv(filename):
    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

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


def single_judge():
    score = 0
    msg = "single_judge\n"
    # Test 1
    shutil.copyfile('./random.txt.bak', './random.txt')
    p = process(argv=['./stu','./random.txt'])
    file_read(p,15)
    output = p.recvall(timeout=0.1)
    if standard_output[0] in output:
        # print("\033[92mTested 1 - Passed\033[0m")
        msg += "Tested 1 - Passed\n"
        score += 10
    p.close()

    # Test 2
    shutil.copyfile('./random.txt.bak', './random.txt')
    p = process(argv=['./stu','./random.txt'])
    file_write(p,b"P"*60) # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
    file_seek(p,20, SEEK_SET)
    file_read(p,35)
    output = p.recvall(timeout=0.1)
    if standard_output[1] in output:
        # print("\033[92mTested 2 - Passed\033[0m")
        msg += "Tested 2 - Passed\n"
        score += 10
    p.close()

    # Test 3
    shutil.copyfile('./random.txt.bak', './random.txt')
    p = process(argv=['./stu','./random.txt'])
    file_seek(p,-50, SEEK_END)
    file_read(p,50)
    output = p.recvall(timeout=0.1)
    if standard_output[2] in output:
        # print("\033[92mTested 3 - Passed\033[0m")
        msg += "Tested 3 - Passed\n"
        score += 10
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
        # print("\033[92mTested 4 - Passed\033[0m")
        msg += "Tested 4 - Passed\n"
        score += 10
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
        # print("\033[92mTested 5 - Passed\033[0m")
        msg += "Tested 5 - Passed\n"
        score += 10
    p.close()
    return score, msg

def score(out_file):

    answer_list = []
    out_message = "all output:\n"
    shutil.copyfile('./random.txt.bak', './random.txt')
    p = process(argv=['./stu','./random.txt'])

    # Test 1
    file_read(p, 15) # r 15
    print("Tested 1")

    # Test 2
    file_write(p, b"P"*60) # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
    file_seek(p, 20, SEEK_SET)
    file_read(p, 35)
    print("Tested 2")

    # Test 3
    file_seek(p, -50, SEEK_END)
    file_read(p, 50)
    print("Tested 3")

    # Test 4
    file_seek(p, 1000, SEEK_SET)
    file_write(p, b"Hello,_World!")
    file_seek(p, 1000, SEEK_SET)
    file_read(p, 13) # str should be cut off by "\x00"
    print("Tested 4")

    # Test 5
    file_seek(p, 5000, SEEK_SET)
    file_write(p, b"0123456789abcdef")
    file_seek(p, 4950, SEEK_SET)
    file_read(p, 60)
    print("Tested 5")

    all_output = p.recvall(timeout=0.1)

    p.close()

    out_message += all_output.decode() + "\n"

    score = 0
    for i in range(5):
        # if answer_list[i] == standard_output[i]:
        if standard_output[i] in all_output:
            # print("Correct")
            out_message += f"Correct: {filename} Test {i+1}\n"
            score += 10
        else:
            # print(f"Wrong: {filename} Test {i+1}")
            out_message += f"Wrong: {filename} Test {i+1}\n"
            # input()

    if score != 50:
        score2, msg2 = single_judge()
        out_message += msg2
        if score < score2: # select the higher score
            score = score2 - 2 # run normally, but -2 for the single_judge
        if score < 0:
            score = 0

    # print(f"Score: {score}")
    out_message += f"Score: {score}\n"

    with open(out_file, "w") as f:
        f.write(out_message)
    f.close()

    score_dict[filename] = score

def write_score(score_dict):
    data_from_csv = read_csv('2024-02-29T1333_Grades-CSCI_3753.csv')
    for key, value in score_dict.items():
        for line in data_from_csv[2:]:
            if line[1] in key:
                line[5] = str(value)
    write_csv('out.csv', data_from_csv)

if __name__ == "__main__":
    current_directory = os.getcwd()
    source_folder = "./PA2_submit"
    output_folder = "./output_logs"

    for filename in os.listdir(source_folder):
        # input()
        print(f"Testing {filename}")
        r = subprocess.run(["gcc", "-o", "stu", f"{source_folder}/{filename}"])
        if r.returncode != 0:
            print(f"compile Error: {filename}")
            error_list.append(filename)
            continue
        try:
            score(output_folder+"/"+filename+".log")
        except:
            try:
                single_judge()
                score2, msg2 = single_judge()
                score_dict[filename] = score2 - 1 # maybe my fault
            except:
                print(f"Fatal Error: {filename}")
                error_list.append(filename)
                continue
        # input()
        os.remove('./stu')

    score_counter = {}
    print(f"Score:")
    for key, value in score_dict.items():
        print(f"{key}: {value}")
        if value in score_counter:
            score_counter[value] += 1
        else:
            score_counter[value] = 1
    print("\n"*2)

    print(f"Score counter:")
    sorted_dict = dict(sorted(score_counter.items(), key=lambda item: item[0], reverse=True))
    for key, value in sorted_dict.items():
        print(f"{key}: {value}")
    print("\n"*2)
    print(f"Error files:")
    for error in error_list:
        print(error)

    write_score(score_dict)