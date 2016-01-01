import json
import pickle
import os
import datetime

with open("fio_result.json") as fio_raw:
    fio_data=json.load(fio_raw)

r_iops=[];
r_io_bytes=[];
r_io_runtime=[];
r_lat=[];
w_iops=[];
w_io_bytes=[];
w_io_runtime=[];
w_lat=[];



total_jobs=len(fio_data["jobs"])

for x in range (0,int(total_jobs)):
    r_iops.append(fio_data["jobs"][x]["read"]["iops"])
    r_io_bytes.append(fio_data["jobs"][x]["read"]["io_bytes"])
    r_io_runtime.append(fio_data["jobs"][x]["read"]["runtime"])
    r_lat.append(fio_data["jobs"][x]["read"]["lat"]["mean"])
    w_iops.append(fio_data["jobs"][x]["write"]["iops"])
    w_io_bytes.append(fio_data["jobs"][x]["write"]["io_bytes"])
    w_io_runtime.append(fio_data["jobs"][x]["write"]["runtime"])
    w_lat.append(fio_data["jobs"][x]["write"]["lat"]["mean"])



FIO_result_dict={};

for x in range (0,total_jobs):
    FIO_result_dict['Job_'+str(x)]={};
    FIO_result_dict['Job_'+str(x)]['read']={};
    FIO_result_dict['Job_'+str(x)]['read']['Total_IO_Bytes']=r_io_bytes[x]
    FIO_result_dict['Job_'+str(x)]['read']['IO/sec']=r_iops[x]
    FIO_result_dict['Job_'+str(x)]['read']['IO_runtime (millisec)']=r_io_runtime[x]
    FIO_result_dict['Job_'+str(x)]['read']['mean_IO_latenchy (microsec)']=r_lat[x]
    
    FIO_result_dict['Job_'+str(x)]['write']={};
    FIO_result_dict['Job_'+str(x)]['write']['Total_IO_Bytes']=w_io_bytes[x]
    FIO_result_dict['Job_'+str(x)]['write']['IO/sec']=w_iops[x]
    FIO_result_dict['Job_'+str(x)]['write']['IO_runtime (millisec)']=w_io_runtime[x]
    FIO_result_dict['Job_'+str(x)]['write']['mean_IO_latenchy (microsec)']=w_lat[x]



host_name = (os.popen("hostname").read().rstrip())
report_time = str(datetime.datetime.utcnow().isoformat())
os.system("mv fio_result.json "+str(host_name)+"-"+report_time+".log")
with open('./result_temp','w+')as out_fio_result:
    pickle.dump(FIO_result_dict,out_fio_result)

