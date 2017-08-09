# Usage

Please make sure pip, docker and docker-compose are installer on your environment.

1. Launch qtip and storperf containers.

    ```
    $ cd qtip/integration/storperf
    $ bash launch_containers.sh -t apex -n ""

    Arguments:

        -t : Installer type. For now only supports Apex.
        -n : Node name.
    ```

    Then you will get 5 containers:

    ```
    CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
    2c079d5d88bc        opnfv/qtip                    "/usr/bin/supervisord"   38 minutes ago      Up 38 minutes       5000/tcp                           qtip
    2032a16dab17        opnfv/storperf-httpfrontend   "nginx -g 'daemon ..."   38 minutes ago      Up 38 minutes       80/tcp, 0.0.0.0:5000->5000/tcp     storperf-httpfrontend
    c0d3e2763d35        schickling/swagger-ui         "sh run.sh"              39 minutes ago      Up 38 minutes       80/tcp                             storperf-swaggerui
    0e08a1968829        opnfv/storperf-reporting      "python app.py"          39 minutes ago      Up 38 minutes       0.0.0.0:5080->5000/tcp             storperf-reporting
    b92967139d8e        opnfv/storperf-master         "/usr/bin/supervisord"   39 minutes ago      Up 39 minutes       5000/tcp, 0.0.0.0:8000->8000/tcp   storperf-master
    ```

2. Prepare environment.

    ```
    $ docker exec qtip bash -c "/home/opnfv/repos/qtip/integration/storperf/prepare.sh"
    ```

    This command can create a flavor and upload a Ubuntu 16.04 image on OpenStack.

3. Run storperf job.

    ```
    $ docker exec qtip bash -c "/home/opnfv/repos/qtip/integration/storperf/start_job.sh -s stack.json -j job.json"

    Arguments:

        -s : Stack configuration json file. If not given, default_stack.json will be used.
        -j : Storperf job configuration json file. If not given, default_job.json will be used.
    ```
