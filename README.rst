.. image:: https://travis-ci.org/pwoolvett/petri.svg?branch=master
    :target: https://travis-ci.org/pwoolvett/petri
    :alt: Build Status

.. image:: https://readthedocs.org/projects/petri/badge/?version=latest
   :target: https://petri.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://api.codeclimate.com/v1/badges/f0f976249fae332a0bab/test_coverage
   :target: https://codeclimate.com/github/pwoolvett/petri/test_coverage
   :alt: Test Coverage


.. image:: https://api.codeclimate.com/v1/badges/f0f976249fae332a0bab/maintainability
   :target: https://codeclimate.com/github/pwoolvett/petri/maintainability
   :alt: Maintainability

.. image:: https://img.shields.io/badge/python%20version-3.6.7-275479.svg
   :target: https://img.shields.io/badge/python%20version-3.6.7-275479.svg
   :alt: Python Version

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Code Style


Summary
-------
Avoid boilerplate python code.

Importing petri automagically equips your script/pacakage with:

* settings using pydantic.
* dotenv file handling using python-dotenv.
* logging config using logzero&autologging.
* project metadata from a pyproject.toml file.
* environment (prod/dev/test) handling via ENV environment variable.

Screenshots
-----------

.. image:: static/screenshots/api.png


Code Example
------------

* see tests/data folder


Requirements
------------

- Usage requirements

   + python>=3.6

- Development requirements

   + tox
   + poetry (recommended)


Installation
------------

- pip install petri

Testing
-------

- run `tox -e venv` to create an appropiate virtualenv
- `tox` to run the full test suite


Contribute
----------

- Development
   
   + Make sure to pass tox tests (including those with `--runslow`).
   + For tests design, you can use use ´@pytest.mark.incremental´ and  ´@pytest.mark.slow´. See "catalogo_db/tests/conftest.py"
   + If the requirements change, make sure to re-build all images

- Versioning
   
   + Use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/pwoolvett/petri/tags).

Support
-------

If you are having issues, please file an issue in github.
