import sys
import requests
import json
import time
import threading
import queue
from datetime import date, datetime
import dateutil.relativedelta

LOG = queue.Queue()

def wait_sec(ms):
    try:
        while True:
            a = LOG.get()
            print(".", end="", flush=True)
            time.sleep(ms)
            if a != None:
                break
    except KeyboardInterrupt:
        sys.exit(0)

def previous_month():
    current = date.today()
    first_of_previous = current + dateutil.relativedelta.relativedelta(months=-1)
    return first_of_previous, current

class Env:
    def __init__(self, u, p, w):
        self.username = u
        self.password = p
        self.uri = w
        self.auth = ""

    def auth_token(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 1,
            "auth": None
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.uri, data=json.dumps(payload), headers=headers)
        data = response.json()

        if "result" in data:
            self.auth = data["result"]
        else:
            raise Exception(f"Failed to authenticate: {data}")
    #
    def list_groups(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": ["groupid", "name"]
            },
            "auth": self.auth,
            "id": 2
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.uri, data=json.dumps(payload), headers=headers)
        return response.json()
    #
    def get_hosts(self, g):
        payload = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "groupids": g,
                "output": ["hostid", "name"],
            },
            "auth": self.auth,
            "id": 3
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.uri, data=json.dumps(payload), headers=headers)
        return response.json()
    #
    def get_cpu_items(self, h):
        dot = threading.Thread(target=wait_sec, args=(0.5,), daemon=True)
        dot.start()
        payload = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "hostids" : h,
                "search": {"key_": "system.cpu.util"},
                "output": ["itemid", "name"],
            },
            "auth": self.auth,
            "id": 4
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.uri, data=json.dumps(payload), headers=headers)
        if response != None:
            LOG.put(1)

        return response.json()
    #
    def get_memory_items(self, h):
        dot = threading.Thread(target=wait_sec, args=(0.5,), daemon=True)
        dot.start()
        payload = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "hostids" : h,
                "search": {"key_": "vm.memory.util"},
                "output": ["itemid", "name"],
            },
            "auth": self.auth,
            "id": 5
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.uri, data=json.dumps(payload), headers=headers)
        if response != None:
            LOG.put(1)

        return response.json()
    #
    def get_cpu_data(self, id):
        dot = threading.Thread(target=wait_sec, args=(0.5,), daemon=True)
        dot.start()
        start, end = previous_month()
        s = int(time.mktime(datetime.strptime(str(start), "%Y-%m-%d").timetuple()))
        e = int(time.mktime(datetime.strptime(str(end), "%Y-%m-%d").timetuple()))
        payload = {
            "jsonrpc": "2.0",
            "method": "trend.get",
            "params": {
                "itemids": id,
                "time_from": s,  # Start time (Unix timestamp)
                "time_till": e,    # End time (Unix timestamp)
                "sortfield": "clock",
                "sortorder": "ASC",
                "output": ["itemid", "clock", "value_avg", "value_min", "value_max"]  # Get timestamp and value
            },
            "auth": self.auth,
            "id": 6
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.uri, data=json.dumps(payload), headers=headers)
        if response != None:
            LOG.put(1)

        return response.json()
    #
    def get_memory_data(self, id):
        dot = threading.Thread(target=wait_sec, args=(0.5,), daemon=True)
        dot.start()
        start, end = previous_month()
        s = int(time.mktime(datetime.strptime(str(start), "%Y-%m-%d").timetuple()))
        e = int(time.mktime(datetime.strptime(str(end), "%Y-%m-%d").timetuple()))
        payload = {
            "jsonrpc": "2.0",
            "method": "trend.get",
            "params": {
                "itemids": id,
                "time_from": s,  # Start time (Unix timestamp)
                "time_till": e,    # End time (Unix timestamp)
                "sortfield": "clock",
                "sortorder": "ASC",
                "output": ["itemid", "clock", "value_avg", "value_min", "value_max"]  # Get timestamp and value
            },
            "auth": self.auth,
            "id": 7
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.uri, data=json.dumps(payload), headers=headers)
        if response != None:
            LOG.put(1)

        return response.json()

    #
    def logout(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "user.logout",
            "params": [],
            "id": 1 
        }

        headers = {"Content-Type", "application/json"}
        response = requests.post(self.uri, data=json.dumps(payload), headers=headers)
        if response != None:
            LOG.put(1)
        return response.json()
