import re
import subprocess

def get_last_login():
    result = subprocess.run(
    ["last", "-3", "joshnelson"],
    capture_output=True,
    text=True
    )

    third_entry = result.stdout.splitlines()[2]

    logout_time = re.findall(r'\d{1,2}:\d{2}', third_entry)[1]

    print(logout_time)

get_last_login()