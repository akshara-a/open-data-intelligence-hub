# Reviewer Checklist – PR Review

Use this checklist while reviewing each project submission PR.

## 1. Submission Scope

* [ ] Confirm that the PR contains changes only for the submitter's own project/folder.
* [ ] Ensure no files or folders belonging to other participants have been modified.
* [ ] Ensure no files or folders belonging to other participants have been deleted.
* [ ] Ensure no unrelated project files have been renamed or moved.
* [ ] Check the PR diff for accidental bulk deletions or unrelated changes.
* [ ] Reject the PR if it modifies another participant's submission without a valid reason.

---

## 2. PR Completeness

* [ ] Do not approve incomplete PRs.
* [ ] Verify that all mandatory deliverables are included.
* [ ] Ensure there are no placeholder files such as `TODO`, empty implementations, or unfinished sections.
* [ ] Ensure required models, scripts, reports, results, or documentation are included where applicable.
* [ ] Check that code referenced in the README actually exists.
* [ ] Check that the project can be executed using the provided instructions.
* [ ] Ensure required outputs/results are available and not merely described.
* [ ] Verify that obvious runtime errors or broken imports are not present.
* [ ] Reject the PR if major functionality is commented out or left unfinished.

---

## 3. Unwanted Generated / Cache Files

The PR should contain source code and required project artifacts only.

Ensure the following are **not committed**:

* [ ] `__pycache__/`
* [ ] `*.pyc`
* [ ] `*.pyo`
* [ ] `*.pyd`
* [ ] `.pytest_cache/`
* [ ] `.mypy_cache/`
* [ ] `.ruff_cache/`
* [ ] `.ipynb_checkpoints/`
* [ ] Temporary files
* [ ] Local IDE cache files
* [ ] Build-generated files that are not required
* [ ] Operating-system-generated files such as `.DS_Store`
* [ ] Unnecessary log files
* [ ] Temporary downloaded datasets when they should be obtained through setup instructions

Verify that an appropriate `.gitignore` is present.

---

## 4. Model / Binary Files

For ML projects, review model files carefully.

* [ ] Check whether `.pkl`, `.pickle`, `.joblib`, `.h5`, `.keras`, `.pt`, `.pth`, `.onnx`, or similar files are actually required.
* [ ] Do not allow unnecessary model checkpoints or temporary model files.
* [ ] Do not allow multiple large checkpoints when only the final/best model is required.
* [ ] Ensure model files are not accidentally generated cache artifacts.
* [ ] Verify that large binary files follow the repository's expected storage policy.
* [ ] Ensure temporary serialized Python objects such as `.pkl` files are not committed unless explicitly required by the project.

---

## 5. Secrets and Sensitive Information

No credentials or secrets should be committed.

Check for:

* [ ] API keys
* [ ] Access tokens
* [ ] Personal access tokens
* [ ] Passwords
* [ ] Database passwords
* [ ] Connection strings containing credentials
* [ ] Cloud credentials
* [ ] Private keys
* [ ] Client secrets
* [ ] Authentication tokens
* [ ] Hardcoded usernames/passwords
* [ ] `.env` files containing real secrets

Look for suspicious values in:

```text
.env
config.py
settings.py
appsettings files
notebooks
README files
scripts
JSON/YAML configuration
source code
```

Secrets should instead be represented using placeholders such as:

```text
API_KEY=<YOUR_API_KEY>
DATABASE_PASSWORD=<YOUR_PASSWORD>
```

* [ ] Reject the PR immediately if an active secret or credential is committed.
* [ ] If a real secret was previously committed, ensure the reviewer informs the submitter that removing it from the latest commit is not enough; the credential should also be rotated.

---

## 6. Repository Hygiene

* [ ] No unnecessary files are committed.
* [ ] No personal files are committed.
* [ ] No screenshots unrelated to the project are committed.
* [ ] No editor/IDE metadata is committed unless intentionally shared.
* [ ] No large temporary files are committed.
* [ ] No duplicate datasets/models are committed.
* [ ] `.gitignore` covers common Python and IDE artifacts.
* [ ] File and folder names are meaningful and consistent.

---
