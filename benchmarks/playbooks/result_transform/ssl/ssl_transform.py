import os
import json
import pickle
import datetime

#total_cpu=os.popen("cat $HOME/tempD/nDPI/example/result.txt | tail -1").read()

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

<<<<<<< HEAD

=======
#    def get_nova_client(self):
>>>>>>> 5a7dcc0... Networking testcases for QTIP Framework
hostname = os.popen("hostname").read().rstrip()
time_stamp = str(datetime.datetime.utcnow().isoformat())


os.system("mv RSA_dump " + hostname + "-" + time_stamp + ".log")
os.system("cat AES-128-CBC_dump >> " + hostname + "-" + time_stamp + ".log")

<<<<<<< HEAD
=======
#      if self._glance_client is None:
##          keystone = self.get_keystone_client()
#         nova = client.Client('2', token = keystone.auth_token)

>>>>>>> 5a7dcc0... Networking testcases for QTIP Framework

result = {}

result['1. Version'] = [openssl_version]
result['2. RSA singatures'] = {}
result['2. RSA singatures']['1. 512 bits (sign/s)'] = [rsa_512_sps]
result['2. RSA singatures']['2. 1024 bits (sign/s)'] = [rsa_1024_sps]
result['2. RSA singatures']['3. 2048 bits (sign/s)'] = [rsa_2048_sps]
result['2. RSA singatures']['4. 4096 bits (sign/s)'] = [rsa_4096_sps]

result['3. AES-128-cbc throughput'] = {}
result['3. AES-128-cbc throughput']['1. 16 Bytes block (B/sec)'] = [aes_16B]
result['3. AES-128-cbc throughput']['2. 64 Bytes block (B/sec)'] = [aes_64B]
result['3. AES-128-cbc throughput']['3. 256 Bytes block (B/sec)'] = [aes_256B]
result['3. AES-128-cbc throughput']['4. 1024 Bytes block (B/sec)'] = [aes_1024B]
result['3. AES-128-cbc throughput']['5. 16 Bytes block (B/sec)'] = [aes_8192B]


with open('./result_temp', 'w+') as result_file:
    pickle.dump(result, result_file)

<<<<<<< HEAD

=======
# print json.dumps(result, indent=4, sort_keys=True)
# print result.items()
>>>>>>> 5a7dcc0... Networking testcases for QTIP Framework
