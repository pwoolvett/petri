set -e

poetry add petri==${PETRI_VERSION} --extras color
poetry install
A_PKG_CONFIG=a_pkg.settings:Testing pytest tests
poetry build
poetry publish -r notpypi
