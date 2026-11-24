# VASP Best Practices — 2027 preparation

ENCCS training material. The 2024 source and history are preserved on branch `2024` at `c90a58d09b22d1ca386235a999a6d096f1d03239`; `main` is the working 2027 edition.

The theme and build setup are adapted from [ENCCS/sphinx-lesson-template](https://github.com/ENCCS/sphinx-lesson-template/tree/b44f1af72b189c1bb97014c6d88772a83e1cb691). Existing lesson prose, scientific examples, commands, slides and contributor credits are retained. Event-specific instructions remain historical until reviewed for 2027.

## Build locally

Use Python 3.13:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --group notebook .
make dirhtml SPHINXOPTS='-W --keep-going'
make singlehtml SPHINXOPTS='-W --keep-going'
```

Generated files and environments are ignored. Notebook execution is disabled during documentation builds.

## Publication

CI builds documentation without publishing. Deployment is absent during this migration; event details, historical accounts/paths and all intended publication artifacts need review before enabling deployment. The `2024` source branch is preserved exactly; it does not by itself create an archive website.

Project briefs, review lists, validation evidence and handovers are maintained in the surrounding workspace, outside this teaching repository.

The original CC-BY-4.0 material and MIT code licences and contributor attribution are retained.
