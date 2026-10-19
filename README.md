# David Chin · Lobby Portfolio

Game-lobby version of my engineering portfolio, with my live Valorant rank (avendail#4974) in the player card.
Classic version: https://davidchin-purdue.github.io/Portfolio-Website/

## How the live rank works
- `.github/workflows/rank.yml` runs every 30 minutes and calls `scripts/update_rank.py`.
- The script asks the HenrikDev API for the rank and writes `rank.json`, committing only when the rank or RR changes.
- `rank.js` reads `rank.json` and updates the page. If the file is missing, the page keeps its built-in rank.

## Setup
1. Repo secret `HENRIK_API_KEY` (Settings > Secrets and variables > Actions) with a free HenrikDev key.
2. Settings > Actions > General > Workflow permissions: Read and write.
3. Settings > Pages: deploy from branch `main`, folder `/ (root)`.
4. Actions tab > Update Valorant rank > Run workflow, to pull the first real rank.
