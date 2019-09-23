=====
PETRI
=====

Summary
-------
Avoid boilerplate python code.

Importing petri automagically equips your app/pacakage with:

* Dotenv file handling using python-dotenv.
* Package metadata (for installed packages), using importlib_metadata.
* Settings using pydantic.
* Logging config using logzero + autologging.
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

Define dev/prod/test settings:

  .. include:: examples/a_pkg/a_pkg/settings.py

IMPORTANT: Make sure to set
`Config.env_prefix=[package_name].upper().replace('-' ,'_')+'_'`.
In this example, `a-pkg` turns into `A_PKG_`

Instantiate `petri.Petri` form your package's `__init__.py`, like so:

  .. include:: examples/a_pkg/a_pkg/__init__.py

Under the hood, petri takes care of the following:

- If the environment variable `env_file` is set, petri will load its contents.
- Your package's metadata (version, author, etc) is now available in
  `pkg.meta` (lazy-loaded to avoid reading files unnecessarily).
- Select settings: either
  (a) Set the envvar `[package_name].replace("-", "_").upper() + "_CONFIG"` to
  a defined settings class (eg: `A_PKG_CONFIG=a_pkg.settings:Production`), or
  (b) Use the `default_config` kwarg when instantiating `petri.Petri`.
  (Of course, you can use both...)
- Settings are available in `pkg.settings` (https://pydantic-docs.helpmanual.io/#id5)
