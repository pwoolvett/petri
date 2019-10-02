=====
PETRI
=====

Free your python code from 12-factor boilerplate.

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

   .. include:: examples/a_pkg/a_pkg/settings.py

  IMPORTANT: Make sure to set
  `Config.env_prefix=[package_name].upper().replace('-' ,'_')+'_'`.
  In this example, a package named `a-pkg` turns into `A_PKG_`

- Select which class of setting to use, by doing one of the folowing:

  + Set the envvar `[package_name].replace("-", "_").upper() + "_CONFIG"` to
    a defined settings class (eg: `A_PKG_CONFIG=a_pkg.settings:Production`), or

  + Use the `default_config` kwarg when instantiating `petri.Petri` (See Below)

  Of course, you can use both. Petri will attempt to load said env, and if not
  found, default to the defined kwarg.

- Instantiate `petri.Petri` form your package's `__init__.py`, like so:

   .. include:: examples/a_pkg/a_pkg/__init__.py

This allows petri to:

- Load `env_file`'s contents, if defined.
- Provide your package's metadata (version, author, etc), available in
  `pkg.meta` (lazy-loaded to avoid reading metadata files unnecessarily).
- Activate and instantiate a settings class, according to environment var and
  default, available in `pkg.settings` (https://pydantic-docs.helpmanual.io/#id5)
- Configure and expose a logger, available in `pkg.log`, which uses
  configuration defined in your settings.
