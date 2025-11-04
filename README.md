# SpaceY — Reusability Prediction API

![CI](https://github.com/GitDario79/The-SpaceY-project/actions/workflows/ci.yml/badge.svg?branch=main)


FastAPI service that serves a tiny scikit-learn model (saved with joblib) to predict the probability that a booster is reusable. Includes tests and GitHub Actions CI so reviewers can verify it runs.

---

## Why this repo matters

- **Product thinking:** turns a model into an **HTTP API** that anyone can call.
- **Reproducible:** artifact built from a script; environment pinned via `requirements.txt`.
- **Quality:** unit tests + CI on every push/PR.
- **Clarity:** minimal endpoints, typed payloads, and a 2-minute quickstart.

---

## Quickstart

> Windows PowerShell shown; macOS/Linux: replace the activate line with `source .venv/bin/activate`.

```bash
# 1) Setup
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt

# 2) Build the demo model artifact
python scripts/train_dummy_model.py    # writes models/model.joblib

# 3) Run the API
uvicorn app.main:app --reload
# Open docs: http://127.0.0.1:8000/docs
```

Smoke test (new shell):

```bash
# Single prediction
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"features\":[0.1,0.5,1.2]}"

# Batch prediction
curl -X POST http://127.0.0.1:8000/predict-batch \
  -H "Content-Type: application/json" \
  -d "{\"batch\":[[0.1,0.5,1.2],[0.9,1.0,0.8]]}"
```

Endpoints
GET /health → { "status": "ok" }

POST /predict → body:

```json
{ "features": [0.1, 0.5, 1.2] }
```
response:
```json
{ "reusability_probability": 0.462 }
```
POST /predict-batch → body:
```json
{ "batch": [[0.1, 0.5, 1.2], [0.9, 1.0, 0.8]] }
```
response:
```json
{ "reusability_probabilities": [0.462, 0.873] }
```

Run tests
```bash
# from repo root, with venv active
pytest -q
```
Project structure
```bash
The-SpaceY-project/
├─ app/
│  └─ main.py              # FastAPI app (uses lifespan to load the model)
├─ src/
│  ├─ model.py             # joblib loader + single/batch predict
│  └─ schemas.py           # pydantic request models
├─ scripts/
│  └─ train_dummy_model.py # builds models/model.joblib
├─ tests/
│  ├─ test_api.py          # health + single predict
│  └─ test_api_batch.py    # batch predict
├─ models/                 # generated artifacts (ignored in git)
├─ .github/workflows/
│  └─ ci.yml               # GitHub Actions (install → build artifact → tests)
├─ requirements.txt
├─ pytest.ini
└─ README.md
```
CI (GitHub Actions)
On every push/PR to main, CI will:

Set up Python

pip install -r requirements.txt

python scripts/train_dummy_model.py

pytest -q

Badge:

```markdown
![CI](https://github.com/GitDario79/The-SpaceY-project/actions/workflows/ci.yml/badge.svg)
```

If your workflow filename isn’t ci.yml, change the badge URL to match (e.g., api-ci.yml).

Notes & decisions
Artifacts: models/*.joblib is git-ignored; re-build locally/CI via the script.

Startup: app uses FastAPI lifespan to load the model at startup (modern replacement for @on_event).

Typing: Pydantic models validate request bodies; responses return rounded probabilities for readability.

Troubleshooting
Badge looks failing or “no status”:

Confirm the workflow file is at .github/workflows/ci.yml (or update the badge URL to your actual filename).

Confirm default branch is main.

Push any change to trigger a new run.

ModuleNotFoundError: app or src:

Ensure app/__init__.py, src/__init__.py exist and pytest.ini contains:

```ini
[pytest]
testpaths = tests
pythonpath = .
```
FileNotFoundError: models/model.joblib:

Run python scripts/train_dummy_model.py before starting the API or running tests.

License
MIT


I wrapped a scikit-learn model as a FastAPI service, added schema validation, tests, and CI. The artifact is built in CI and the API exposes both single and batch prediction with docs at /docs.
