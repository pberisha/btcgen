#!/usr/bin/env python3
import subprocess
import uuid

genpool = 2000
filename = "../btcgen_data/" + str(uuid.uuid4()) + ".csv"
print(f"Starting Generation process -- Generation {genpool} saving to {filename}")
subprocess.call(["python3", "genbtcadd.py", str(genpool), str(filename)])


