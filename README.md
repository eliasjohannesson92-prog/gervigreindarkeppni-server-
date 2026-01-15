# gervigreindarkeppni-server-
Gervigreindarkeppni Íslands 2026

## Competition-Ready FastAPI Service

This is a competition-ready FastAPI service scaffold for Gervigreindarkeppni. It provides robust endpoints, input validation, structured logging, and Azure deployment automation.

## Features

- **Health & Version Endpoints**: Monitor service health and version information
- **Predict Endpoint**: Generic prediction endpoint with Pydantic validation
- **Request ID Tracking**: Automatic request ID generation and propagation
- **Structured Logging**: JSON-formatted logs with request IDs
- **Configuration**: Environment variable based configuration
- **Tests**: Comprehensive test suite with pytest
- **Azure Deployment**: Automated deployment via GitHub Actions

## API Endpoints

### GET /health
Health check endpoint.

**Response:**
```json
{"status": "ok"}
```

### GET /version
Returns version and runtime information.

**Response:**
```json
{
  "status": "ok",
  "git_sha": "abc1234",
  "python_version": "3.12.0",
  "challenge": "unknown"
}
```

### POST /predict
Generic prediction endpoint.

**Request:**
```json
{
  "inputs": <any valid JSON>
}
```

**Response:**
```json
{
  "outputs": <any valid JSON>
}
```

## Configuration

Configure the service using environment variables:

- `CHALLENGE`: Challenge identifier (default: `"unknown"`)
- `LOG_LEVEL`: Logging level (default: `"INFO"`)
- `MODEL_PATH`: Optional path to model files

## Local Development

### Prerequisites

- Python 3.12 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd gervigreindarkeppni-server-
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

Run the development server with uvicorn:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at http://localhost:8000

- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Running Tests

Run the test suite with pytest:

```bash
pytest -q
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Azure Deployment

The service automatically deploys to Azure App Service when changes are pushed to the `main` branch.

### Setup

1. **Create an Azure App Service** (if not already created):
   - Go to Azure Portal
   - Create a new Web App
   - Select Python 3.12 runtime
   - Note the app name (e.g., `gervi2026`)

2. **Configure GitHub Secrets**:
   - The workflow uses Azure authentication via OpenID Connect (OIDC)
   - The following secrets are already configured in this repository:
     - `AZUREAPPSERVICE_CLIENTID_*`
     - `AZUREAPPSERVICE_TENANTID_*`
     - `AZUREAPPSERVICE_SUBSCRIPTIONID_*`

3. **Update Workflow Configuration**:
   - The current app name is `gervi2026`
   - To deploy to a different app, update the `app-name` in `.github/workflows/main_gervi2026.yml`

### Deployment Process

The GitHub Actions workflow:
1. Checks out the code
2. Sets up Python 3.12
3. Installs dependencies
4. Generates build info (git SHA and run number)
5. Creates deployment artifact (excluding virtual environment)
6. Authenticates with Azure
7. Deploys to Azure App Service using ZIP deploy

### Manual Deployment

To trigger a manual deployment:
1. Go to the Actions tab in GitHub
2. Select the "Build and deploy Python app to Azure Web App" workflow
3. Click "Run workflow"

## Request ID Support

The service automatically handles request IDs:
- If `X-Request-ID` header is provided, it will be used
- If not provided, a UUID will be generated
- The request ID is included in all logs and returned in response headers

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   └── main.py           # FastAPI application
├── challenges/           # Challenge-specific implementations
│   ├── nlp/
│   ├── image/
│   └── rl/
├── tests/
│   ├── __init__.py
│   └── test_api.py       # API tests
├── .github/
│   └── workflows/
│       └── main_gervi2026.yml  # Azure deployment workflow
├── main.py               # Entry point (imports from app.main)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## License

[Add license information]
