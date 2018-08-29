# -*- coding: utf-8 -*-
import sys

# Get version
sys.path.insert(0, 'python/')
from ga4gh.dos import __version__  # noqa

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
    name="ga4gh_dos_schemas",
    description="GA4GH Data Object Service Schemas",
    packages=[
        "ga4gh",
        "ga4gh.dos",
        'ga4gh.dos.test'
    ],
    namespace_packages=["ga4gh"],
    url="https://github.com/ga4gh/data-object-service-schemas",
    entry_points={
        'console_scripts': [
            'ga4gh_dos_server=ga4gh.dos.server:main',
            'ga4gh_dos_client=ga4gh.dos.client:main',
        ]
    },
    package_dir={'': 'python'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'connexion==1.4.2',
        'Flask-Cors==3.0.4',
        'bravado-core==4.13.4',
        'bravado==9.2.2'
    ],
    license='Apache License 2.0',
    package_data={
        'ga4gh.dos': ['data_object_service.swagger.yaml'],
        '': ['openapi/data_object_service.swagger.yaml']
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
