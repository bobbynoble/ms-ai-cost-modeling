# AI Deployment Cost Modeling

A total-cost-of-ownership (TCO) calculator for AI deployments across
**Microsoft**, **Anthropic (Claude)**, and **AWS** — per-seat licensing, AI
model usage, supporting infrastructure, and implementation/support effort.
Licensing and usage are repeatable line items, so a deployment can mix
providers (e.g. some Microsoft 365 Copilot seats alongside direct Claude API
usage and Amazon Bedrock).

Estimates are based on approximate list pricing and are meant as a planning
tool, not a quote. Update `server/pricing.py` as vendors' published pricing
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
.venv/bin/uvicorn main:app --reload --port 8900
```

Windows (PowerShell or cmd):

```powershell
cd server
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8900
```

(Use `python -m uvicorn` rather than calling `.venv\Scripts\uvicorn` directly —
PowerShell doesn't resolve the `.exe` extension for explicit paths, so the
bare script name fails with "not recognized".)

Port 8900 is just this project's default — if it's already taken on your
machine, pick another free one with `netstat -aon | findstr LISTENING`
(Windows) or `lsof -iTCP -sTCP:LISTEN` (macOS/Linux), then pass
`--port <yours>` and update the proxy target in `client/vite.config.js` to match.

API docs: http://localhost:8900/docs

### Frontend

```bash
cd client
npm install
npm run dev
```

App: http://localhost:4200 (proxies `/api` to `http://localhost:8900`)

## API

- `GET /api/pricing-reference` — current pricing assumptions for all three
  providers (license tiers, model usage rates, infrastructure tiers, default
  hourly rates)
- `POST /api/calculate` — takes a deployment description (one or more
  licensing lines, one or more AI usage lines, infrastructure,
  implementation/support effort) and returns a full cost breakdown (monthly,
  annual, one-time, first-year total)

## What's modeled

- **Licensing** (repeatable, per provider) — Microsoft 365 Copilot / Copilot
  Studio, Claude for Work / Enterprise, Amazon Q Business Lite / Pro — with an
  optional annual-commitment discount per line
- **AI usage** (repeatable, per provider) — pay-as-you-go token pricing per
  model (Azure OpenAI, Claude API, Amazon Bedrock), or reserved/provisioned
  throughput where a provider offers it (currently Azure OpenAI PTU)
- **Infrastructure** (repeatable, per provider) — Azure AI Search tier, Amazon
  OpenSearch Serverless / Kendra, plus any other flat monthly infra cost
- **Implementation** — one-time integration effort (hours × hourly rate)
- **Support** — ongoing monthly support effort (hours × hourly rate)
