import httplib

import connexion

from qtip.base import error


def get_one_exceptions(resource):
    def _decorator(func):
        def _execute(query):
            try:
                return func(query)
            except error.NotFoundError:
                return connexion.problem(
                    httplib.NOT_FOUND,
                    '{} Not Found'.format(resource),
                    'Requested {} `{}` not found.'.format(resource, query))
        return _execute
    return _decorator
