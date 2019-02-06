.. image:: https://travis-ci.org/pwoolvett/petri.svg?branch=master
    :target: https://travis-ci.org/pwoolvett/petri
    :alt: Build Status

.. image:: https://api.codeclimate.com/v1/badges/f0f976249fae332a0bab/test_coverage
   :target: https://codeclimate.com/github/pwoolvett/petri/test_coverage
   :alt: Test Coverage


.. image:: https://api.codeclimate.com/v1/badges/f0f976249fae332a0bab/maintainability
   :target: https://codeclimate.com/github/pwoolvett/petri/maintainability
   :alt: Maintainability


reqs:
  poetry
  tox
  python>=3.6

for devs:
  :code:`tox -e venv` creates virtualenv located at .venv

  :code:`tox -e venv` creates virtualenv located at .venv

testing:

- unit / developer-required tests with pytest
- integration testing with docker-compose+pytest
- user stories testing with docker-compose+behave
