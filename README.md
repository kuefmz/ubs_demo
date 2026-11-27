# Repository governance demo

Edit [project.yaml](project.yaml) for project values and [ci/validate.py](ci/validate.py)
when required fields or validation rules change. CI checks the metadata and
requires a `requirements.txt` update when `pyproject.toml`, `setup.py` or
`setup.cfg` changes.

## GitHub demo

Open a PR to `main` and look for **Validate repository**. To enforce review,
protect `main` with that required check and one approval, then enable native
auto-merge. This requires a supported paid plan for a private repo.

After validation passes on a push to `main`, Actions automatically creates
`build-<commit SHA>`. Protect `main` to limit this to merged changes. If tag
rules apply, allow the workflow identity to create these tags.

## GitLab setup

Copy the files to GitLab, protect `main` against direct pushes, enable
**Pipelines must succeed**, and require one approval (Premium or Ultimate).
Select **Set to auto-merge** on the MR so GitLab merges after approval and checks.

On GitLab 18.4+, enable **Allow Git push requests to the repository** under
CI/CD job token permissions. The pipeline tags the validated commit on
protected `main` automatically. If tags are protected, the identity that
starts the pipeline needs permission to create `build-*` tags.
