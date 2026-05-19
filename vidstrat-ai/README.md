# anvidAI

anvidAI is a Video Marketing Intelligence Platform for comparing real YouTube channels, finding competitive gaps, scoring content strategy, and exporting a professional PowerPoint report. It is built as a decoupled full-stack application: a FastAPI backend handles YouTube data, statistical analysis, SEO scoring, Claude strategy generation, chart rendering, and PPTX creation; a React 18 frontend presents an animated SaaS dashboard with live Recharts visualisations.

## Architecture

- Backend: Python, FastAPI, YouTube Data API v3, Anthropic Claude, matplotlib, seaborn, pandas, python-pptx.
- Frontend: React 18, Vite, Tailwind CSS, framer-motion, Recharts, axios.
- Development ports: backend on `8000`, frontend on `5173`.
- Deployment targets: Railway or Render for the backend, Vercel or Netlify for the frontend.

## Prerequisites

- Python 3.10 or newer.
- Node.js 18 or newer.
- A YouTube Data API v3 key.
- An Anthropic API key for Claude strategy analysis.

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `backend/.env`:

```env
YOUTUBE_API_KEY=your_youtube_data_api_v3_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Run the backend:

```bash
uvicorn main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/api/health
```

Expected response:

```json
{ "status": "ok", "version": "1.0" }
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## YouTube API v3 Key Setup

1. Open Google Cloud Console.
2. Create a new project or choose an existing project.
3. Go to APIs and Services.
4. Select Library.
5. Search for YouTube Data API v3.
6. Open the API page and select Enable.
7. Go to APIs and Services, then Credentials.
8. Select Create Credentials, then API key.
9. Copy the generated key.
10. Paste it into `backend/.env` as `YOUTUBE_API_KEY`.

Suggested screenshots for documentation evidence: Google Cloud project selector, YouTube Data API v3 enabled screen, Credentials page with the API key dialog.

## Anthropic API Key Setup

1. Open the Anthropic Console.
2. Go to API Keys.
3. Create a new key.
4. Copy it once and store it securely.
5. Paste it into `backend/.env` as `ANTHROPIC_API_KEY`.

If Claude is unavailable, anvidAI still returns real YouTube data, data science scores, SEO scores, charts, and PPTX output. Strategic commentary sections use deterministic data-based fallbacks and the API response includes a clear availability message.

## Running Locally

Start the backend:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Start the frontend in another terminal:

```bash
cd frontend
npm run dev
```

Use the built-in dairy example for the assessment flow: Amul as the primary company, with Mother Dairy, Nestle India, Britannia, and Nandini as competitors.

## API

`POST /api/analyse`

```json
{
  "primary_company": "Amul",
  "competitors": ["Mother Dairy", "Nestle India", "Britannia", "Nandini"]
}
```

The response contains company metrics, radar scores, SEO scores, content pillars, top videos, personas, whitespace opportunities, a 90-day action plan, base64 PNG charts, and a base64 PowerPoint report.

`GET /api/health`

```json
{ "status": "ok", "version": "1.0" }
```

## Score Interpretation

- Consistency: based on the standard deviation of intervals between uploads.
- Engagement: maps average engagement rate to a 100-point score, with 4 percent or higher treated as elite.
- Audience Growth: relative subscriber strength within the comparison set.
- Content Performance: average views relative to subscribers.
- Activity Level: upload frequency across the recent video window.
- Overall Strength: weighted score combining consistency, engagement, audience growth, content performance, and activity.

SEO scores combine title quality, description depth, and upload timing consistency. Content pillars classify recent video titles into strategic buckets such as Education, Product Showcase, Social Proof, Tutorial/How-To, and Brand Culture.

## Deployment

### Backend on Railway

1. Create a new Railway project.
2. Connect the repository.
3. Set the root directory to `backend`.
4. Add environment variables `YOUTUBE_API_KEY` and `ANTHROPIC_API_KEY`.
5. Use the start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Backend on Render

1. Create a new Web Service.
2. Set the root directory to `backend`.
3. Build command:

```bash
pip install -r requirements.txt
```

4. Start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

5. Add `YOUTUBE_API_KEY` and `ANTHROPIC_API_KEY`.

### Frontend on Vercel

1. Import the repository into Vercel.
2. Set the root directory to `frontend`.
3. Build command: `npm run build`.
4. Output directory: `dist`.
5. Update `API_URL` in `src/App.jsx` or provide an environment-based API URL before production deployment.

### Frontend on Netlify

1. Create a new site from Git.
2. Set base directory to `frontend`.
3. Build command: `npm run build`.
4. Publish directory: `frontend/dist`.
5. Configure the backend URL for production.

## Report Workflow

1. Enter one primary brand and one to four competitors.
2. anvidAI locates official YouTube channels and excludes companies it cannot confidently resolve.
3. The backend fetches recent video data, calculates performance scores, runs SEO analysis, creates content pillars, generates charts, and builds the PPTX.
4. The dashboard renders eight analysis tabs.
5. Use the final tab to download the self-contained 12-slide PowerPoint report.
