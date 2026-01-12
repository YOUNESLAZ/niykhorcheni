# NIDS ML API

This is a FastAPI-based implementation of the Network Intrusion Detection System (NIDS) described in the project report. It provides an interface to classify network flows as "Normal" or "Attack" and identify the attack category.

## Features

- **FastAPI** for high-performance REST API.
- **Hierarchical Classification**: Supports Binary (Normal/Attack) and Multi-class (DoS, Exploit, etc.) classification.
- **Dockerized**: Ready for deployment.
- **Mock Mode**: Runs with simulated models if trained `.joblib` files are not present.

## Setup

### Prerequisites

- Python 3.9+ OR Docker

### Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Test the API:
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.
   - Or run the included test script:
     ```bash
     python test_api.py
     ```

### Running with Docker

1. Build the image:
   ```bash
   docker build -t nids-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 nids-api
   ```

## Model Files

Place your trained models in the root directory:
- `binary_model.joblib`
- `multiclass_model.joblib`

If not found, the system defaults to a **Mock Model** for testing purposes.
