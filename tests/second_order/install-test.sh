set -e

poetry build
poetry publish -r notpypi --username ${NOT_PYPI_USERNAME} --password ${NOT_PYPI_PASSWORD}

poetry add a_pkg==1.2.3

poetry install

pytest tests
