# SAP RPT-1 Code Examples (Python)

This folder contains Python code examples for working with **SAP RPT-1**, a foundation model for tabular tasks hosted on SAP AI Core. You provide tabular rows with one or more cells marked as prediction targets, and the model returns predicted values for those cells based on patterns in the surrounding data.

> **Note:** An official SAP AI SDK for Python with RPT-1 support is planned but not yet publicly available. The examples here use direct API requests and a custom-built helper client to demonstrate how to access RPT-1 from Python in the meantime. Once the official SDK is released, these examples will be updated accordingly.

The folder provides two independent approaches:

1. **Raw HTTP requests**: a standalone notebook that builds every request from scratch using `requests`. This is the most transparent way to understand the RPT-1 API.
2. **`RPT1Client` (custom example client)**: a sample DataFrame-first wrapper with a scikit-learn-style `fit`/`predict` API, showing how you could build a more streamlined experience on top of the raw API.

## Project Structure

```
python/
├── .env.example              # Template for required environment variables
├── requirements.txt          # Python dependencies (requests, python-dotenv, pandas)
├── rpt1_client.py            # Example custom client: DataFrame-first fit/predict wrapper
├── test_rpt1_client.py       # Unit tests for the example client (unittest + mocks)
├── RPT-1_client.ipynb        # Tutorial notebook: example client workflow
└── RPT-1_request.ipynb       # Tutorial notebook: raw HTTP requests workflow
```

## What Each File Does

### `rpt1_client.py` example custom client

A sample Python module (~590 lines) that wraps the RPT-1 prediction API into a pandas DataFrame workflow. This is **not an official SDK**. It is included as a reference showing how you could build a more streamlined, reusable experience on top of the raw REST API. Key patterns it demonstrates:

- **`fit` / `predict` pattern**: mirrors scikit-learn conventions. `fit()` stores context rows and prediction configuration; `predict()` sends query rows and returns a `PredictionResult` with a DataFrame of predictions and confidence scores.
- **Multiple target columns**: predict several columns in a single call, each with its own task type.
- **Mixed task types**: combine `classification` and `regression` targets in the same request (e.g., predict `COSTCENTER` as classification and `DISCOUNT_RATE` as regression simultaneously).
- **Automatic schema inference**: detects column data types (`string`, `numeric`, `date`) from the DataFrame, or accepts an explicit `data_schema` override.
- **OAuth2 authentication**: acquires and caches access tokens, refreshes them automatically before expiry.
- **Retry with exponential backoff**: retries on transient HTTP errors (429, 500, 502, 503, 504) and on 401 (re-authenticates).
- **Deployment resolution**: resolves the prediction endpoint from a direct URL, a deployment ID, or by querying the AI Core API.
- **Custom error hierarchy**: `RPT1ValidationError`, `RPT1AuthError`, `RPT1RequestError` for targeted exception handling.

### `test_rpt1_client.py`, unit tests for the example client

Seven test cases covering:
- End-to-end `fit`/`predict` happy path (classification)
- Deployment URL resolution (from URL and from ID)
- Input validation failures (missing columns, empty DataFrames, invalid task types)
- Automatic schema inference and explicit schema override
- Multi-target prediction with confidence parsing
- API-level error status handling
- Authentication failure and HTTP retry behavior

### `RPT-1_client.ipynb`, example client tutorial

A step-by-step Jupyter notebook that walks through the complete `RPT1Client` workflow. Use this to see the custom client in action and as a starting point for building your own wrapper:

1. Install dependencies and configure `.env`
2. Initialize the client with `RPT1Client.from_env()`
3. Build context and query DataFrames
4. `fit()` with target columns, index column, and task types
5. `predict()` and inspect `PredictionResult.predictions_df`
6. Read metadata and raw response
7. Use an explicit data schema
8. Predict mixed task types (classification + regression) in a single call

### `RPT-1_request.ipynb`, raw HTTP requests tutorial

A comprehensive Jupyter notebook that demonstrates the full RPT-1 lifecycle without any client library:

1. Authenticate with OAuth2 `client_credentials`
2. Discover available foundation models and find RPT-1 (`sap-rpt-1-small`, `sap-rpt-1-large`)
3. Create a configuration and deployment (or reuse an existing one)
4. Poll deployment status until ready
5. Send prediction requests in **rows** format (records as JSON objects)
6. Send prediction requests in **columns** format (columnar data arrays)
7. Interpret prediction responses (status codes, metadata, confidence scores)

This notebook can optionally create billable AI Core resources (configuration + deployment) if `RPT1_DEPLOYMENT_URL` is not set in the environment.

## Key Concepts

These are the core RPT-1 API building blocks visible across both approaches:

| Concept | Description |
|---|---|
| `prediction_config.target_columns` | Declares which column(s) to predict, the placeholder value, and the task type (`classification` or `regression`). |
| `prediction_placeholder` | A sentinel value placed in target column cells you want the model to fill. Typically `"[PREDICT]"` for classification or a numeric value like `-1` for regression. |
| `index_column` | The column that uniquely identifies each row (e.g., `"ID"`), so predictions can be mapped back to their source rows. |
| `data_schema` | A mapping of column names to `{"dtype": "string" | "numeric" | "date"}`. Can be inferred or declared explicitly. |
| `parse_data_types` | When `true`, the API interprets row values according to the declared schema types. |
| `rows` vs `columns` | Two payload formats for sending tabular data. `rows` sends an array of record objects; `columns` sends a dict of column arrays. Both produce identical results. |
| `task_type` | `"classification"` for categorical targets; `"regression"` for continuous numeric targets. |
| Status codes | `0` = OK, `1` = warning, `2` = invalid input, `3` = server error. |

## Prerequisites

- Python 3.10+
- An SAP AI Core instance with RPT-1 available
- A deployed RPT-1 model (or credentials to create one)

## Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required variables:

| Variable | Description |
|---|---|
| `AICORE_AUTH_URL` | OAuth2 token endpoint for your SAP AI Core instance. |
| `AICORE_CLIENT_ID` | OAuth2 client ID from your service key. |
| `AICORE_CLIENT_SECRET` | OAuth2 client secret from your service key. |
| `AICORE_BASE_URL` | SAP AI Core API base URL (with or without `/v2`). |
| `AICORE_RESOURCE_GROUP` | Resource group for deployments (default: `"default"`). |
| `RPT1_DEPLOYMENT_URL` | Direct URL of your RPT-1 deployment (preferred). |
| `RPT1_DEPLOYMENT_ID` | Alternative: deployment ID (the client resolves the URL via the AI Core API). |

You need either `RPT1_DEPLOYMENT_URL` or `RPT1_DEPLOYMENT_ID`. If neither is set, the raw HTTP notebook can create a deployment for you.

## Install

```bash
cd best-practices/narrow-ai/RPT-1/python
pip install -r requirements.txt
```

Dependencies: `requests`, `python-dotenv`, `pandas`.

## Run

### Example client notebook

```bash
jupyter notebook RPT-1_client.ipynb
```

Or use the example client programmatically:

```python
from rpt1_client import RPT1Client
import pandas as pd

client = RPT1Client.from_env()

context_df = pd.DataFrame([
    {"PRODUCT": "Office Chair", "PRICE": 150.8, "ID": "44", "COSTCENTER": "Office Furniture"},
    {"PRODUCT": "Server Rack",  "PRICE": 2200.0, "ID": "104", "COSTCENTER": "Data Infrastructure"},
])

query_df = pd.DataFrame([
    {"PRODUCT": "Couch", "PRICE": 999.99, "ID": "35"},
])

client.fit(
    context_df,
    target_columns=["COSTCENTER"],
    index_column="ID",
    task_types={"COSTCENTER": "classification"},
)

result = client.predict(query_df)
print(result.predictions_df)
```

### Raw HTTP notebook

```bash
jupyter notebook RPT-1_request.ipynb
```

### Unit tests

```bash
python -m pytest test_rpt1_client.py -v
# or
python -m unittest test_rpt1_client -v
```

## What to Expect

### Example client output

`predict()` returns a `PredictionResult` containing:

```
   ID        COSTCENTER  COSTCENTER__confidence
0  35  Office Furniture                    0.89
```

- **`predictions_df`**: DataFrame with the index column, predicted values, and `<target>__confidence` columns.
- **`metadata`**: dict with `num_columns`, `num_predictions`, `num_query_rows`, `num_rows`.
- **`status_code`** / **`status_message`**: RPT-1 API status (0 = OK).
- **`request_id`**: unique identifier for the prediction request.
- **`raw_response`**: the complete JSON response from the deployment.

### Raw HTTP output

The API returns JSON with this structure:

```json
{
  "id": "<request-uuid>",
  "status": { "code": 0, "message": "ok" },
  "predictions": [
    {
      "ID": "35",
      "COSTCENTER": [
        { "prediction": "Office Furniture", "confidence": 0.97 }
      ]
    }
  ],
  "metadata": {
    "num_columns": 5,
    "num_predictions": 1,
    "num_query_rows": 1,
    "num_rows": 2
  }
}
```

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `401` / `403` | Invalid credentials, expired token, wrong scopes, or mismatched resource group. |
| `404` on `/predict` | Deployment URL is incorrect, or the deployment is not in `RUNNING` state. |
| `422` | Payload shape issue. Check `target_columns`, placeholder values, column names, and `data_schema` consistency. |
| `RPT1ValidationError` | Client-side validation caught the problem before making a request. Read the error message for specifics. |
| Weak predictions | Add more representative context rows, verify data quality, and ensure consistent column types. Prefer explicit `data_schema` and `task_type` for stable results. |
