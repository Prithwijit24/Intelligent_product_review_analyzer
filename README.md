# Intelligent Product Review Analyzer

An end-to-end NLP application for extracting structured insight from product reviews. It provides a FastAPI backend, a Streamlit dashboard, Docker Compose for local deployment, and Kubernetes manifests for cluster deployment.

The first version is intentionally runnable without downloading large datasets. It uses a deterministic rule-based NLP baseline for aspect sentiment and review tags, with training modules included for later TF-IDF and logistic regression experiments.

## Features

- Aspect-level sentiment for `price`, `quality`, `delivery`, and `packaging`
- Overall sentiment: `positive`, `neutral`, `negative`, or `mixed`
- Review tags: `complaint`, `praise`, `suggestion`, `question`, or `neutral`
- FastAPI endpoints for analysis and health checks
- FastAPI lifespan startup that warms the NLP pipeline before serving traffic
- Streamlit dashboard for interactive review analysis
- Multi-stage Docker image, Docker Compose, and Kubernetes manifests with ingress
- Unit and integration tests

## Architecture

```text
Streamlit Dashboard
        |
        v
FastAPI Backend
        |
        v
ReviewAnalyzer Pipeline
        |
        +-- cleaner
        +-- tokenizer
        +-- normalizer
        +-- aspect extractor
        +-- sentiment analyzer
        +-- tagger
        |
        v
Structured JSON Insights
```

## Project Structure

```text
.
├── src/review_analyzer/
│   ├── api/                 # FastAPI app, routes, request/response schemas
│   ├── core/                # Settings, logging, domain exceptions
│   ├── dashboard/           # Streamlit dashboard
│   ├── nlp/                 # Cleaning, tokenization, aspects, sentiment, tags
│   ├── pipeline/            # End-to-end analyzer orchestration
│   └── training/            # Optional TF-IDF/vectorizer/model training helpers
├── tests/
│   ├── integration/
│   └── unit/
├── data/
├── models/
├── k8s/
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── requirements.txt
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
python -m spacy download en_core_web_sm
```

The app falls back to a blank English spaCy pipeline if `en_core_web_sm` is not installed, but the full model is recommended for better token normalization.

Optional local environment file:

```bash
cp .env.example .env
```

## Run the API

```bash
uvicorn review_analyzer.api.main:app --reload
```

Open:

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

Example request:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "B001234",
    "review_text": "The product quality is great but delivery was very slow."
  }'
```

Example response:

```json
{
  "product_id": "B001234",
  "overall_sentiment": "mixed",
  "aspects": {
    "quality": "positive",
    "delivery": "negative"
  },
  "aspect_terms": {
    "quality": ["great"],
    "delivery": ["slow"]
  },
  "tags": ["complaint", "praise"],
  "cleaned_text": "The product quality is great but delivery was very slow.",
  "tokens": ["The", "product", "quality", "is", "great", "but", "delivery", "was", "very", "slow", "."],
  "normalized_tokens": ["product", "quality", "great", "delivery", "slow"]
}
```

## Run the Dashboard

Start the API first, then run:

```bash
streamlit run src/review_analyzer/dashboard/app.py
```

Open `http://localhost:8501`.

To point the dashboard to another backend:

```bash
API_URL=http://localhost:8000 streamlit run src/review_analyzer/dashboard/app.py
```

## Docker Compose

```bash
docker compose up --build
```

Services:

- API: `http://localhost:8000`
- Dashboard: `http://localhost:8501`

## Kubernetes

Build the image and apply the manifests:

```bash
docker build -t review-analyzer:latest .
kubectl apply -k k8s/
```

For local clusters such as minikube or kind, make sure the image is available inside the cluster.
The included ingress routes `review-analyzer.local/` to the dashboard and `review-analyzer.local/api` to the API when an nginx ingress controller is installed.

Port-forward services:

```bash
kubectl -n review-analyzer port-forward svc/review-analyzer-api 8000:8000
kubectl -n review-analyzer port-forward svc/review-analyzer-dashboard 8501:8501
```

## Tests

```bash
pytest
```

## Configuration

Environment variables:

| Variable | Default | Purpose |
|---|---:|---|
| `ENVIRONMENT` | `local` | Runtime environment label |
| `SPACY_MODEL` | `en_core_web_sm` | spaCy model name |
| `API_URL` | `http://localhost:8000` | Backend URL used by Streamlit |
| `LOG_LEVEL` | `INFO` | Application log level |

## Training Extension Points

The baseline analyzer is rule-based so it works immediately. For future labeled-data work, use:

- `review_analyzer.training.vectorizer.build_tfidf`
- `review_analyzer.training.vectorizer.save_artifact`
- `review_analyzer.training.vectorizer.load_artifact`
- `review_analyzer.training.sentiment_model.SentimentClassifier`

These modules support TF-IDF features, logistic regression training, and model persistence with `joblib`.
