# Microsoft AI Deployment Cost Modeling

A total-cost-of-ownership (TCO) calculator for Microsoft AI deployments —
Microsoft 365 Copilot licensing, Azure OpenAI usage, supporting infrastructure
(Azure AI Search, etc.), and implementation/support effort.

Estimates are based on approximate list pricing and are meant as a planning
tool, not a quote. Update `server/pricing.py` as Microsoft's published pricing
changes.

## Stack

- **Backend:** FastAPI (Python 3.11+) — `server/`
- **Frontend:** Vue 3 + Vite — `client/`

## Running locally

### Backend

macOS/Linux:

```bash
cd server
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --reload --port 8000
```

Windows (PowerShell or cmd):

```powershell
cd server
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

(Use `python -m uvicorn` rather than calling `.venv\Scripts\uvicorn` directly —
PowerShell doesn't resolve the `.exe` extension for explicit paths, so the
bare script name fails with "not recognized".)

API docs: http://localhost:8000/docs

### Frontend

```bash
cd client
npm install
npm run dev
```

App: http://localhost:3000 (proxies `/api` to `http://localhost:8000`)

## API

- `GET /api/pricing-reference` — current pricing assumptions (license tiers,
  Azure OpenAI model rates, Azure AI Search tiers, default hourly rates)
- `POST /api/calculate` — takes a deployment description (seats, model,
  token volume, infrastructure, implementation/support effort) and returns a
  full cost breakdown (monthly, annual, one-time, first-year total)

## What's modeled

- **Licensing** — Microsoft 365 Copilot / Copilot Studio per-seat cost, with
  an optional annual-commitment discount
- **AI usage** — Azure OpenAI pay-as-you-go token pricing per model, or
  Provisioned Throughput Units (PTU)
- **Infrastructure** — Azure AI Search tier, plus any other monthly
  infrastructure cost
- **Implementation** — one-time integration effort (hours × hourly rate)
- **Support** — ongoing monthly support effort (hours × hourly rate)
