.. image:: https://circleci.com/gh/pwoolvett/python_template.svg?style=shield
    :target: https://circleci.com/gh/pwoolvett/python_template
    :alt: Build Status

.. image:: https://api.codeclimate.com/v1/badges/f0f976249fae332a0bab/test_coverage
   :target: https://codeclimate.com/github/pwoolvett/python_template/test_coverage
   :alt: Test Coverage


.. image:: https://api.codeclimate.com/v1/badges/f0f976249fae332a0bab/maintainability
   :target: https://codeclimate.com/github/pwoolvett/python_template/maintainability
   :alt: Maintainability


1. clone
2. refactor "package" folder
3. enjoy!

reqs:
  poetry
  tox
  python>=3.7

for dev:
  :code:`tox -e env` creates virtualenv located at .venv

testing:

- unit / developer-required tests with pytest
- integration testing with docker-compose+pytest
- user stories testing with docker-compose+behave
