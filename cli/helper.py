import os


def fetch_root():
    return os.path.join(os.path.dirname(__file__), os.pardir, 'benchmarks/')
