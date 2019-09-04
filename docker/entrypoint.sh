poetry config repositories.notpypi http://notpypi:8080/simple/
poetry config http-basic.notpypi username password
poetry publish --build -r notpypi
