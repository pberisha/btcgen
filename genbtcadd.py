#!/usr/bin/env python3
# 2022/Dec/26, citb0in
from fastecdsa import keys, curve
import secp256k1 as ice
import uuid
from datetime import datetime
startTime = datetime.now()
filename = str(uuid.uuid4()) + "-20mil.csv"
# Set the number of addresses to generate
num_addresses = 20000000

# Open a file for writing
with open(filename, 'w') as f:
  # Generate and write each address to the file
  for i in range(num_addresses):
    prvkey_dec   = keys.gen_private_key(curve.P256)
    addr1 = ice.privatekey_to_address(0, True, prvkey_dec)
    addr2 = ice.privatekey_to_address(0, False, prvkey_dec)
    addr3 = ice.privatekey_to_address(1, True, prvkey_dec)
    addr4 = ice.privatekey_to_address(2, True, prvkey_dec)
    priv = ice.btc_pvk_to_wif(prvkey_dec, False)
    f.write(f'{addr2},{addr1},{addr3},{addr4},{priv}\n')
print(datetime.now() - startTime)

