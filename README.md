# 🚀 PipelineIQ: CI/CD Intelligence Layer

[![CI](https://github.com/dev-joshi-ops/PipelineIQ/actions/workflows/ci.yml/badge.svg)](https://github.com/dev-joshi-ops/PipelineIQ/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pipeline-iq?style=for-the-badge)](https://pypi.org/project/pipeline-iq/)
[![FastMCP](https://img.shields.io/badge/Framework-FastMCP-green?style=for-the-badge)](https://github.com/modelcontextprotocol/python-sdk)

**PipelineIQ** is a high-performance Model Context Protocol (MCP) server that empowers LLMs to diagnose CI/CD failures with surgical precision. By bridging the gap between raw logs and actionable insights, PipelineIQ slashes MTTR and eliminates context-switching fatigue for modern DevOps teams. 🛠️

---

### ⚡ TL;DR
Stop hunting through Jenkins console output. PipelineIQ gives your LLM (Claude, GPT) direct, structured access to **Jenkins** logs, offering automated **Failure Pattern Detection** and **Sensitive Data Redaction** to get your builds back to green faster and safer. 🚀

---

### ✨ Core Features

#### 🔍 Advanced Log Pattern Matching
PipelineIQ doesn't just "read" logs—it analyzes them across a vast tech stack:
- **Liferay / OSGi**: Bundle resolution and Blade CLI deployment errors.
- **Java / Spring Boot**: Compilation, dependency conflicts, and bean creation failures.
- **Node.js / React**: ESLint violations, Vite/Webpack compilation, and Hydration mismatches.
- **Python / Django / FastAPI**: Import errors, migration conflicts, and Pydantic validation.
- **Infrastructure**: Out-of-memory (OOM) kills, timeouts, and Docker build failures.

#### 🛡️ Built-in Security (Log Redaction)
PipelineIQ automatically redacts sensitive information (passwords, API tokens, keys) from build logs before they are sent to the LLM, ensuring your secrets stay private.

#### 🤖 Industry-Standard MCP
Built on **FastMCP**, PipelineIQ follows the latest Model Context Protocol standards, providing:
- **Recursive Job Discovery**: Navigate deep Jenkins folder structures with ease.
- **Standardized Tools**: `list_jobs`, `list_builds`, `get_build_info`, `get_build_log`, `analyze_failure`, and `get_suggestions`.
- **Diagnostic Prompt**: A pre-defined `debug-failure` prompt to guide AI agents.
- **Patterns Resource**: Access internal failure patterns via `patterns://config`.

### 🛠️ Tool Reference

| Tool | Purpose |
|------|---------|
| `list_jobs` | Discover Jenkins jobs and folders (sorted by latest activity). |
| `list_builds` | List history for a specific job. |
| `get_build_info` | Get metadata (status, duration, timestamp) for a build. |
| `get_build_log` | Fetch and sanitize console output. |
| `analyze_failure` | Detect known failure patterns in logs. |
| `get_suggestions` | Get actionable fix instructions for detected patterns. |

---

### 🚀 Quick Start (using `uvx`)

No installation required! Run PipelineIQ instantly using `uvx`:

```bash
uvx pipeline-iq
```

---

### 🔑 Jenkins API Token Setup

Follow these steps to generate a secure API token:

1.  **Generate Token**:
    *   Log in to your Jenkins dashboard.
    *   Click on your **Username** (top right) > **Configure**.
    *   Locate the **API Token** section and click **Add new Token**.
    *   Provide a name (e.g., `PipelineIQ`) and click **Generate**.
    *   **IMPORTANT**: Copy the token immediately; it will not be shown again.

2.  **Required Permissions**:
    PipelineIQ requires the following **Read-Only** permissions (using Matrix Authorization or Role-Based Strategy):
    *   **Overall**: `Read`
    *   **Job**: `Read`, `Extended Read` (to view logs)
    *   **View**: `Read`

> [!TIP]
> Always follow the **Principle of Least Privilege**. Use a dedicated service account if possible rather than your personal admin account.

---

### ⚙️ Installation & Configuration

#### Recommended: Install via pip
```bash
pip install pipeline-iq
```

#### From Source
```bash
# Clone the repo
git clone https://github.com/dev-joshi-ops/PipelineIQ.git

# Initialize virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies (Editable Mode)
pip install -e .

# OR run instantly using uv (no manual install needed)
uv run pipeline-iq
```

#### Environment Configuration 🔒

Create a `.env` file in the root directory or export these variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JENKINS_URL` | Yes | — | Base URL of Jenkins server |
| `JENKINS_USER` | Yes | — | Jenkins username |
| `JENKINS_TOKEN` | Yes | — | Jenkins API token (read-only) |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity (`DEBUG`, `INFO`, etc.) |
| `MAX_LOG_LINES` | No | `2000` | Max lines to retrieve from build log |
| `REQUEST_TIMEOUT` | No | `30` | HTTP request timeout in seconds |

Example `.env`:
```env
JENKINS_URL=https://jenkins.yourdomain.com
JENKINS_USER=admin
JENKINS_TOKEN=your_api_token_here
```

---

### 🔌 Client Configuration (Recommended: `uvx`)

The easiest way to use PipelineIQ is with `uvx`.

#### 1. Claude Desktop
Edit your `claude_desktop_config.json` (Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "pipeline-iq": {
      "command": "uvx",
      "args": ["pipeline-iq"],
      "env": {
        "JENKINS_URL": "https://your-jenkins-url",
        "JENKINS_USER": "your-username",
        "JENKINS_TOKEN": "your-api-token"
      }
    }
  }
}
```

#### 2. Antigravity
Edit your `mcp_config.json` (Windows: `%APPDATA%\.gemini\antigravity\mcp_config.json`):

```json
{
  "mcpServers": {
    "pipeline-iq": {
      "command": "uvx",
      "args": ["pipeline-iq"],
      "env": {
        "JENKINS_URL": "https://your-jenkins-url",
        "JENKINS_USER": "your-username",
        "JENKINS_TOKEN": "your-api-token"
      }
    }
  }
}
```

---

### ⚙️ Development Setup (Manual)

If you want to contribute or run from source:

```bash
# Clone the repo
git clone https://github.com/dev-joshi-ops/PipelineIQ.git

# Initialize virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies (Editable Mode)
pip install -e .
```
---

### ✍️ About the Author
Built with <3 by Dev Joshi

---

### 📄 License
MIT © 2026 PipelineIQ
