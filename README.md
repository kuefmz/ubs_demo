# Repository governance demo

Edit [project_config.yaml](project_config.yaml) for project values. Both CI
workflows use the validation in [.gitlab-ci.yml](.gitlab-ci.yml). Validation
requires `requirements.txt` to exist. Every merge request to `main` must also
change it.

## GitLab setup

1. Copy `.gitlab-ci.yml`, `project_config.yaml`, and `requirements.txt` to the
   repository root. In **Settings → CI/CD → Variables**, set
   `VALIDATION_IMAGE` to your approved Python image and `PIP_INDEX_URL` to
   your approved Python package index's `/simple/` URL. Make both variables
   available to merge request pipelines.
2. Open or update a merge request to `main`. GitLab detects the requirements
   change using `rules:changes`. The job only needs Python, pip, and PyYAML.
3. To enforce review, protect `main`, enable **Pipelines must succeed**, and
   require an approval if your GitLab tier supports it. Use **Set to auto-merge**
   on the merge request if desired.

GitHub Actions runs the same validator on pull requests and pushes to `main`.
