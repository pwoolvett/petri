FROM pwoolvett/poetry-docker

COPY docker/config.toml /root/.config/pypoetry/config.toml
COPY docker/auth.toml /root/.config/pypoetry/auth.toml
COPY docker/add_petri_install_test_build_publish.sh /a_pkg/

WORKDIR /a_pkg
COPY . .
RUN echo \
    '[[tool.poetry.source]]\
    \nname = "notpypi"\
    \nurl = "http://notpypi:8080/simple/"' >> pyproject.toml

# ENTRYPOINT [ "bash" ]
ENTRYPOINT [ "sh", "-c", "./add_petri_install_test_build_publish.sh" ]
