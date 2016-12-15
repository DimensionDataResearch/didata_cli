# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from setuptools import setup, find_packages

wargs = {}
requires = ['click',
            'apache-libcloud>=1.4.0',
            'tabulate']

# python 2.7 hackery
if sys.version_info <= (3, 0):
    requires.extend(
        ["future"]
    )

setup(
    author="Jeff Dunham",
    author_email="jeff.dunham@itaas.dimensiondata.com",
    description="A CLI to interact with the Dimension Data Cloud API",
    license='Apache License (2.0)',
    url="https://www.dimensiondata.com/",
    name="didata_cli",
    version="0.3.0",
    packages=find_packages(exclude=["contrib", "docs", "tests*", "tasks", "venv"]),
    install_requires=requires,
    setup_requires=[],
    classifiers=[
                'Development Status :: 4 - Beta',
                'License :: OSI Approved :: Apache Software License',
                'Intended Audience :: End Users/Desktop',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3.4',
    ],
    dependency_links = ['https://github.com/apache/libcloud/tarball/trunk#egg=apache-libcloud-1.4.0-66'],
    entry_points='''
        [console_scripts]
        didata=didata_cli.cli:cli
    ''',
)
