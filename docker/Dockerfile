FROM pwoolvett/poetry-docker

WORKDIR /petri
COPY poetry.lock ./
COPY petri ./petri
COPY pyproject.toml ./
COPY README.rst ./
COPY docker/publish.sh ./

ENTRYPOINT [ "sh", "./publish.sh" ]
