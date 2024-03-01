#!/usr/bin/env python3
import subprocess
import uuid

genpool = 2000
file_path = "../btcgen_data/"
filename = str(uuid.uuid4()) + ".csv"
print(f"Starting Generation process -- Generation {genpool} saving to {filename}")
subprocess.call(["python3", "genbtcadd.py", str(genpool), file_path, filename])

subprocess.call(["python3", "btcdupcheck.py", file_path, filename, "0"])
subprocess.call(["python3", "btcdupcheck.py", file_path, filename, "1"])
subprocess.call(["python3", "btcdupcheck.py", file_path, filename, "2"])
subprocess.call(["python3", "btcdupcheck.py", file_path, filename, "3"])
