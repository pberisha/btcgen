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

data = []

# Generate and write each address to the file
for i in range(int(num_addresses)):
    prvkey_dec   = keys.gen_private_key(curve.P256)
    addr1 = ice.privatekey_to_address(0, True, prvkey_dec)
    addr2 = ice.privatekey_to_address(0, False, prvkey_dec)
    addr3 = ice.privatekey_to_address(1, True, prvkey_dec)
    addr4 = ice.privatekey_to_address(2, True, prvkey_dec)
    priv = ice.btc_pvk_to_wif(prvkey_dec, False)
    data.append({addr2, priv})
    data.append({addr1, priv})
    data.append({addr3, priv})
    data.append({addr4, priv})

df_generated = pd.DataFrame(data)
print("Generated " + str(num_addresses) + " and it took " + str(datetime.now() - startTime))

#start duplicate check against real addresses with gpu acceleration

real_csv_filename = '../btcgen_data/richaddresses.csv'
output_csv_path = "../btcgen_data/result.csv"

#read richaddresses
df_real = pd.read_csv(real_csv_filename)

r_column_to_compare = df_real.columns[0]
g_column_to_compare = df_generated.columns[0]

matches = df_generated[g_column_to_compare].isin(df_real[r_column_to_compare])
df_matched = df_generated[matches]

df_matched.to_csv(output_csv_path, mode='a', index=False, header=False)
print("Duplication proces of " + str(num_addresses) + " took " + str(datetime.now() - startTime))