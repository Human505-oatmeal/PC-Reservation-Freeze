import psutil
import re
import os
import json
from time import sleep

#  TODO
#  Create a json file that represents which programs are suspended.
#  key/val will look like Program/Frozen (key program, frozen)
#  create JSON file that will add, append and delete matching keys.

with open('./data/data.json', 'r') as fp:
    data = json.load(fp)


re_proc_match = ".*PC Reservation.*"  # Handling Client weird prefix/suffix's.
questionnaire = """Options
1. Exit
2. Resume
3. Suspend
4. Change target
5. Show suspended processes"""

def clear_screen():
    os.system('cls')

def loading_bar(random_string="here_for_debugging_purposes_ig"):
    cur_str = random_string
    for _ in range(3):
        clear_screen()
        cur_str += "."
        print(cur_str)
        sleep(.5)
        clear_screen()

for proc in psutil.process_iter(['pid', 'name']):
    if re.match(re_proc_match, proc.name()):
        while True:
            user_input = str(input(f"Target = \"{proc.name()}\"\n{questionnaire}\n> "))

            if user_input == "1":
                clear_screen()
                print("Have a good day, the program will still be suspended\n\nPlease rerun this program to continue.")
                break

            elif user_input == "2":
                clear_screen()
                try:
                    proc.resume()
                    loading_bar("Resuming, please wait")
                except psutil.NoSuchProcess:
                    print("The target process is no longer running.")
                    break
                except psutil.AccessDenied:
                    print("Access denied: Unable to resume the process.")
                    break
                except Exception as e:
                    print(f"An unexpected error occurred while resuming: {e}")
                    break

            elif user_input == "3":
                try:
                    proc.suspend()
                    with open("./data/data.json", "w") as f:
                        entry = {f"{proc.name()}": "Suspended"}
                        json.dump(entry, f)
                    loading_bar("Suspending, please wait")
                except psutil.NoSuchProcess:
                    print("The target process is no longer running.")
                    break
                except psutil.AccessDenied:
                    print("Access denied: Unable to suspend the process.")
                    break
                except Exception as e:
                    print(f"An unexpected error occurred while suspending: {e}")
                    break

            elif user_input == "4":
                re_proc_match = input("Please input a program name: ")
                print(f"Updated target match pattern: {re_proc_match}")
                sleep(.5)

                clear_screen()
                break  # Break to update the regex

            elif user_input == "5":
                for k,v in data.items():
                    print(f"Process = {k}, Status = {v}")


            else:
                print("Please enter a valid input.")
                sleep(.5)
                clear_screen()
                continue
