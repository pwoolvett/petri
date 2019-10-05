FROM pwoolvett/poetry-docker

COPY docker/config.toml /root/.config/pypoetry/config.toml
COPY docker/auth.toml /root/.config/pypoetry/auth.toml

WORKDIR /petri
COPY README.rst poetry.lock pyproject.toml ./
RUN poetry install --no-dev
COPY petri ./petri

RUN poetry build
ENTRYPOINT [ "poetry", "publish", "-r", "notpypi" ]
