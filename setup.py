# -*- coding: utf-8 -*-
import sys

# Get version
sys.path.insert(0, 'python/')
from ga4gh.drs import __version__  # noqa

# First, we try to use setuptools. If it's not available locally,
# we fall back on ez_setup.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

with open("README.md") as readmeFile:
    long_description = readmeFile.read()


setup(
    name="ga4gh_drs_schemas",
    description="GA4GH Data Repository Service Schemas",
    packages=[
        "ga4gh",
        "ga4gh.drs",
        'ga4gh.drs.test'
    ],
    namespace_packages=["ga4gh"],
    url="https://github.com/ga4gh/data-repository-service-schemas",
    entry_points={
        'console_scripts': [
            'ga4gh_drs_server=ga4gh.drs.server:main',
            'ga4gh_drs_client=ga4gh.drs.client:main',
        ]
    },
    package_dir={'': 'python'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'connexion==1.4.2',
        'Flask-Cors==3.0.9',
        'bravado-core==4.13.4',
        'bravado==9.2.2',
        'jsonschema>=2.6.0,<3',
        # These dependencies listed below are dependencies of jsonschema[format].
        # We specify them here manually because of pypa/pip#4957. In summary,
        # between the dependencies listed above, both jsonschema and
        # jsonschema[format] are identified as sub-dependencies. Due to a bug in
        # pip, only the former is installed, and not the latter, causing
        # installation to fail silently on some setups. (Related to #137.)
        'jsonpointer>1.33',
        'rfc3987',
        'strict-rfc3339',
        'webcolors'
    ],
    license='Apache License 2.0',
    package_data={
        'ga4gh.drs': ['data_repository_service.swagger.yaml'],
        '': ['openapi/data_repository_service.swagger.yaml']
    },
    zip_safe=False,
    author="Global Alliance for Genomics and Health",
    author_email="theglobalalliance@genomicsandhealth.org",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    version=__version__,
    keywords=['genomics'],
)
