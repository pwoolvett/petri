=====
PETRI
=====

petri: free your python code from 12-factor boilerplate.
--------------------------------------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 0

   * - Python Version
     - .. image:: https://img.shields.io/pypi/pyversions/petri
        :target: https://www.python.org/downloads/
        :alt: Python Version
   * - Code Style
     - .. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/ambv/black
        :alt: Code Style
   * - Release
     - .. image:: https://img.shields.io/pypi/v/petri
        :target: https://pypi.org/project/petri/
        :alt: PyPI
   * - Downloads
     - .. image:: https://img.shields.io/pypi/dm/petri
        :alt: PyPI - Downloads
   * - Build Status
     - .. image:: https://github.com/pwoolvett/petri/workflows/publish_wf/badge.svg
        :target: https://github.com/pwoolvett/petri/actions
        :alt: Build Status
   * - Docs
     - .. image:: https://readthedocs.org/projects/petri/badge/?version=latest
        :target: https://petri.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
   * - Maintainability
     - .. image:: https://api.codeclimate.com/v1/badges/4a883c99f3705d3390ee/maintainability
        :target: https://codeclimate.com/github/pwoolvett/petri/maintainability
        :alt: Maintainability
   * - License
     - .. image:: https://img.shields.io/badge/license-Unlicense-blue.svg
        :target: http://unlicense.org/
        :alt: License: Unlicense
   * - Coverage
     - .. image:: https://api.codeclimate.com/v1/badges/4a883c99f3705d3390ee/test_coverage
        :target: https://codeclimate.com/github/pwoolvett/petri/test_coverage
        :alt: Test Coverage
   * - Deps
     - .. image:: https://img.shields.io/librariesio/github/pwoolvett/petri
        :alt: Libraries.io dependency status for GitHub repo


------------

Summary
-------

Importing petri equips your app/pacakage with:

* Dotenv file handling using python-dotenv.
* Package metadata (for installed packages), using importlib_metadata.
* Settings using pydantic.
* Logging config using structlog.
* Environment switching (prod/dev/test) handling via ENV environment variable.

Install
-------

Install using `poetry` or `pip`:

- Poetry::

    poetry add petri

- pip::

    pip install petri

Usage
-----

- [OPTIONAL] Define an environment variable named `env_file`, to feed
  additional envs. Its value must be the path to a valid, existing file.

- Define dev/prod/test settings:

  .. code:: python

      from petri.settings import BaseSettings


      class Settings(BaseSettings):
          class Config:  # pylint: disable=missing-docstring,too-few-public-methods
              env_prefix = "A_PKG_"


      class Production(Settings):
          ENV = "production"


      class Development(Settings):
          ENV = "development"


      class Testing(Settings):
          ENV = "testing"


  IMPORTANT: In your base class, define ``Config.env_prefix``. For example, a package
  named `a-pkg` turns into `A_PKG_`. The code used should be compatible with:
  `Config.env_prefix=[package_name].upper().replace('-' ,'_')+'_'`.

- Select which class of setting to use, by doing one of the folowing:

  + Set the envvar `[package_name].replace("-", "_").upper() + "_CONFIG"` to
    a defined settings class (eg: `A_PKG_CONFIG=a_pkg.settings:Production`), or

  + Use the `default_config` kwarg when instantiating `petri.Petri` (See Below)

  Of course, you can use both. Petri will attempt to load said env, and if not
  found, default to the defined kwarg.

- Instantiate `petri.Petri` form your package's `__init__.py`, like so:

   .. code:: python

      """A package: sample petri usage"""

      from petri import Petri

      pkg = Petri(__file__)

      __version__ = "1.2.3"


This allows petri to:

- Load `env_file`'s contents, if defined.
- Provide your package's metadata (version, author, etc), available in
  `pkg.meta` (lazy-loaded to avoid reading metadata files unnecessarily).
- Activate and instantiate a settings class, according to environment var and
  default, available in `pkg.settings` (https://pydantic-docs.helpmanual.io/#id5)
- Configure and expose a logger, available in `pkg.log`, which uses
  configuration defined in your settings.
