# -*- coding: utf-8 -*-
# -- Path setup --------------------------------------------------------------
# not required if `petri` is installed
# -- Project information -----------------------------------------------------
from petri import __meta__

project = __meta__.name
copyright = __meta__.copyright
author = __meta__.authors
version = __meta__.version
release = __meta__.release
# -- General configuration ---------------------------------------------------
# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinxcontrib.apidoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    'sphinx_autodoc_typehints',
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
]

# region  ======================= apidoc =======================
apidoc_module_dir = "../../petri"
""" The path to the module to document. This must be a path to a Python package. This path can be a path relative to the documentation source directory or an absolute path.

Required
"""
    
apidoc_output_dir = "."
"""The output directory. If it does not exist, it is created. This path is relative to the documentation source directory.

Optional, defaults to api.
"""

# apidoc_excluded_paths
    # """An optional list of modules to exclude. These should be paths relative to apidoc_module_dir. fnmatch-style wildcarding is supported.

    # Optional, defaults to [].
    # """

apidoc_separate_modules = True
"""Put documentation for each module on its own page. Otherwise there will be one page per (sub)package.

Optional, defaults to False.
"""

# apidoc_toc_file
# """Filename for a table of contents file. Defaults to modules. If set to False, apidoc will not create a table of contents file.

# Optional, defaults to None.
# """

apidoc_module_first = True
"""When set to True, put module documentation before submodule documentation.

Optional, defaults to False.
"""

apidoc_extra_args = [
    "--force",
    "--private",
    "--ext-doctest",
    "--ext-intersphinx",
    "--ext-todo",
    "--ext-coverage",
    "--ext-imgmath",
    "--ext-mathjax",
    "--ext-ifconfig",
    "--ext-viewcode",
    "--ext-githubpages",
    "-e",
    "-M",
    "--tocfile",
    "index"
]
"""Extra arguments which will be passed to sphinx-apidoc. These are placed after flags and before the module name.

Optional, defaults to [].
"""
# endregion ===================== apidoc =======================


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"
# The master toctree document.
master_doc = "index"
# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list = []
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None
# -- Options for HTML output -------------------------------------------------
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["static"]
# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}
# -- Options for HTMLHelp output ---------------------------------------------
# Output file base name for HTML help builder.
htmlhelp_basename = "petridoc"
# -- Options for LaTeX output ------------------------------------------------
latex_elements: dict = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "myproject.tex", "myproject Documentation", "PW", "manual")
]
# -- Options for manual page output ------------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "myproject", "myproject Documentation", [author], 1)]
# -- Options for Texinfo output ----------------------------------------------
# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "myproject",
        "myproject Documentation",
        author,
        "myproject",
        "One line description of project.",
        "Miscellaneous",
    )
]
# -- Options for Epub output -------------------------------------------------
# Bibliographic Dublin Core info.
epub_title = project
# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''
# A unique identification for the text.
#
# epub_uid = ''
# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]
# -- Extension configuration -------------------------------------------------
# -- Options for intersphinx extension ---------------------------------------
# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"https://docs.python.org/": None}
# -- Options for todo extension ----------------------------------------------
# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
