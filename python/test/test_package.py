# -*- coding: utf-8 -*-
import os
import unittest

import swagger_spec_validator
import yaml


class TestPackage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cwd = os.path.dirname(os.path.realpath(__file__))
        cls.spec_dir = os.path.join(cwd, "../../openapi")

    @classmethod
    def get_spec_version(cls, filename):
        with open(filename, 'r') as f:
            spec = yaml.safe_load(f)
        return spec['info']['version']

    def test_version_consensus(self):
        from ga4gh.dos import __version__
        for f in os.listdir(self.spec_dir):
            assert __version__ == self.get_spec_version(os.path.join(self.spec_dir, f))

    def test_schema_validity(self):
        """Check to make sure that the Swagger schema specification is
        valid by running it through the online validator. If the schema
        is valid, the online validator will return 200 OK and an empty
        JSON response."""
        path = os.path.join(self.spec_dir, 'data_object_service.swagger.yaml')
        swagger_spec_validator.validate_spec_url('file://' + os.path.abspath(path))

