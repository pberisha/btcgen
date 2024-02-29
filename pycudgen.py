import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy as np
import hashlib
import binascii
import csv

# CUDA kernel code to generate private keys and corresponding Bitcoin addresses
kernel_code = """
#include <stdint.h>
#include <stdio.h>
#include <openssl/sha.h>
#include <openssl/ecdsa.h>
#include <openssl/ripemd.h>
#include <openssl/bn.h>

__global__ void generate_keys(uint8_t* keys, const int num_keys) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < num_keys) {
        EC_KEY* eckey = EC_KEY_new_by_curve_name(NID_secp256k1);
        EC_KEY_generate_key(eckey);
        const BIGNUM* priv_key = EC_KEY_get0_private_key(eckey);
        const EC_POINT* pub_key_point = EC_KEY_get0_public_key(eckey);
        const EC_GROUP* group = EC_KEY_get0_group(eckey);
        BIGNUM* x = BN_new();
        BIGNUM* y = BN_new();
        EC_POINT_get_affine_coordinates_GFp(group, pub_key_point, x, y, NULL);
        BN_bn2bin(priv_key, keys + i * 32);
        BN_bn2bin(x, keys + num_keys * 32 + i * 32);
        BN_bn2bin(y, keys + 2 * num_keys * 32 + i * 32);
        BN_free(x);
        BN_free(y);
        EC_KEY_free(eckey);
    }
}
"""

def generate_keys_with_cuda(num_keys):
    # Compile the CUDA kernel
    mod = SourceModule(kernel_code, options=['-arch=sm_61'])  # Specify a compatible architecture, e.g., 'sm_61'
    generate_keys_kernel = mod.get_function("generate_keys")

    # Allocate memory buffers for keys
    keys = np.zeros((num_keys, 96), dtype=np.uint8)
    keys_gpu = cuda.mem_alloc(keys.nbytes)
    
    # Execute kernel
    block_size = 256
    grid_size = (num_keys + block_size - 1) // block_size
    generate_keys_kernel(keys_gpu, np.int32(num_keys), block=(block_size, 1, 1), grid=(grid_size, 1))

    # Retrieve results
    cuda.memcpy_dtoh(keys, keys_gpu)
    
    return keys

def generate_address(priv_key):
    sk = hashlib.sha256(binascii.unhexlify(priv_key)).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(binascii.unhexlify(priv_key)).digest())
    return ripemd160.hexdigest()

def save_to_csv(keys, num_keys):
    with open('bitcoin_addresses.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Private Key', 'Address'])
        for i in range(num_keys):
            priv_key = keys[i][:32].tobytes().hex()
            address = generate_address(priv_key)
            writer.writerow([priv_key, address])

# Example usage
num_keys = 10
keys = generate_keys_with_cuda(num_keys)
save_to_csv(keys, num_keys)
print("Bitcoin addresses saved to bitcoin_addresses.csv")

