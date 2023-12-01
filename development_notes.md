Development notes
-----------------

Because I forget.

## Setup

Install dev dependencies: `pip install ".[dev]"`

Install pre-commit hooks: `pre-commit install`

For code formatting, `black` and `isort` are used with default settings.

## Unit tests

`pytest` is used to run unit tests.

Generated test figures are checked if they match with a set of reference figures in the `tests/reference_figures` directory. For some code changes, they may no longer match character-for-character, but still look good. If this is acceptable, you can generate new reference figures.

### Generating reference figures

Set the `GENERATE` variable at the top of `tests/test_reference_figures.py` to `True` and run the tests again. You use `git status` to tell you which reference plots have changed, since they're just text files. Use your own eyes to look at any changes. If they look good, set the `GENERATE` flag back to `False` and commit the new refernce figures to git.

## Creating a new release

- Bump the version in `pyproject.toml`
- [Create an annotated git tag with the version string](https://stackoverflow.com/questions/11514075/what-is-the-difference-between-an-annotated-and-unannotated-tag): `git tag -a v0.2.0 -m ""`
- [Git push with tags](https://stackoverflow.com/questions/5195859/how-do-you-push-a-tag-to-a-remote-repository-using-git): `git push --follow-tags`
- [Publish on pypi](https://flit.pypa.io/en/stable/): `flit publish`
- [Create a release on GitHub](https://github.com/JeroenDelcour/tplot/releases/new)

Documentation is built automatically by readthedocs. To build locally, run: `cd docs && make html`
