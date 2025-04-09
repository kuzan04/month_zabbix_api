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
        e.logout()
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
        e.logout()
        sys.exit(0)
#
def list_items(m, e, sh, h):
    clear_screen()
    print(m)
    try:
        if not isinstance(sh, list) and not isinstance(h, list):
            si1 = e.get_cpu_items(sh)['result']
            si2 = e.get_memory_items(sh)['result']
            if len(si1) != 0 and len(si2) != 0:
                si1 = [i['itemid'] for i in si1]
                si2 = [i['itemid'] for i in si2]
                cpu = e.get_cpu_data(si1)['result']
                memory = e.get_memory_data(si2)['result']
                ra1 = list(dict.fromkeys([i['itemid'] for i in cpu]))
                ra2 = list(dict.fromkeys([i['itemid'] for i in memory]))
                if len(ra1) != 1 and len(ra2) != 1:
                    gh = {};
                    for i in range((len(ra1) + len(ra2))//2):
                        gh.update({f"{h} (Stack{i+1})": 
                                   {"cpu_util": [j for j in cpu if j['itemid'] == ra1[i]],
                                   "memory_util": [j for j in memory if j['itemid'] == ra2[i]]}
                                   })
                    print(f"{h} get datas susccess!")
                    return list(gh.keys()), gh
                else:
                    print(f"{h} get datas susccess!")
                    return h, {h: {"cpu_util":cpu, "memory_util":memory}}
            else:
                print(f"{h} not have datas... [SNMP: Disable and Not have about cpu & memory]")
                return h, {h: {"cpu_util":[], "memory_util":[]}}
        else:
            host_dirc = {}
            for i in range((len(sh) + len(h))//2):
                si1 = e.get_cpu_items(sh[i])['result']
                si2 = e.get_memory_items(sh[i])['result']
                si1 = [j['itemid'] for j in si1]
                si2 = [j['itemid'] for j in si2]
                if len(si1) != 0 and len(si2) != 0:
                    cpu  = e.get_cpu_data(si1)['result']
                    memory  = e.get_memory_data(si2)['result']
                    ra1 = list(dict.fromkeys([i['itemid'] for i in cpu]))
                    ra2 = list(dict.fromkeys([i['itemid'] for i in memory]))
                    if len(cpu) == 0 and len(memory) == 0:
                        print(f"{h[i]} not have datas... [SNMP: Disable]")
                        host_dirc.update({h[i]: {"cpu_util":[], "memory_util":[]}})
                    elif len(ra1) != 1 and len(ra2) != 1:
                        for j in range((len(ra1)+len(ra2))//2):
                            if "Border" in h[i] or ("DR" in h[i] and "Core" in h[i]):
                                host_dirc.update({f"{h[i]} (Resource{j+1})": 
                                                  {"cpu_util": [k for k in cpu if k['itemid'] == ra1[j]],
                                                   "memory_util": [k for k in memory if k['itemid'] == ra2[j]]}
                                                  })
                            else:
                                host_dirc.update({f"{h[i]} (Stack{j+1})": 
                                                  {"cpu_util": [k for k in cpu if k['itemid'] == ra1[j]],
                                                   "memory_util": [k for k in memory if k['itemid'] == ra2[j]]}
                                                  })
                        print(f"{h[i]} get datas susccess!")
                        
                    else:
                        print(f"{h[i]} get datas susccess!")
                        host_dirc.update({h[i]: {"cpu_util":cpu, "memory_util":memory}})
                else:
                    print(f"{h[i]} not have datas... [SNMP: Disable and Not have about cpu & memory]")
                    host_dirc.update({h[i]: {"cpu_util":[], "memory_util":[]}})

            return list(host_dirc.keys()), host_dirc
    except Exception as err:
        print(err)
        e.logout()
        sys.exit(0)
