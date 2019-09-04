FROM python:3.6 as base

# FROM base as poetry

FROM base as app

COPY get-poetry.py .
RUN python get-poetry.py --preview --version 1.0.0a5
RUN rm get-poetry.py
RUN mkdir -p /root/.config/pypoetry/
RUN touch /root/.config/pypoetry/config.toml
ENV PATH="/root/.poetry/bin:$PATH"
RUN poetry config settings.virtualenvs.create false

WORKDIR /a_pkg
COPY . .
RUN mv ./.env.dist ./.env

RUN poetry install
RUN pytest tests
RUN poetry config repositories.notPYPI notPYPI/simple/
RUN poetry config http-basic.notPYPI username password
RUN poetry publish --build -r notPYPI
ENTRYPOINT [ "bash" ]
# RUN poetry add pytest


# ARG PYPI_USERNAME
# ARG PYPI_PASSWORD
# RUN poetry config repositories.test https://test.pypi.org/legacy/

# RUN poetry publish --username ${PYPI_USERNAME} --password ${PYPI_PASSWORD} --build --repository test
