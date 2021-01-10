Development notes
-----------------

Because I forget.

[Update dependencies to latest version](https://python-poetry.org/docs/cli/#update): `poetry update`

[Bump version](https://python-poetry.org/docs/cli/#version): `poetry version [major/minor/patch]`

[Use an annotated git tag with the version](https://stackoverflow.com/questions/11514075/what-is-the-difference-between-an-annotated-and-unannotated-tag): `git tag -a v0.2.0 -m ""`

[Git push with tags](https://stackoverflow.com/questions/5195859/how-do-you-push-a-tag-to-a-remote-repository-using-git): `git push --follow-tags`

[Publish on pypi](https://python-poetry.org/docs/cli/#publish): `poetry publish --build`

Documentation is built automatically by readthedocs. To build locally, run: `cd docs && make html`