FROM pwoolvett/poetry-docker

COPY docker/config.toml /root/.config/pypoetry/config.toml
COPY docker/auth.toml /root/.config/pypoetry/auth.toml
COPY docker/add_a_pkg_install_test.sh /second_order/

WORKDIR /second_order
COPY . .
RUN echo \
    '[[tool.poetry.source]]\
    \nname = "notpypi"\
    \nurl = "http://notpypi:8080/simple/"' >> pyproject.toml

# ENTRYPOINT [ "bash" ]
ENTRYPOINT [ "sh", "-c", "./add_a_pkg_install_test.sh" ]
