# ⚽ FIFA World Cup Analytics Engine

Comprehensive match outcome analysis and patterns — 1930 to 2014 · 852 matches · 20 tournaments.

## Quick Deploy to Netlify

### Option A — Drag & Drop (Fastest)
1. Go to [app.netlify.com](https://app.netlify.com)
2. Log in (or sign up free)
3. Drag the entire `fifa-analytics` folder onto the **"Deploy manually"** drop zone
4. Your site is live in ~10 seconds ✅

### Option B — GitHub + Netlify CI/CD
1. Push this folder to a GitHub repo
2. Go to [app.netlify.com](https://app.netlify.com) → "Add new site" → "Import an existing project"
3. Connect GitHub, select your repo
4. Build settings: **Build command** = *(leave blank)*, **Publish directory** = `.`
5. Click "Deploy site" ✅

## Project Structure

```
fifa-analytics/
├── index.html          ← Entry point
├── netlify.toml        ← Netlify config (headers, redirects, cache)
├── css/
│   └── style.css       ← All styles
└── js/
    ├── data.js         ← Embedded dataset + CSV parsers
    ├── charts.js       ← Chart.js rendering functions
    └── app.js          ← Tab routing, UI, upload logic
```

## Features
- **Overview** — Goals, attendance, winners donut, goals-per-match trend
- **Teams** — Win rates, titles/finals/SF breakdown, goals comparison
- **Goal Patterns** — Stage-by-stage analysis, era comparisons
- **Matches** — Searchable/filterable table of all tracked matches
- **Analytics** — Outcome patterns, scoreline frequencies, growth charts
- **Upload Data** — Drop Kaggle CSVs to load real 852-match dataset

## Loading Real Kaggle Data
1. Download from https://www.kaggle.com/datasets/abecklas/fifa-world-cup
2. Extract ZIP
3. Open the live site → "Upload Data" tab
4. Drop `WorldCupMatches.csv` and/or `WorldCups.csv`
5. All charts update instantly — no server needed

## Tech Stack
- Pure HTML / CSS / Vanilla JS (zero build step)
- Chart.js 4.4.1 via CDN
- No frameworks, no dependencies, no Node.js required
