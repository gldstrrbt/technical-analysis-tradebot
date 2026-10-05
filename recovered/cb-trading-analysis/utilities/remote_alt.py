import os, sys, time, subprocess
from threading import Thread

proc = ""

def fuck():
	proc = subprocess.Popen(['python3 __orig_get_history.py'], shell=True)


Thread(target=fuck).start()
quit()
time.sleep(3)
proc.terminate()
# sys.exit("fuck")