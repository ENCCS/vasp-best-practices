# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

# -- Project information -----------------------------------------------------

project = "VASP Best Practices 2027"
author = "The contributors"
copyright = (
    "2023–2027, Weine Olovsson and contributors; ENCCS | "
    "EuroCC 3 has received funding from the European High-Performance Computing Joint Undertaking"
    " (JU) under Grant Agreement No. 101306701. The JU receives support from the European Union's"
    " Digital Europe Programme and Germany, Albania, Austria, Belgium, Bosnia and Herzegovina, "
    "Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Greece, Hungary, "
    "Iceland, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Montenegro, the Netherlands, "
    "North Macedonia, Norway, Poland, Portugal, Romania, Serbia, Slovakia, Slovenia, Spain, "
    "Sweden, Türkiye, and Kosovo. Funded by the European Union. Views and opinions expressed are "
    "however those of the author(s) only and do not necessarily reflect those of the European "
    "Union or EuroHPC Joint Undertaking. Neither the European Union nor the EuroHPC Joint "
    "Undertaking can be held responsible for them. ENCCS has also received national funding "
    "through Vinnova and the Swedish Research Council (VR). HPC in Europe is the umbrella brand "
    "uniting Europe's high-performance computing initiatives across 36+ countries. The project is"
    " supported by the European High-Performance Computing Joint Undertaking and its members."
)

github_user = "ENCCS"
github_repo_name = "vasp-best-practices"
github_version = "main"
conf_py_path = "/content/"  # with leading and trailing slash

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinxcontrib.jquery",
    # githubpages just adds a .nojekyll file
    "sphinx.ext.githubpages",
    "sphinx_lesson",
    "sphinx_evita.css",
    "sphinxcontrib.bibtex",
    "myst_nb",
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
]

bibtex_bibfiles = []

# Settings for myst_nb:
# https://myst-nb.readthedocs.io/en/latest/use/execute.html#triggering-notebook-execution
# nb_execution_mode = "off"
# nb_execution_mode = "auto"   # *only* execute if at least one output is missing.
# nb_execution_mode = "force"
nb_execution_mode = "off"

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = ["colon_fence", "attrs_inline", "substitution"]
myst_substitutions = {"author": author}

# Settings for sphinx-copybutton
copybutton_exclude = ".linenos, .gp"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "README*",
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "jupyter_execute",
    "*venv*",
]

# -- Options for HTML output -------------------------------------------------
from pathlib import Path


HERE = Path(__file__).parent
detected_repo_name = HERE.parent.name

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title = project
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["overrides.css"]
html_favicon = str((HERE / "_static" / "favicon.ico").resolve())
github_repo_url = f"https://github.com/ENCCS/{github_repo_name or detected_repo_name}"
html_theme_options = {
    "announcement": "2027 event in preparation. The retained 2024 instructions have not been revalidated for 2027.",
    "light_logo": "ENCCS_logo_light.png",
    "dark_logo": "ENCCS_logo_dark.png",
    "source_repository": github_repo_url,
    "source_branch": github_version,
    "source_directory": conf_py_path,
    "footer_icons": [
        {
            "name": "GitHub",
            "url": github_repo_url,
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}


# HTML context:
html_context = {
    "display_github": True,
    "github_user": github_user,
    # Auto-detect directory name.  This can break, but
    # useful as a default.
    "github_repo": github_repo_name or detected_repo_name,
    "github_version": github_version,
    "conf_py_path": conf_py_path,
}

# sphinx-evita
evita_eu_funding_badge = "co-funded"


# Intersphinx mapping.  For example, with this you can use
# :py:mod:`multiprocessing` to link straight to the Python docs of that module.
# List all available references:
#   python -msphinx.ext.intersphinx https://docs.python.org/3/objects.inv
# extensions.append('sphinx.ext.intersphinx')
intersphinx_mapping = {
    # "python": ("https://docs.python.org/3", None),
    # "sphinx": ("https://www.sphinx-doc.org/", None),
    # "numpy": ("https://numpy.org/doc/stable/", None),
    # "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    # "pandas": ("https://pandas.pydata.org/docs/", None),
    # "matplotlib": ("https://matplotlib.org/", None),
    # "seaborn": ("https://seaborn.pydata.org/", None),
    # "evita": ("https://sphinx-evita.readthedocs.io/en/latest", None),
    # "instruct": ("https://enccs.github.io/instructor-training/", None),
    # "lesson": ("https://coderefinery.github.io/sphinx-lesson/", None),
    # "myst": ("https://myst-parser.readthedocs.io/en/latest/", None),
}

import os

if os.environ.get('GITHUB_REF', '') == 'refs/heads/main':
    html_js_files = [
        (
            'https://plausible.io/js/script.js',
            {
                "data-domain": f"enccs.github.io/{detected_repo_name}",
                "defer": "defer"
            }
        ),
    ]




# add few new directives
from sphinx_lesson.directives import _BaseCRDirective


class SignatureDirective(_BaseCRDirective):
    extra_classes = ["toggle-shown", "dropdown"]


class ParametersDirective(_BaseCRDirective):
    extra_classes = ["dropdown"]


class TypealongDirective(_BaseCRDirective):
    extra_classes = ["toggle-shown", "dropdown"]


DIRECTIVES = [SignatureDirective, ParametersDirective, TypealongDirective]


def single_page_navigation(app, pagename, templatename, context, doctree):
    if app.builder.name == "singlehtml":
        # Single-page output has no standalone search or index pages.
        hasdoc = context["hasdoc"]
        context["hasdoc"] = lambda name: name not in {"search", "genindex"} and hasdoc(name)
        context["sidebars"] = [
            sidebar for sidebar in context.get("sidebars", [])
            if sidebar != "sidebar/search.html"
        ]


def setup(app):
    # Reuse the template's EU badge assets without EVITA-specific branding.
    from sphinx_evita import init_static_path

    app.connect("builder-inited", init_static_path)
    app.connect("html-page-context", single_page_navigation)
    for obj in DIRECTIVES:
        app.add_directive(obj.get_cssname(), obj)
