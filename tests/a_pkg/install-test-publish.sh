set -e

poetry config repositories.notpypi http://notpypi:8080/
poetry config http-basic.notpypi ${NOT_PYPI_USERNAME} ${NOT_PYPI_PASSWORD}

poetry add petri==${PETRI_VERSION}

poetry install

pytest tests

poetry build
poetry publish \
    -r notpypi \
    --username ${NOT_PYPI_USERNAME} \
    --password ${NOT_PYPI_PASSWORD}
