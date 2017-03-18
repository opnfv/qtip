import httplib

import connexion

from qtip.base import error


def check_endpoint_for_error(resource, operation=None):
    def _decorator(func):
        def _execute(name=None):
            try:
                return func(name), httplib.OK
            except error.NotFoundError:
                return connexion.problem(
                    httplib.NOT_FOUND,
                    '{} not found'.format(resource),
                    'Requested {} `{}` not found.'
                    .format(resource.lower(), name))
            except error.ToBeDoneError:
                return connexion.problem(
                    httplib.NOT_IMPLEMENTED,
                    '{} handler not implemented'.format(operation),
                    'Requested operation `{}` on {} not implemented.'
                    .format(operation.lower(), resource.lower()))
        return _execute
    return _decorator
