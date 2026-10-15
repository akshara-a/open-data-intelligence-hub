# Task 2: GitHub Actions Keep-Alive Workflow

**Student:** Shaik Aiesha  

**Batch:** G40 AI/ML  

## What I Did:

1. Created `.github/workflows/keep_alive.yml` with GitHub Actions automation.
2. Configured the workflow to run automatically using a cron schedule.
3. Added `STREAMLIT_APP_URL` as a GitHub repository secret.
4. Used Playwright browser automation to open my Streamlit application.
5. Successfully executed the workflow to help keep my Streamlit app awake.

## My Streamlit App:

Add your Streamlit app URL here:

`YOUR_STREAMLIT_APP_URL`

## Files in This Folder:

- `keep_alive.yml` - GitHub Actions workflow file
- `workflow-success.png` - Screenshot of successful workflow run
- `README.md` - This file

## Workflow Schedule:

The workflow runs every 4 hours using the cron schedule:

```text
0 */4 * * *