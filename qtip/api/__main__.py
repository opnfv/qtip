##############################################################################
# Copyright (c) 2017 akhil.batra@research.iiit.ac.in and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import connexion
import os


swagger_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'swagger/'))


def get_app():
    app = connexion.App(__name__, specification_dir=swagger_dir)
    app.add_api('swagger.yaml', base_path='/v1.0', strict_validation=True)
    return app


def main():
    app = get_app()
    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()
