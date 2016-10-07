import json
import importlib
import sys
from utils import logger_utils

logger = logger_utils.QtipLogger('suite_result').get


def get_benchmark_result(benchmark_name, suite_name):
    benchmark_indices = importlib.import_module('{0}_benchmarks_indices'.format(suite_name))
    methodToCall = getattr(benchmark_indices, '{0}_index'.format(benchmark_name))
    return methodToCall()


def get_suite_result(suite_name):
    suite_dict = {}
    suite_bench_list = {'compute': ['DPI', 'Dhrystone', 'Whetstone', 'SSL', 'RamSpeed'],
                        'storage': ['FIO'],
                        'network': ['IPERF']}
    temp = 0
    l = len(suite_bench_list[suite_name])
    for benchmark in suite_bench_list[suite_name]:
        try:
            suite_dict[benchmark] = get_benchmark_result(benchmark.lower(), suite_name)
            temp = temp + float(suite_dict[benchmark]['index'])
        except OSError:
            l = l - 1
            pass

    if l == 0:
        logger.info("No {0} suite results found".format(suite_name))
        return False
    else:
        suite_index = temp / l
        suite_dict_f = {'index': suite_index,
                        'suite_results': suite_dict}
        with open('../../results/{0}_result.json'.format(suite_name), 'w+') as result_json:
            json.dump(suite_dict_f, result_json, indent=4, sort_keys=True)
        return True


def main():
    get_suite_result(sys.argv[1])


if __name__ == "__main__":
    main()
