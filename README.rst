Dimension Data CLI
==================
.. image:: https://travis-ci.org/DimensionDataDevOps/didata_cli.svg?branch=master
    :target: https://travis-ci.org/DimensionDataDevOps/didata_cli

.. image:: https://badge.fury.io/py/didata_cli.svg
    :target: https://badge.fury.io/py/didata_cli

A CLI tool to interact with the Dimension Data Cloud

* Documentation: `didata_cli at ReadTheDocs`_
* Python package: `didata_cli at PyPi`_
* Source code: `didata_cli at GitHub`_
* Free software: `Apache License (2.0)`_

Installation
------------

Installation via `pip`_::

    pip install didata_cli

It is highly recommended to also take the LATEST version of `libcloud`_::

    pip install git+https://github.com/apache/libcloud.git@trunk --upgrade


QuickStart
----------

To see all the commands::

    didata --help

The easiest way to start using the CLI is to export environment variables for username and password::

    export DIDATA_USER='cloud_user'
    export DIDATA_PASSWORD='cloud_password'


You may also want to specify a region (Default is dd-na)::

    export DIDATA_REGION='dd-eu'

From there as a first command to list servers::

    didata server list

Contributing
------------

1. Fork it ( https://github.com/DimensionDataDevOps/didata_cli/fork  )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request


.. _LICENSE: https://github.com/DimensionDataDevOps/master/blob/trunk/LICENSE

.. _pip: http://www.pip-installer.org/en/latest/
.. _`libcloud`: http://libcloud.readthedocs.org/en/latest/
.. _`didata_cli at ReadTheDocs`: https://didata_cli.readthedocs.org
.. _`didata_cli at PyPi`: https://pypi.python.org/pypi/didata_cli
.. _`didata_cli at GitHub`: https://github.com/DimensionDataDevOps/didata_cli
.. _`Apache License (2.0)`: http://www.apache.org/licenses/LICENSE-2.0
