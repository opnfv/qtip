##############################################################################
# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger

import legacy.api.router.mapper as mapper

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1', description='QTIP API specs')


def add_routers():
    for (handler, url) in mapper.mappers:
        api.add_resource(handler, url)


def main():
    add_routers()
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
