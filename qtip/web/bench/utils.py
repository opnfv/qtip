import os
import sys
from subprocess import Popen, PIPE, STDOUT
import shutil
from django.http import HttpResponse


def print_http_response(f):
    """ Wraps a python function that prints to the console, and
    returns those results as a HttpResponse (HTML)"""

    class WritableObject:
        def __init__(self):
            self.content = []
        def write(self, string):
            self.content.append(string)

    def new_f(*args, **kwargs):
        printed = WritableObject()
        sys.stdout = printed
        f(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return HttpResponse(['<BR>' if c == '\n' else c for c in printed.content ])
    return new_f


def run(repo):
    if os.path.exists(repo.name):
        shutil.rmtree(repo.name)
    os.mkdir(repo.name)
    os.chdir(repo.name)
    output = Popen(("git clone "+repo.git_link+" .").split(), stdout=PIPE, stderr=STDOUT)
    for line in output.stdout:
        yield line
    output.wait()
    output = Popen("ansible-playbook run.yml".split(), stdout=PIPE, stderr=STDOUT)
    for line in output.stdout:
        yield line
    os.chdir("../")
