import os
import shutil

answers = ["user space!","PPPPPPPPPPPPPPPPPPPP","GP9TIK33ZJ","0123456789abcdef","PdIkt49z2skDztgTTSrhbGP9TIK33Z"]

failed_list = []
potential_failed_list = []
sussesful_list = []
other_list = {40:[], 30:[], 20:[], 10:[], 0:[]}

score_map = {0:0, 10:0, 20:0, 30:0, 40:0, 50:0}

def dmesg_log5():
    output = os.popen("dmesg | tail -5").read()
    print("dmesg output:\n", output)

def score(lines):
    i = 0
    failures = []
    score = 0
    try:
        for i in range(5):
            l = lines[i][8:]
            if l == answers[i]:
                score += 10
            else:
                failures.append(i+1)
                print(l, "is not->", answers[i])
    except:
        failures = [1,2,3,4,5]
    return score, failures
        
for root, dirs, files in os.walk("submissions"):
    for file in files:
        print("Processing", os.path.join(root, file))
        shutil.copy(os.path.join(root, file), "pa3_src.c")

        os.system("dmesg -C")
        os.system("make clean")
        os.system("make")
        print("Done ", os.path.join(root, file), "\n"*10)
        input()
        continue
        os.system("rmmod pa3")
        a = os.system("insmod pa3.ko")

        if a != 0:
            # print("ERR at:", file)
            failed_list.append(file)
            # input()
            continue
        
        try:
            output = os.popen("./executor").read()
        except:
            os.system("rmmod pa3")
            failed_list.append(file)
            continue

        print("student output:\n", output)

        s,f = score(output.split("\n"))
        print("Score:", s)

        # if len(f) > 0:
        #     print("Failed questions:", f)

        os.system("rmmod pa3")
        score_map[s] += 1

        try:
            dmesg = os.popen("dmesg").read()
            if "RSP: " in dmesg:
                potential_failed_list.append(file)
        except:
            potential_failed_list.append(file)
            pass

print("Scores:", score_map)
print("Sussesful list:", sussesful_list)
print("Other list:", other_list)
print("Failed list:", failed_list)
print("Potential failed list:", potential_failed_list)