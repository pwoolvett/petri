set -e

poetry add petri==${PETRI_VERSION}

poetry install

pytest tests

poetry config repositories.notpypi http://notpypi:8080/

poetry build
poetry publish -r notpypi --username ${NOT_PYPI_USERNAME} --password ${NOT_PYPI_PASSWORD}
