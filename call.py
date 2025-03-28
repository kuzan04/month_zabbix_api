import os
import sys
import time
import threading
from connect import Env


NOT_USE1 = ["Linux servers", "Zabbix servers", "Discovered hosts", "Virtual machines", "Hypervisors", "Applications", "Databases"]
NOT_USE2 = ["DC Firewall", "DC Other", "DR Other", "DR Firewall", "DR-Disable"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
#
def select_group(m, e, lg):
    clear_screen()
    print(m)
    dup = []
    for i in range(len(lg)):
        if lg[i]['name'] not in NOT_USE1 and lg[i]['name'] not in NOT_USE2:
            dup.append(lg[i])
            print(f'({i})\t: {lg[i]['name']}')
    print("(a)\t: All from top.")
    print("(b)\t: Back to first.")
    s = input("Press the value (Ctrl+C or Press Enter to exit || Press ',' to multiple select): ")
    try:
        if s == "":
            sys.exit(0)
        elif s == "b":
            return s
        elif s == "a":
            return select_host(m, e, [i["groupid"] for i in dup], lg)
        elif ',' in set(s):
            s = s.split(',')
            dup = [lg[i]['groupid'] for i in range(len(lg)) if str(i) in s and (lg[i]['name'] not in NOT_USE1 and lg[i]['name'] not in NOT_USE2)]
            return select_host(m, e, dup)
        elif lg[int(s)]['name'] in NOT_USE1 or lg[int(s)]['name'] in NOT_USE2:
            return select_group(m, e, lg)
        else:
            return select_host(m, e, lg[int(s)]['groupid'], lg)
    except:
        sys.exit(0)
#
def select_host(m, e, sg, lg):
    clear_screen()
    ah = e.get_hosts(sg)['result']
    print(m)
    for i in range(len(ah)):
        print(f'({i})\t: {ah[i]['name']}')
    print("(a)\t: All from top.")
    print("(b1)\t: Back to before.")
    print("(b)\t: Back to first.")
    s = input("Press the value (Ctrl+C or Press Enter to exit || Press ',' to multiple select): ")
    try:
        if s == "":
            sys.exit(0)
        elif s == "b":
            return s
        elif s == "b1":
            return select_group(m, e, lg)
        elif s == "a":
            return list_items(m, e, [i["hostid"] for i in ah], [i["name"] for i in ah])
        elif ',' in set(s):
            s = [i.replace(" ", "") for i in s.split(',') if i != ""]
            dup = [ah[i] for i in range(len(ah)) if str(i) in s]
            return list_items(m, e, [i["hostid"] for i in dup], [i["name"] for i in dup])
        else:
            return list_items(m, e, ah[int(s)]["hostid"], ah[int(s)]["name"])
    except:
        sys.exit(0)
#
def list_items(m, e, sh, h):
    clear_screen()
    print(m)
    try:
        if not isinstance(sh, list) and not isinstance(h, list):
            si1 = e.get_cpu_items(sh)['result'][0]['itemid']
            si2 = e.get_memory_items(sh)['result'][0]['itemid']
            cpu = e.get_cpu_data(si1)['result']
            memory = e.get_memory_data(si2)['result']
            print(f"{h} get datas susccess!")
            return h, {h: {"cpu_util":cpu, "memory_util":memory}}
        else:
            host_dirc = {i: {} for i in h}
            for i in range(int((len(sh) + len(h))/2)):
                si1 = e.get_cpu_items(sh[i])['result'][0]['itemid']
                si2 = e.get_memory_items(sh[i])['result'][0]['itemid']
                cpu  = e.get_cpu_data(si1)['result']
                memory  = e.get_memory_data(si2)['result']
                print(f"{h[i]} get datas susccess!")
                host_dirc[h[i]] = {"cpu_util":cpu, "memory_util":memory}
            return h, host_dirc
    except Exception as e:
        sys.exit(1)
