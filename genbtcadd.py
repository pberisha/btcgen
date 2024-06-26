#!/usr/bin/env python3

from fastecdsa import keys, curve
from datetime import datetime

import secp256k1 as ice
import uuid
import sys

startTime = datetime.now()
num_addresses = sys.argv[1]
filename = str(sys.argv[3])
filepath = str(sys.argv[2])
# Set the number of addresses to generate

# Open a file for writing
with open(filepath + filename, 'w') as f:
  # Generate and write each address to the file
  for i in range(int(num_addresses)):
    prvkey_dec   = keys.gen_private_key(curve.P256)
    addr1 = ice.privatekey_to_address(0, True, prvkey_dec)
    addr2 = ice.privatekey_to_address(0, False, prvkey_dec)
    addr3 = ice.privatekey_to_address(1, True, prvkey_dec)
    addr4 = ice.privatekey_to_address(2, True, prvkey_dec)
    priv = ice.btc_pvk_to_wif(prvkey_dec, False)
    f.write(f'{addr2},{addr1},{addr3},{addr4},{priv}\n')
print("Generated " + num_addresses + " and it took " + str(datetime.now() - startTime))

