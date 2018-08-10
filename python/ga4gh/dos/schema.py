# -*- coding: utf-8 -*-
import os.path

import swagger_spec_validator.common

cd = os.path.dirname(os.path.realpath(__file__))
SWAGGER_PATH = os.path.join(cd, 'data_object_service.swagger.yaml')


def present_schema():
    """
    Presents the OpenAPI 2.0 schema as a dictionary.
    :rvtype: dict
    """
    return swagger_spec_validator.common.read_file(SWAGGER_PATH)
