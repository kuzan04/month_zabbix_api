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

                # Set Date.
                s, e = previous_month()

                # Write row other.
                if not isinstance(h, list):
                    if len(r[h]['cpu_util']) != 0 or len(r[h]['memory_util']) != 0:
                        # CPU
                        mn = [float("%.2f" % round(float(i['value_min']), 2)) for i in r[h]['cpu_util'] if float(i['value_min']) > 1]
                        avg = [float("%.2f" % round(float(i['value_avg']), 2)) for i in r[h]['cpu_util'] if float(i['value_avg']) > 1]
                        mx = [float("%.2f" % round(float(i['value_max']), 2)) for i in r[h]['cpu_util'] if float(i['value_max']) > 1]
                        # Memory
                        mmn = [float("%.2f" % round(float(i['value_min']), 2)) for i in r[h]['memory_util'] if float(i['value_min']) > 1]
                        mavg = [float("%.2f" % round(float(i['value_avg']), 2)) for i in r[h]['memory_util'] if float(i['value_avg']) > 1]
                        mmx = [float("%.2f" % round(float(i['value_max']), 2)) for i in r[h]['memory_util'] if float(i['value_max']) > 1]

                        wr.writerow([h, s, e, min(mn), "%.2f" % round(mean(list(map(float, avg))), 2), max(mx), min(mmn), "%.2f" % round(mean(list(map(float, mavg))), 2), max(mmx)])
                else:
                    for j in h:
                        if len(r[j]['cpu_util']) != 0 or len(r[j]['memory_util']) != 0:
                            # CPU
                            mn = [float("%.2f" % round(float(i['value_min']), 2)) for i in r[j]['cpu_util'] if float(i['value_min']) > 1]
                            avg = [float("%.2f" % round(float(i['value_avg']), 2)) for i in r[j]['cpu_util'] if float(i['value_avg']) > 1]
                            mx = [float("%.2f" % round(float(i['value_max']), 2)) for i in r[j]['cpu_util'] if float(i['value_max']) > 1]
                            # Memory
                            mmn = [float("%.2f" % round(float(i['value_min']), 2)) for i in r[j]['memory_util'] if float(i['value_min']) > 1]
                            mavg = [float("%.2f" % round(float(i['value_avg']), 2)) for i in r[j]['memory_util'] if float(i['value_avg']) > 1]
                            mmx = [float("%.2f" % round(float(i['value_max']), 2)) for i in r[j]['memory_util'] if float(i['value_max']) > 1]

                            wr.writerow([j, s, e, min(mn), "%.2f" % round(mean(list(map(float, avg))), 2), max(mx), min(mmn), "%.2f" % round(mean(list(map(float, mavg))), 2), max(mmx)])
                
            if platform == "win32":
                ctypes.windll.user32.MessageBoxW(0, "File saved successfully:\n{}".format(fn), "File Saved", 0)
        except Exception as e:
            if platform == "win32":
                ctypes.windll.user32.MessageBoxW(0, "Error saving file:\n{}".format(str(e)), "Error", 0)
            else:
                print(e)

    root.destroy()

    print("Generate file csv success!\n3 seconds back to first page...", end="")
    time.sleep(3)
    return 1
