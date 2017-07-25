# usage

Please make sure pip, docker and docker-compose are installer on your environment.

```
storperf.sh -t installer_type -i installer_ip -s stack_json_file -j job_json_file

options:
    -t : installer type. For now only supports Apex.
    -i : installer ip address.
    -s : Stack configuration json file. Default: default_stack.json.
    -j : Storperf job configuration json file. Default: default_job.json.
```