import psutil
import re
import os
import json
from time import sleep

# TODO
# Use colorize for user-friendly look
# Add more comprehensive info like PID, CPU usage, Memory Usage
# Implement a GUI


json_file_path = "./data/data.json"
pattern = r"(.*)(PC Reservation)(.*)"
re_proc_match = pattern
questionnaire = """Options
1. Exit
2. Resume
3. Suspend
4. Change target
5. Show suspended processes"""

def update_json_file():
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=4)


if os.stat(json_file_path).st_size == 0:
    data = {}
else:
    with open(json_file_path, 'r') as fp:
        data = json.load(fp)

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

exit_program = False
while not exit_program:
    for proc in psutil.process_iter(['pid', 'name']):
        if re.match(re_proc_match, proc.info['name']):
            while True:
                user_input = str(input(f"Target = \"{proc.info['name']}\"\n{questionnaire}\n> "))
                if user_input == "1":
                    clear_screen()
                    print("Have a good day, the program will still be suspended\n\nPlease rerun this program to continue.")
                    exit_program = True
                    break

                elif user_input == "2":
                    clear_screen()
                    try:
                        proc.resume()
                        if proc.info['name'] in data:
                            del data[proc.info['name']]
                        update_json_file()
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
                        data[proc.info['name']] = "Suspended"
                        update_json_file()
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
                    new_program_name = input("Please input a program name: ").strip()
                    re_proc_match = pattern.replace("PC Reservation", new_program_name)
                    print(f"Updated target match pattern: {re_proc_match}")
                    sleep(.5)
                    clear_screen()
                    break # break to check for inner processes (finally figured this bs out)

                elif user_input == "5":
                    if data: 
                        for process, status in data.items():
                            print(f"Process = {process}, Status = {status}")
                    else:
                        print("No processess are currently suspended.")
                    sleep(1)
                    clear_screen()


                else:
                    print("Please enter a valid input.")
                    sleep(.5)
                    clear_screen()
                    continue
