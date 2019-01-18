# -*- coding: utf-8 -*-
import datetime
import functools
import hashlib
import random
import unittest
import uuid


def test_requires(*operations):
    """
    This is a decorator that identifies what DOS operations a given test
    case uses (where each DOS operation is named by its `operationId` in
    the schema, e.g. ListBundles, UpdateObject, GetServiceInfo,
    etc.) and skips them if the operation is not supported by the
    implementation under test.

    For example, given this test setup::

        class Test(AbstractComplianceTest):
            supports = ['UpdateBundles']

            @test_requires('UpdateBundles')
            def test_update_data_bundles(self):
                self.drs_request('PUT', '/databundles/1234')

            @test_requires('ListBundles', 'UpdateBundles')
            def test_list_and_update_data_bundles(self):
                self.drs_request('GET', '/databundles')
                self.drs_request('PUT', '/databundles/1234')

    ``test_update_data_bundles`` would run and ``test_list_and_update_data_bundles``
    would be skipped.

    :param str \*operations: the operations supported by the decorated
                             test case
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self):
            unsupported = [op for op in operations if op not in self.supports]
            if unsupported:
                raise unittest.SkipTest("not supported: " + ", ".join(unsupported))
            return func(self)
        return wrapper
    return decorator


class DataRepositoryServiceTest(unittest.TestCase):
    @staticmethod
    def generate_objects(amount):
        """
        Yields a specified number of data objects with random attributes.

        :param int amount: the amount of data objects to generate
        """
        # Defines sane default random values for each field type. The
        # field types are defined in the schema and manually assigned here.
        # They are specified as lambdas so that we can generate a new
        # value each time, instead of having a single value for each
        # invocation of :meth:`generate_data_objects`.
        types = {
            # uuid4() produces UUIDs that are easier to quickly
            # differentiate visually, as opposed to uuid1() which
            # produces UUIDs based on the hostname and current time.
            # (It doesn't matter too much but it's a nice convenience
            # thing to have.)
            'string': lambda: str(uuid.uuid4()),
            # `long`
            'str-int64': lambda: str(random.randint(-(2**63) + 1, 2**63 - 1)),
            # Swagger expects a RFC 3339 compliant datetime object.
            # See https://stackoverflow.com/a/8556555
            'str-date-time': lambda: datetime.datetime.utcnow().isoformat('T') + 'Z'
        }
        for _ in range(amount):
            yield {
                'id': types['string'](),
                'name': types['string'](),
                # `size` can't be negative, but there's a possibility that
                # not calling :func:`abs` on the 'size' key could result in
                # a really entertaining bug down the line so I'm going to
                # leave it like that
                'size': types['str-int64'](),
                'created': types['str-date-time'](),
                'updated': types['str-date-time'](),
                'version': types['string'](),
                'mime_type': types['string'](),
                'checksums': [{
                    # Encode for Python 3 compat
                    'checksum': hashlib.md5(types['string']().encode('utf-8')).hexdigest(),
                    # I believe that this field will soon become an `enum` in the schema.
                    # Ideally, the available choices should be pulled from the schema...
                    'type': random.choice(['md5', 'multipart-md5', 'sha256', 'sha512'])
                }],
                'urls': [
                    {'url': types['string']()},
                    {'url': types['string']()}
                ],
                'description': types['string'](),
                'aliases': [types['string']()],
            }

    @staticmethod
    def generate_bundles(amount):
        """
        Yields a specified number of data bundles with random attributes.

        :param int amount: the amount of data bundles to generate
        """
        for bdl in DataRepositoryServiceTest.generate_objects(amount):
            del bdl['name']
            del bdl['size']
            del bdl['mime_type']
            del bdl['urls']
            # See :var:`generate_data_objects.types` above
            bdl['object_ids'] = [str(uuid.uuid4()), str(uuid.uuid4())]
            yield bdl
