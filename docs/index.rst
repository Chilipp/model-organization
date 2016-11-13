.. model_organization documentation master file

==========================================================
Create an argparse.ArgumentParser from function docstrings
==========================================================

.. start-badges

.. list-table::
    :stub-columns: 1
    :widths: 10 90

    * - docs
      - |docs|
    * - tests
      - |travis| |requires| |coveralls|
    * - package
      - |version| |supported-versions| |supported-implementations|

.. |docs| image:: http://readthedocs.org/projects/model-organization/badge/?version=latest
    :alt: Documentation Status
    :target: http://model-organization.readthedocs.io/en/latest/?badge=latest

.. |travis| image:: https://travis-ci.org/Chilipp/model-organization.svg?branch=master
    :alt: Travis
    :target: https://travis-ci.org/Chilipp/model-organization

.. |coveralls| image:: https://coveralls.io/repos/github/Chilipp/model-organization/badge.svg?branch=master
    :alt: Coverage
    :target: https://coveralls.io/github/Chilipp/model-organization?branch=master

.. |requires| image:: https://requires.io/github/Chilipp/model-organization/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Chilipp/model-organization/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/model-organization.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/model-organization

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/model-organization.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/model-organization

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/model-organization.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/model-organization


.. end-badges

Welcome! This package attempts to create an interface for managing the usage of
a climate model. It provides the :class:`ModelOrganization` class that manages
different experiments in projects.

Content
-------

.. toctree::
    :maxdepth: 1

    getting_started
    square
    api/model_organization
    command_line/model


.. _install:

Installation
============

Simply install it via ``pip``::

    $ pip install model-organization

Or you install it via::

    $ python setup.py install

from the `source on GitHub`_.

.. _source on GitHub: https://github.com/Chilipp/model-organization


Requirements
============
The package is based upon

- funcargparse_: used to create the command line utility.
- PyYAML_: for storing, loading and displaying the configuration
- six_: For compatibility issues between python 2 and python 3
- fasteners_: For a parallel access to the configuration files

The package has been tested for python 2.7 and 3.5.

.. _funcargparse: http://funcargparse.readthedocs.io/en/latest/
.. _PyYAML: http://pyyaml.org/wiki/PyYAML
.. _six: https://pythonhosted.org/six/
.. _fasteners: http://fasteners.readthedocs.io/en/latest/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

