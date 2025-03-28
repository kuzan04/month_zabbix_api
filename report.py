import tkinter as tk
import csv
from sys import platform
import time
import ctypes
from statistics import mean
from datetime import datetime
from tkinter import filedialog
from connect import previous_month


def save_file(res):
    h, r = res
    # Date time now.
    now = datetime.now()
    t = now.strftime("%Y-%m-%dT%H%M%S")
    
    root = tk.Tk()
    root.withdraw()

    fn = filedialog.asksaveasfilename(
        initialfile=f"zabbix-reports-{t}",
        defaultextension='.csv',
        title="Save File As",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
    if fn:
        try:
            with open(fn, 'w', newline='') as f:
                # Cursor in csv.
                wr = csv.writer(f)

                # Header
                fi = ['Host', 'From', 'Til', 'CPU (Min)', 'CPU (Avg)', 'CPU (Max)', 'Memory (Min)', 'Memory (Avg)', 'Memory (Max)']

                # Write header in file.
                wr.writerow(fi)
                # Write row other.
                if not isinstance(h, list):
                    # CPU
                    mn = []; avg =[]; mx = []
                    for i in range(len(r[h]['cpu_util'])):
                        mn.append("%.2f" % round(float(r[h]['cpu_util'][i]['value_min']), 2))
                        avg.append(r[h]['cpu_util'][i]['value_avg'])
                        mx.append("%.2f" % round(float(r[h]['cpu_util'][i]['value_max']), 2))
                    #Memory
                    mmn =[]; mavg =[]; mmx =[]
                    for i in range(len(r[h]['memory_util'])):
                        mmn.append("%.2f" % round(float(r[h]['memory_util'][i]['value_min']), 2))
                        mavg.append(r[h]['memory_util'][i]['value_avg'])
                        mmx.append("%.2f" % round(float(r[h]['memory_util'][i]['value_max']), 2))

                    s, e = previous_month()
                    wr.writerow([h, s, e, min(mn), "%.2f" % round(mean(list(map(float, avg))), 2), max(mx), min(mmn), "%.2f" % round(mean(list(map(float, mavg))), 2), max(mmx)])
                else:
                    s, e = previous_month()
                    for j in h:
                        mn = []; avg =[]; mx = [];
                        for i in range(len(r[j]['cpu_util'])):
                            mn.append("%.2f" % round(float(r[j]['cpu_util'][i]['value_min']), 2))
                            avg.append(r[j]['cpu_util'][i]['value_avg'])
                            mx.append("%.2f" % round(float(r[j]['cpu_util'][i]['value_max']), 2))
                        #Memory
                        mmn =[]; mavg =[]; mmx =[]
                        for i in range(len(r[j]['memory_util'])):
                            mmn.append("%.2f" % round(float(r[j]['memory_util'][i]['value_min']), 2))
                            mavg.append(r[j]['memory_util'][i]['value_avg'])
                            mmx.append("%.2f" % round(float(r[j]['memory_util'][i]['value_max']), 2))

                        wr.writerow([j, s, e, min(mn), "%.2f" % round(mean(list(map(float, avg))), 2), max(mx), min(mmn), "%.2f" % round(mean(list(map(float, mavg))), 2), max(mmx)])
                
            if platform == "win32":
                ctypes.windll.user32.MessageBoxW(0, "File saved successfully:\n{}".format(fn), "File Saved", 0)
        except Exception as e:
            if platform == "win32":
                ctypes.windll.user32.MessageBoxW(0, "Error saving file:\n{}".format(str(e)), "Error", 0)
            else:
                pass

    root.destroy()

    print("Generate file csv success!\n5 seconds back to first page...", end="")
    time.sleep(5)
    return 1
