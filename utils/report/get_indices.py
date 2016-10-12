import json


def get_index(suite):
    with open('../../results/' + suite + '.json') as result_file:
        result_djson = json.load(result_file)
        index = result_djson['index']
    return index
