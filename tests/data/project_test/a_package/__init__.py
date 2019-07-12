# -*- coding: utf-8 -*-
"""sample python module using petri"""

from petri import initialize

__meta__, DOTENV_LOCATION, SETTINGS, LOGGER, _ = initialize(
    __file__, "a_package"
)

assert __meta__.release == "pre-alpha"
assert __meta__.maintainer == "Maintainer Name <maintainer@mail.com>"
assert __meta__.copyright == "A copyright"
assert __meta__.url == "www.a_package.com"
assert __meta__.license == "A License"
assert __meta__.name == "a_package"
assert __meta__.version == "1.2.3"
assert __meta__.description == "A description"
assert __meta__.readme == "README.rst"

assert __meta__.authors == ["Author Name <author@mail.com>"]
