poetry config repositories.notpypi http://notpypi:8080/

poetry config http-basic.notpypi ${NOT_PYPI_USERNAME} ${NOT_PYPI_PASSWORD}

poetry build
poetry publish \
    --username ${NOT_PYPI_USERNAME} \
    --password ${NOT_PYPI_PASSWORD} \
    -r notpypi
