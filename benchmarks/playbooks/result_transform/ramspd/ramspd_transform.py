import os
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

result = {"int_bandwidth": {"copy": intmem_copy,
                            "add": intmem_add,
                            "scale": intmem_scale,
                            "triad": intmem_triad,
                            "average": intmem_average},
          "float_bandwidth": {"copy": floatmem_copy,
                              "add": floatmem_add,
                              "scale": floatmem_scale,
                              "triad": floatmem_triad,
                              "average": floatmem_average}}

with open('./result_temp', 'w+') as result_file:
    pickle.dump(result, result_file)
