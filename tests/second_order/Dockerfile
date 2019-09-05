FROM pwoolvett/poetry-docker

WORKDIR /second_order
COPY . ./
RUN mv .env.dist .env
ENTRYPOINT [ "sh", "./install-test.sh" ]
