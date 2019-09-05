poetry config repositories.notpypi http://notpypi:8080/

touch /root/.config/pypoetry/auth.toml
poetry config http-basic.notpypi ${NOT_PYPI_USERNAME} ${NOT_PYPI_PASSWORD}
sleep 2
poetry config http-basic.notpypi ${NOT_PYPI_USERNAME} ${NOT_PYPI_PASSWORD}

poetry build
poetry publish -r notpypi --username ${NOT_PYPI_USERNAME} --password ${NOT_PYPI_PASSWORD}
