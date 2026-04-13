---
description: Safely integrate a third-party API with error handling, retry logic, and testability
---

# Add Third-Party API Integration Workflow

## When to Use
When integrating with any external service (payment gateway, email provider, maps API, analytics, AI model, etc.).

## Steps

### 1. Research & Document
Before writing any code:
- [ ] Read the API documentation thoroughly.
- [ ] Identify: authentication method, rate limits, pricing, SLA guarantees.
- [ ] Document the integration in an ADR (see `write-adr.md`):
  - Why this provider? What alternatives were considered?
  - What happens if the service goes down?

### 2. Create an API Service Wrapper
Create a dedicated integration module. Never call external APIs directly from MCP handlers:

```
src/pipeline_iq/integrations/
├── __init__.py
├── base.py              # Shared HTTP client behavior and safety defaults
├── <provider>.py        # Provider-specific wrapper
└── <provider>_types.py  # Provider payload normalization helpers
```

#### Base Client Pattern
```python
# src/pipeline_iq/integrations/base.py
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class ExternalServiceBase:
    def __init__(self, base_url: str, api_key: str, timeout: float = 10.0):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def _request(self, method: str, path: str, **kwargs):
        response = await self.client.request(method, path, **kwargs)
        response.raise_for_status()
        return response.json()
```

#### Provider Wrapper Pattern
```python
# src/pipeline_iq/integrations/<provider>.py
from pipeline_iq.integrations.base import ExternalServiceBase
from pipeline_iq.config import settings

class StripeService(ExternalServiceBase):
    def __init__(self):
        super().__init__(
            base_url="https://api.stripe.com/v1",
            api_key=settings.STRIPE_API_KEY,
        )

    async def create_payment_intent(self, amount: int, currency: str = "usd"):
        return await self._request("POST", "/payment_intents", data={
            "amount": amount,
            "currency": currency,
        })
```

Prefer realistic provider names for this repository, such as `jenkins.py` or `github_actions.py`.

### 3. Add Configuration
Add required environment variables to `src/pipeline_iq/config.py`:
```python
class Settings(BaseSettings):
    # ... existing settings ...
    GITHUB_TOKEN: str | None = None
    JENKINS_URL: str | None = None
    JENKINS_USER: str | None = None
    JENKINS_API_TOKEN: str | None = None
```
Update `.env.example` with placeholder values.

### 4. Add Error Handling
Define provider-specific exceptions:
```python
# src/pipeline_iq/exceptions.py
class ExternalServiceError(Exception):
    """Base exception for external API failures."""
    def __init__(self, service: str, message: str, status_code: int = 502):
        self.service = service
        self.message = message
        self.status_code = status_code
```

Handle gracefully in the MCP handler:
```python
try:
    result = await github_actions_client.fetch_run_logs(run_id=1000)
except ExternalServiceError as e:
    return {"error": {"service": e.service, "message": e.message, "status_code": e.status_code}}
```

### 5. Add Circuit Breaker (Optional but Recommended)
For critical integrations, prevent cascading failures:
```python
# pip install circuitbreaker
from circuitbreaker import circuit

class StripeService(ExternalServiceBase):
    @circuit(failure_threshold=5, recovery_timeout=30)
    async def create_payment_intent(self, amount: int, currency: str = "usd"):
        ...
```

### 6. Create Mock for Testing
```python
# tests/fixtures/mock_github_actions.py
class MockGitHubActionsClient:
    async def fetch_run_logs(self, run_id: int):
        return {
            "run_id": run_id,
            "status": "completed",
            "log_excerpt": "Process completed successfully",
        }
```

Use in tests by injecting the mock client into the handler or integration boundary:
```python
# tests/conftest.py
@pytest.fixture
def mock_github_actions_client():
    return MockGitHubActionsClient()
```

### 7. Write Tests
```python
# tests/unit/test_github_actions_client.py
async def test_fetch_run_logs_success(mock_github_actions_client):
    result = await mock_github_actions_client.fetch_run_logs(run_id=1000)
    assert result["run_id"] == 1000

async def test_fetch_run_logs_service_down(client):
    # Mock the service to raise ExternalServiceError
    ...
```

### 8. Integration Checklist
- [ ] ADR documented (why this provider, alternatives, failure handling)
- [ ] Integration wrapper in `src/pipeline_iq/integrations/<provider>.py`
- [ ] Credentials in `config.py` and `.env.example`
- [ ] Retry logic with exponential backoff
- [ ] Circuit breaker for critical integrations
- [ ] Custom error handling (`ExternalServiceError`)
- [ ] Mock created for testing
- [ ] Unit tests (success + failure scenarios)
- [ ] Integration test with real API on staging (optional)
- [ ] Rate limits documented and respected
