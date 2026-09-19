# SkillBridge Vercel deployment

## Keep these files at repository root

- index.html
- main.html
- opportunity.html
- oppurtunity.js
- opportunity.css
- jobs.csv
- skills.csv
- main.py
- requirements.txt
- api/index.py

## What changed

1. `api/index.py` imports the existing FastAPI `app` from root `main.py`.
2. `oppurtunity.js` uses `/api/recommend` on Vercel and keeps `127.0.0.1:8000` for local backend testing.
3. `requirements.txt` installs the Python dependencies.
4. No custom Vercel routing file is required; Vercel can package `api/index.py` as the Python function.

## Deploy

```bash
npm i -g vercel
vercel login
vercel link
vercel --prod
```

## Test after deployment

Open:

- `/api/` or `/` depending on the deployment route
- `/api/recommend` with POST from the frontend
- `/docs` may be available depending on the Vercel function routing

## Local API test

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open `http://127.0.0.1:8000/docs`.

The browser frontend should use the same-origin `/api/recommend` endpoint when hosted on Vercel.
