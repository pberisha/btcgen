#!/usr/bin/env python3
# 2022/Dec/26, citb0in
import concurrent.futures
import os
import numpy as np
import fastecdsa.keys as fkeys
import fastecdsa.curve as fcurve
import secp256k1 as ice

# Set the number of addresses to generate
num_addresses = 10

# Define a worker function that generates a batch of addresses and returns them
def worker(start, end):
  # Generate a NumPy array of random private keys using fastecdsa
  private_keys = np.array([fkeys.gen_private_key(fcurve.P256) for _ in range(start, end)])

  # Use secp256k1 to convert the private keys to addresses
  thread_addresses = np.array([ice.privatekey_to_address(2, True, dec) for dec in private_keys])
  print(thread_addresses)

  return thread_addresses

# Use a ProcessPoolExecutor to generate the addresses in parallel
with concurrent.futures.ProcessPoolExecutor() as executor:
  # Divide the addresses evenly among the available CPU cores
  addresses_per_core = num_addresses // os.cpu_count()

  # Submit a task for each batch of addresses to the executor
  tasks = []
  for i in range(os.cpu_count()):
    start = i * addresses_per_core
    end = (i+1) * addresses_per_core
    tasks.append(executor.submit(worker, start, end))

  # Wait for the tasks to complete and retrieve the results
  addresses = []
  for task in concurrent.futures.as_completed(tasks):
    addresses.extend(task.result())

# Write the addresses to a file
np.savetxt('addresses_1M_with_ProcessPool.txt', addresses, fmt='%s')