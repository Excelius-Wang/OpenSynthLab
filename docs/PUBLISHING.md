# Publishing

The repository uses GitHub Actions and PyPI Trusted Publishing. No long-lived PyPI API token is needed.

## One-time setup

Sign in to PyPI with a verified email and two-factor authentication. For the first release, add a pending publisher at <https://pypi.org/manage/account/publishing/>:

| Field | Value |
| --- | --- |
| PyPI project name | `opensynthlab` |
| GitHub owner | `Excelius-Wang` |
| GitHub repository | `OpenSynthLab` |
| Workflow filename | `publish.yml` |
| Environment name | `pypi` |

Use the `pypi` GitHub environment for this repository and restrict deployment to the `main` branch. This publisher allows only the named repository, workflow, and environment to publish this package. A pending publisher does not reserve the package name; the first successful upload creates the project.

## Release

1. Update the version in both `pyproject.toml` and `src/opensynthlab/__init__.py`, and update the changelog.
2. Verify the test matrix and review the intended commit on `main`.
3. Manually run **Publish to PyPI** from GitHub Actions on `main`.
4. Check the successful run and confirm the version on PyPI.
5. Tag the published commit and create a GitHub release, marking alpha versions as prereleases.

The workflow tests and builds in a separate job before uploading the artifacts through the trusted publisher. It does not run on pull requests or automatic pushes. Treat the first upload as permanent: PyPI does not allow reusing an uploaded filename, even after deletion.

After the alpha is published, install it explicitly:

```bash
python -m pip install 'opensynthlab==0.1.0a1'
opensynthlab --version
```
