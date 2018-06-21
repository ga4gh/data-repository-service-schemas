# -*- coding: utf-8 -*-
import os
import unittest

import yaml


class TestPackage(unittest.TestCase):
    @classmethod
    def get_spec_version(cls, filename):
        with open(filename, 'r') as f:
            spec = yaml.safe_load(f)
        return spec['info']['version']

    def test_version_consensus(self):
        from ga4gh.dos import __version__
        cwd = os.path.dirname(os.path.realpath(__file__))
        spec_dir = os.path.join(cwd, "../../openapi")
        for f in os.listdir(spec_dir):
            assert __version__ == self.get_spec_version(os.path.join(spec_dir, f))
