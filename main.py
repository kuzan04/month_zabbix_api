import os
import sys
import json
from dotenv import load_dotenv
from connect import Env
from call import select_group, select_host
from report import save_file


def choose(m, e, s):
    match s:
        case 1:
            # Query group
            groups = e.list_groups()['result']
            # Page1 - Select Group
            g = select_group(m, e, groups)
            # Re-call first page.
            if g == "b":
                return call(m, e)
            # Generate Reports.
            if save_file(g) == 1:
                return call(m, e)
        case 2:
            print("(Hold) Today 2025-03-26 15:12 Fuction this not success.")
#
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
#
def call(m, e):
    clear_screen()
    print(m)
    print("(1)\t: Find all device in zabbix")
    print("(2)\t: Get report all device in zabbix [404]")
    result = input("Press the value (Ctrl+C or Press Enter to exit): ")
    try:
        if result != "":
            return choose(m, e, int(result))
        else:
            sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)
#
if __name__ == "__main__":
    # Handle case where script runs as a bundled .exe
    try:
        base_path = sys._MEIPASS  # Extracted PyInstaller directory
    except Exception:
        base_path = os.path.abspath(".")
    # Load the .env file from the correct location
    env_path = os.path.join(base_path, ".env")
    load_dotenv(env_path)

    w = "Welcome to script create reports from Zabbix (1 Month only)"
    env = Env(os.getenv('ZABBIX_USER'), os.getenv('ZABBIX_PASSWORD'), os.getenv('ZABBIX_URI'))
    env.auth_token()
    try:
        call(w, env)
    except KeyboardInterrupt:
        sys.exit(0)
