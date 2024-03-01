#!/usr/bin/env python3
import subprocess
import uuid
import os
import os.path

from pathlib import Path

Path('BTCGenerator.lock').touch()
genpool = 2000000
file_path = "../btcgen_data/"
while(True):
    filename = str(uuid.uuid4()) + ".csv"
    print(f"Starting Generation process -- Generation {genpool} saving to {filename}")
    subprocess.call(["python3", "genbtcadd.py", str(genpool), file_path, filename])
    subprocess.call(["python3", "btcdupcheck.py", file_path, filename, "0"])
    subprocess.call(["python3", "btcdupcheck.py", file_path, filename, "1"])
    subprocess.call(["python3", "btcdupcheck.py", file_path, filename, "2"])
    subprocess.call(["python3", "btcdupcheck.py", file_path, filename, "3"])
    os.remove(file_path + filename)
    if(os.path.isfile('BTCGenerator.lock') == False):
        break
    