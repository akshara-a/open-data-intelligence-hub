# Task 2 - GitHub Actions and Keep Alive Playwright Workflow

## Name
Guvvadi Ganesh

## Project Title
Global Poverty Intelligence Platform

## Streamlit App Link
https://global-poverty-intelligence-platform-ccl5ete9phglvrkcalyxmr.streamlit.app/

## GitHub Repository Link
https://github.com/guvvadiganesh-crypto/global-poverty-intelligence-platform

## Workflow File
.github/workflows/keep-alive.yml

## Task Completed
Implemented a GitHub Actions workflow using Playwright to keep the deployed Streamlit app active.

## Workflow Details
- Added GitHub repository secret: STREAMLIT_APP_URL
- Created workflow file: .github/workflows/keep-alive.yml
- Workflow runs automatically every 6 hours
- Manual workflow run tested successfully
- Status: Success

## Description
This project uses Python, Pandas, Plotly, Streamlit, and World Bank data to analyse global poverty reduction trends. For Task 2, I added a Playwright-based GitHub Actions workflow that opens the deployed Streamlit app on a schedule to help keep it warm.
