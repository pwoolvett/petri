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

* Dotenv file handling using `python-dotenv <https://pypi.org/project/python-dotenv>`_.
* Package metadata (for installed packages), using `importlib-metadata <https://pypi.org/project/importlib-metadata>`_.
* Settings using `pydantic <https://pypi.org/project/pydantic>`_.
* Logging config using `structlog <https://pypi.org/project/structlog>`_.
* Environment switching (prod/dev/test) handling via ENV environment variable.


.. image:: assets/demo.gif
 :target: https://asciinema.org/a/3vc6LraDAy2v7KQvEoKGRv4sF
 :alt: Sample petri usage

Install
-------

Install using poetry ``poetry add petri`` or pip ``pip install petri``.

Optionally, also install the ``color`` extra for colored logs using `colorama <https://pypi.org/project/colorama>`_.

Usage
-----

* Define configuration setting(s) and instantiate ``petri.Petri``:

.. code-block:: python

   #  my_package/__init__.py

   from petri import Petri
   from petri.settings import BaseSettings
   from petri.loggin import LogFormatter, LogLevel


   class Settings(BaseSettings):
       class Config:
           env_prefix = "MY_PKG_"  # VERY IMPORTANT!!!
       # define common settings here

   class Production(Settings):
       LOG_FORMAT = LogFormatter.JSON
       LOG_LEVEL = LogLevel.TRACE


   class Development(Settings):
       LOG_FORMAT = LogFormatter.COLOR  # requires colorama
       LOG_LEVEL = LogLevel.WARNING


   pkg = Petri(__file__)

   # demo logs
   pkg.log.info("log away info level",mode=pkg.settings, version=pkg.meta.version)
   pkg.log.warning("this will show", kewl=True)

.. note::

   You **must** define ``Config.env_prefix`` inside your setting class
   (see above). This allows `petri` to select settings class using envvars.

   As an example, a package named ``my-pkg`` should have its setting(s) classes:

   1. Inherit from ``petri.BaseSettings``
   2. Contain a ``Config`` subclass (just like for ``pydantic``'s), with its
      ``env_prefix`` set to  ``"MY_PKG_"``.


   The code used should be compatible with:

     ``Config.env_prefix=[package_name].upper().replace('-' ,'_')+'_'``.

     (See `petri.Petri.pkg_2_envvar`.)

* [OPTIONAL] Define an environment variable named `env_file`, to feed
   additional envs. Its value must be the path to a valid, existing file.

* Select which of your settings classes to use, by doing one of the folowing:

   + Point the selector envvar (eg: for `a-pkg`, this would be
     `A_PKG_CONFIG=a_pkg.settings:Production`, see `petri.Petri.pkg_2_envvar`),
     or

   + Use the `default_config` kwarg when instantiating `petri.Petri`
     (See below)

   Of course, you can use both. Petri will attempt to load said env, and if not
   found, default to the defined kwarg.

Additional Info
---------------

- Load `env_file`'s contents, if defined.
- Provide your package's metadata (version, author, etc), available in
  `pkg.meta` (lazy-loaded to avoid reading metadata files unnecessarily).
- Activate and instantiate a settings class, according to environment var and
  default, available in `pkg.settings` (https://pydantic-docs.helpmanual.io/#id5)
- Configure and expose a logger, available in `pkg.log`, which uses
  configuration defined in your settings.

-----

For more info, check the `docs <https://petri.rtfd.org>`_.
