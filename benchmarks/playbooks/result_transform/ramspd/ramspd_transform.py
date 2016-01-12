import os
import json
import pickle
import datetime


intmem_copy = os.popen("cat Intmem | grep 'BatchRun   Copy' | awk '{print $4}'").read().rstrip()
intmem_scale = os.popen("cat Intmem | grep 'BatchRun   Scale' | awk '{print $4}'").read().rstrip()
intmem_add = os.popen("cat Intmem | grep 'BatchRun   Add' | awk '{print $4}'").read().rstrip()
intmem_triad = os.popen("cat Intmem | grep 'BatchRun   Triad' | awk '{print $4}'").read().rstrip()
intmem_average = os.popen("cat Intmem | grep 'BatchRun   AVERAGE' | awk '{print $4}'").read().rstrip()

print intmem_copy
print intmem_average

floatmem_copy = os.popen("cat Floatmem | grep 'BatchRun  Copy' | awk '{print $4}'").read().rstrip()
floatmem_scale = os.popen("cat Floatmem | grep 'BatchRun  Scale' | awk '{print $4}'").read().rstrip()
floatmem_add = os.popen("cat Floatmem | grep 'BatchRun  Add' | awk '{print $4}'").read().rstrip()
floatmem_triad = os.popen("cat Floatmem | grep 'BatchRun  Triad' | awk '{print $4}'").read().rstrip()
floatmem_average = os.popen("cat Floatmem | grep 'BatchRun  AVERAGE' | awk '{print $4}'").read().rstrip()

print floatmem_copy
print floatmem_average


hostname = os.popen("hostname").read().rstrip()
time_stamp = str(datetime.datetime.utcnow().isoformat())


os.system("mv Intmem " + hostname + "-" + time_stamp + ".log")
os.system("cp  Floatmem >> " + hostname + "-" + time_stamp + ".log")


result = {};

result['1. INTmem bandwidth'] = {};
result['1. INTmem bandwidth']['1. Copy (MB/s)']=intmem_copy
result['1. INTmem bandwidth']['2. Add (MB/s)']=intmem_add
result['1. INTmem bandwidth']['3. Scale (MB/s)']=intmem_scale
result['1. INTmem bandwidth']['4. Triad (MB/s)']=intmem_triad
result['1. INTmem bandwidth']['5. Average (MB/s)']=intmem_average


result['2. FLOATmem bandwidth'] = {};
result['2. FLOATmem bandwidth']['1. Copy (MB/s)']=floatmem_copy
result['2. FLOATmem bandwidth']['2. Add (MB/s)']=floatmem_add
result['2. FLOATmem bandwidth']['3. Scale (MB/s)']=floatmem_scale
result['2. FLOATmem bandwidth']['4. Triad (MB/s)']=floatmem_triad
result['2. FLOATmem bandwidth']['5. Average (MB/s)']=floatmem_average



with open('./result_temp', 'w+') as result_file:
    pickle.dump(result, result_file)


