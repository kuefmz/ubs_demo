# Repository governance demo

Each repository has a root `project.yaml` with a project ID, name, Python
version, owner, required access and group share location. The example uses
fictional groups and a placeholder location. Access entries describe the
permissions the project needs. The validator checks their format; provisioning
and checking real entitlements are outside this demo.

The MR/PR check validates metadata, checks that `requirements.txt` exists, and
reports whether it changed. Editing `pyproject.toml`, `setup.py` or `setup.cfg`
requires a corresponding `requirements.txt` change. This simple demo rule
treats every edit to those files as potentially dependency-related. Metadata
only needs an edit when a project value changes.

## Run locally

From the repository root, install PyYAML in a virtual environment:

```sh
python -m pip install PyYAML==6.0.3
python ci/validate.py
python ci/validate.py "$(git merge-base main HEAD)" HEAD
```

## Try it on GitHub

1. Enable **Allow auto-merge** in repository settings. In a ruleset for
   `main`, require a pull request, one approving review and the
   **Validate repository** status check. Enable dismissal of stale approvals
   on new commits and give no bypass to the identities used in the demo.
   A private repository needs GitHub Pro, Team or Enterprise for this setup.
2. Open a pull request from a branch and watch the check run. Try making
   `owner` blank to demonstrate a failure, then restore it. To demonstrate
   the dependency rule, add a dependency manifest without updating
   `requirements.txt`, then update the file to make the check pass.
3. Once checks pass, select **Enable auto-merge** while the review is still
   pending. Have a second user approve the pull request. GitHub merges it
   when all rules are satisfied.
4. After the push pipeline validates protected `main`, Actions pushes a
   lightweight `build-<full commit SHA>` tag. If the repository uses tag
   rules, the workflow identity needs permission to create these tags.

## Run on GitLab

1. Copy the repository to GitLab and protect `main`. Allow merges for the
   appropriate roles and set **Allowed to push and merge** to **No one**.
2. Enable **Pipelines must succeed** and require one eligible human approval.
   Prevent author approval, reset approvals when new commits are added and
   disable per-MR edits to approval rules. Required approvals need GitLab
   Premium or Ultimate.
3. On GitLab 18.4+, enable **Allow Git push requests to the repository** under
   CI/CD job token permissions. If you protect `build-*` tags, allow the
   identity that starts the protected-branch pipeline to create them.
   GitLab job-token pushes use the permissions of the user who started the
   pipeline and do not trigger another pipeline.
4. Open an MR to `main`. Enable **Set to auto-merge** once validation passes
   and while approval is pending. A maintainer with merge permission can also
   request auto-merge when opening the MR with Git push options:
   `git push -o merge_request.create -o merge_request.target=main -o merge_request.merge_when_pipeline_succeeds origin HEAD`.
   GitLab waits for required checks and approval. Review and enable
   auto-merge again if the source branch changes and GitLab cancels it.
5. The protected `main` pipeline validates the merged result and tags that
   commit. The build tag identifies exactly what landed, including when
   GitLab creates a new merge or squash commit. A rerun uses the same tag.

## Before rolling out across repositories

- Test installing dependencies with the declared Python version and run the
  project's own tests. The demo validation runner itself uses Python 3.12.
- Adopt a generated lock file if you want to verify synchronization with
  dependency declarations and move past the filename-change heuristic.
- Require review for CI and validator changes. Consider managing the
  required check centrally when the same rules apply across repositories.
