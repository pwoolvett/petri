set -e

poetry add a_pkg==1.2.3
poetry install
SECOND_ORDER_CONFIG=a_pkg.settings:Testing A_PKG_CONFIG=a_pkg.settings:Testing pytest tests
