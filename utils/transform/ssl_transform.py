import os
import pickle
import datetime

openssl_version = os.popen("cat RSA_dump | head -1").read().rstrip()
rsa_512_sps = os.popen(
    "cat RSA_dump | grep  '512 bits ' | awk '{print $6}' ").read().rstrip()
rsa_512_vps = os.popen(
    "cat RSA_dump | grep  '512 bits ' | awk '{print $7}' ").read().rstrip()
rsa_1024_sps = os.popen(
    "cat RSA_dump | grep  '1024 bits ' | awk '{print $6}' ").read().rstrip()
rsa_1024_vps = os.popen(
    "cat RSA_dump | grep  '1024 bits ' | awk '{print $7}' ").read().rstrip()
rsa_2048_sps = os.popen(
    "cat RSA_dump | grep  '2048 bits ' | awk '{print $6}' ").read().rstrip()
rsa_2048_vps = os.popen(
    "cat RSA_dump | grep  '2048 bits ' | awk '{print $7}' ").read().rstrip()
rsa_4096_sps = os.popen(
    "cat RSA_dump | grep  '4096 bits ' | awk '{print $6}' ").read().rstrip()
rsa_4096_vps = os.popen(
    "cat RSA_dump | grep  '4096 bits ' | awk '{print $7}' ").read().rstrip()

aes_16B = os.popen(
    "cat AES-128-CBC_dump | grep  'aes-128-cbc  ' | awk '{print $2}' ").read().rstrip()
aes_64B = os.popen(
    "cat AES-128-CBC_dump | grep  'aes-128-cbc  ' | awk '{print $3}' ").read().rstrip()
aes_256B = os.popen(
    "cat AES-128-CBC_dump | grep  'aes-128-cbc  ' | awk '{print $4}' ").read().rstrip()
aes_1024B = os.popen(
    "cat AES-128-CBC_dump | grep  'aes-128-cbc  ' | awk '{print $5}' ").read().rstrip()
aes_8192B = os.popen(
    "cat AES-128-CBC_dump | grep  'aes-128-cbc  ' | awk '{print $6}' ").read().rstrip()

hostname = os.popen("hostname").read().rstrip()
time_stamp = str(datetime.datetime.utcnow().isoformat())

os.system("mv RSA_dump " + hostname + "-" + time_stamp + ".log")
os.system("cat AES-128-CBC_dump >> " + hostname + "-" + time_stamp + ".log")

result = {"version": [openssl_version],
          "rsa_sig": {"512_bits": rsa_512_sps,
                      "1024_bits": rsa_1024_sps,
                      "2048_bits": rsa_2048_sps,
                      "4096_bits": rsa_4096_sps,
                      "unit": "sig/sec"},
          "aes_128_cbc": {"16B_block": aes_16B,
                          "64B_block": aes_64B,
                          "256B_block": aes_256B,
                          "1024B_block": aes_1024B,
                          "8192B_block": aes_8192B,
                          "unit": "B/sec"}}

with open('./result_temp', 'w+') as result_file:
    pickle.dump(result, result_file)
