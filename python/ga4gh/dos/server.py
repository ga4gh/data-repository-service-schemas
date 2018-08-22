# -*- coding: utf-8 -*-
"""
DOS Demonstration Server

Running this server will start an ephemeral Data Object Service (its registry
contents won't be saved after exiting). It uses the connexion module
to translate the OpenAPI schema into named controller functions.

These functions are described in :mod:`ga4gh.dos.controllers` and
are meant to provide a simple implementation of DOS.
"""
import connexion
from flask_cors import CORS

# These are imported by name by connexion so we assert it here.
from ga4gh.dos.controllers import *  # noqa
from ga4gh.dos.schema import SWAGGER_PATH


def configure_app():
    # The model name has to match what is in
    # tools/prepare_swagger.sh controller.
    app = connexion.App(
        "ga4gh.dos.server",
        swagger_ui=True,
        swagger_json=True)
    app.add_api(SWAGGER_PATH)

    CORS(app.app)
    return app


def main():
    app = configure_app()
    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
