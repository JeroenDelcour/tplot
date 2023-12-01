Development notes
-----------------

Because I forget.

## Development setup

Install dev dependencies: `pip install ".[dev]"`

Install pre-commit hooks: `pre-commit install`

For code formatting, `black` and `isort` are used with default settings.

## For a new release

Bump the version in `pyproject.toml`.

[Use an annotated git tag with the version](https://stackoverflow.com/questions/11514075/what-is-the-difference-between-an-annotated-and-unannotated-tag): `git tag -a v0.2.0 -m ""`

[Git push with tags](https://stackoverflow.com/questions/5195859/how-do-you-push-a-tag-to-a-remote-repository-using-git): `git push --follow-tags`

[Publish on pypi](https://flit.pypa.io/en/stable/): `flit publish`

[Create a release on GitHub](https://github.com/JeroenDelcour/tplot/releases/new).

Documentation is built automatically by readthedocs. To build locally, run: `cd docs && make html`
