FROM python:3.6 as base

# FROM base as poetry

FROM base as app

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:$PATH"
RUN poetry config settings.virtualenvs.create false
RUN poetry self:update --preview 1.0.0a5

WORKDIR /app
COPY . .
RUN mv ./.env.dist ./.env
RUN poetry install

ARG PYPI_USERNAME
ARG PYPI_PASSWORD
RUN poetry config repositories.test https://test.pypi.org/legacy/

RUN poetry publish --username ${PYPI_USERNAME} --password ${PYPI_PASSWORD} --build --repository test

# ENTRYPOINT [ "bash" ]
