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

WORKDIR /petri
COPY poetry.lock ./
COPY petri ./petri
COPY pyproject.toml ./
COPY README.rst ./
COPY docker/entrypoint.sh ./

# RUN poetry install
# RUN pytest tests
ENTRYPOINT [ "sh", "./entrypoint.sh" ]
# ENTRYPOINT [ "bash" ]
# RUN poetry add pytest


# ARG PYPI_USERNAME
# ARG PYPI_PASSWORD
# RUN poetry config repositories.test https://test.pypi.org/legacy/

# RUN poetry publish --username ${PYPI_USERNAME} --password ${PYPI_PASSWORD} --build --repository test
