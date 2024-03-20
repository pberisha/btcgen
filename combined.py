#!/usr/bin/env python3
import pandas as pd
import secp256k1 as ice
import uuid
import sys

from fastecdsa import keys, curve
from datetime import datetime
from pprint import pprint

startTime = datetime.now()
num_addresses = sys.argv[1]
# Set the number of addresses to generate

df = pd.DataFrame()

# Generate and write each address to the file
for i in range(int(num_addresses)):
    prvkey_dec   = keys.gen_private_key(curve.P256)
    addr1 = ice.privatekey_to_address(0, True, prvkey_dec)
    addr2 = ice.privatekey_to_address(0, False, prvkey_dec)
    addr3 = ice.privatekey_to_address(1, True, prvkey_dec)
    addr4 = ice.privatekey_to_address(2, True, prvkey_dec)
    priv = ice.btc_pvk_to_wif(prvkey_dec, False)
    new_row = {addr2, addr1, addr3, addr4, priv}
    df.append(new_row, ignore_index=True)
    ## f.write(f'{addr2},{addr1},{addr3},{addr4},{priv}\n')
pprint(vars(df))
print("Generated " + num_addresses + " and it took " + str(datetime.now() - startTime))

