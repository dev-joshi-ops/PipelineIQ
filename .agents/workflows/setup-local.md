---
description: Bootstrap the local development environment from a fresh clone
---

# Setup Local Development Environment

## Prerequisites
- **Git** installed
- **Python** 3.11 or 3.12
- Access to test credentials for Jenkins or GitHub only if you need live integration checks
- A code editor (VS Code recommended)

## Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-name>
```

### 2. Setup Environment Variables
```bash
cp .env.example .env
```
Edit `.env` with local values only when live provider access is needed.

### 3. Create a Virtual Environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
```

### 4. Install the Package
```bash
pip install -e .
```

### 5. Start the MCP Server
```bash
python -m pipeline_iq.server
```
Verify that the process starts cleanly and advertises the expected MCP transport.

## Verification Checklist
- [ ] Virtual environment is active
- [ ] Package installs in editable mode without dependency errors
- [ ] Server starts without import or configuration failures
- [ ] `pytest` runs successfully for at least one unit test
- [ ] A representative tool can be exercised with local fixtures
