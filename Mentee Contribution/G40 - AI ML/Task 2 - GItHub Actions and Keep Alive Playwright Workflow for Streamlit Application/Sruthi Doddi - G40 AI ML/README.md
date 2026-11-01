# Task 2: GitHub Actions Keep-Alive Workflow

**Student:** Sruthi Doddi  
**Batch:** G40 AI/ML  

## What I Did:
1. Created `.github/workflows/keep-alive.yml` with Playwright browser automation
2. Workflow runs every 4 hours using cron schedule (`0 */4 * * *`)
3. Added `STREAMLIT_APP_URL` as GitHub repository secret
4. Workflow successfully opens my Streamlit app and keeps it awake

## My Streamlit App:
https://extreme-weather-platform-7dlpngezg6tlrsbyh3zlzm.streamlit.app

## Files in This Folder:
- `keep-alive.yml` - GitHub Actions workflow file
- `workflow-success.png` - Screenshot of successful workflow run
- `README.md` - This file

## Workflow Status: ✅ Successful
