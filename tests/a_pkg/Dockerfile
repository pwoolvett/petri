FROM pwoolvett/poetry-docker

WORKDIR /a_pkg
COPY . ./
RUN mv .env.dist .env
ENTRYPOINT [ "sh", "./install-test-publish.sh" ]
