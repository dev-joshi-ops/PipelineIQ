# Requirement Specification: Jenkins CI/CD Debugging MCP

**Project:** PipelineIQ
**Component:** Jenkins CI/CD Debugging MCP
**Version:** 1.0
**Status:** Draft — Pending BA Sign-Off
**Last Updated:** 2026-04-10

---

## 1. Summary

Development teams lose significant time diagnosing Jenkins build failures by manually navigating the Jenkins UI, reading raw logs, and cross-referencing common error patterns. The Jenkins CI/CD Debugging MCP is a read-only component of PipelineIQ that enables LLMs to retrieve Jenkins build logs, detect common failure patterns through structured analysis, and return human-readable explanations with actionable fix suggestions. This MCP is strictly **read-only** — it does not trigger, abort, configure, or modify any Jenkins resource in any way. All fixes suggested by the MCP must be applied manually by the developer after their own verification.

---

## 2. User Stories

### Story 1: Build Log Retrieval

**As a** Developer,
**I want to** fetch the most recent 2000 lines of a Jenkins build's console log via the MCP,
**So that** I can review the full build output and identify failure points without leaving my development tooling or manually navigating the Jenkins UI.

---

### Story 2: Failure Pattern Detection

**As a** Developer,
**I want to** have the MCP analyze a retrieved build log and detect known failure patterns (e.g., compilation errors, test failures, dependency resolution failures, environment/credential issues),
**So that** I can quickly understand the root cause category of a build failure without manually parsing hundreds of log lines.

---

### Story 3: Actionable Fix Suggestions

**As a** Developer,
**I want to** receive specific, actionable fix suggestions based on the detected failure pattern in a build log,
**So that** I can resolve the build issue efficiently by applying the recommended fix manually after my own review and verification. The MCP will never apply any fix automatically.

---

## 3. Acceptance Criteria

### AC 1: Successful Log Retrieval

```
Given a valid job_name and build_id that exist in Jenkins,
When get_jenkins_build_log is invoked,
Then the tool returns the last 2000 lines of the console log as an ordered array of strings,
And the response is returned within 3 seconds,
And no state in Jenkins is modified as a result.
```

### AC 2: Log Retrieval — Build with Fewer Than 2000 Lines

```
Given a valid job_name and build_id whose log contains fewer than 2000 lines,
When get_jenkins_build_log is invoked,
Then all available log lines are returned without error or truncation warning,
And the response payload clearly indicates the total number of lines returned.
```

### AC 3: Log Retrieval — Invalid Job Name

```
Given a job_name that does not exist in Jenkins,
When get_jenkins_build_log is invoked,
Then the tool returns a structured error response with error code JOB_NOT_FOUND,
And a human-readable message indicating the job name was not found,
And no partial or empty log payload is returned.
```

### AC 4: Log Retrieval — Invalid Build ID

```
Given a valid job_name but a build_id that does not exist for that job,
When get_jenkins_build_log is invoked,
Then the tool returns a structured error response with error code BUILD_NOT_FOUND,
And a human-readable message indicating the build ID was not found for the given job.
```

### AC 5: Log Retrieval — Jenkins Unreachable

```
Given the Jenkins server is unavailable or the network connection times out,
When get_jenkins_build_log is invoked,
Then the tool returns a structured error response with error code CONNECTION_ERROR,
And the response includes the attempted Jenkins base URL and a timeout duration,
And the response is returned within 5 seconds (not left hanging indefinitely).
```

### AC 6: Log Retrieval — Active/In-Progress Build

```
Given a valid job_name and a build_id for a build that is still running,
When get_jenkins_build_log is invoked,
Then the tool returns the log lines available at the moment of the request,
And the response includes a flag is_build_complete: false,
And the response does not block or poll waiting for the build to finish.
```

### AC 7: Failure Pattern Detection — Known Pattern Matched

```
Given a build log has been retrieved and it contains output matching a known failure pattern,
When analyze_build_failure is invoked with that log content,
Then the tool returns a structured result identifying at least one matched failure pattern,
And each matched pattern includes a pattern_id, a human-readable label, and the matching log line range,
And the overall confidence level for the match is included (high / medium / low).
```

### AC 8: Failure Pattern Detection — No Known Pattern Matched

```
Given a build log has been retrieved and it does not match any known failure pattern,
When analyze_build_failure is invoked,
Then the tool returns a result with an empty patterns array,
And a message explicitly stating that no known pattern was matched,
And the tool does NOT return a null response or an error — it returns a structured "no match" result.
```

### AC 9: Fix Suggestions — Suggestion Returned

```
Given a failure analysis result containing at least one matched pattern,
When get_fix_suggestions is invoked with that pattern_id,
Then the tool returns at least one fix suggestion,
And each suggestion includes a title, description, and manual_steps array,
And the response explicitly states the fix must be applied manually by the developer.
```

### AC 10: Fix Suggestions — Unknown Pattern ID

```
Given a pattern_id that is not recognized by the suggestion engine,
When get_fix_suggestions is invoked,
Then the tool returns a structured error response with error code UNKNOWN_PATTERN_ID,
And a message advising the developer to inspect the log manually.
```

### AC 11: Mutability Check (Cross-Cutting)

```
Given any tool in this MCP,
When the tool is executed,
Then it must NOT perform any HTTP POST, PUT, PATCH, or DELETE requests against Jenkins,
And it must only use HTTP GET requests (or equivalent read-only API calls),
And no Jenkins job, build, configuration, or artifact must be created, modified, or deleted as a side effect.
```

### AC 12: Authentication Failure

```
Given an invalid or expired API token is used to connect to Jenkins,
When any tool in this MCP is invoked,
Then the tool returns a structured error response with error code AUTH_FAILURE,
And a message indicating the credentials are invalid or have insufficient permissions,
And no retry is attempted automatically.
```

---

## 4. Non-Functional Requirements

### 4.1 Performance

| Metric | Requirement |
|---|---|
| Log retrieval latency (2000 lines) | ≤ 3 seconds under normal load |
| Log retrieval latency (connection timeout) | ≤ 5 seconds maximum before returning CONNECTION_ERROR |
| Failure analysis latency | ≤ 5 seconds for a 2000-line log |
| Fix suggestion latency | ≤ 2 seconds (lookup-based, no external call) |
| Concurrent requests | Must support at least 10 concurrent tool invocations without degraded performance |

### 4.2 Security

- All Jenkins API calls must use API tokens. Username/password authentication is not permitted.
- Tokens must be stored as environment variables or in a secrets manager; they must never be hardcoded in source.
- API tokens must be scoped to **read-only** Jenkins permissions (e.g., `Job/Read`, `Build/Read`). Write-scoped tokens must be rejected at configuration time with a clear error message.
- Log content may contain secrets (e.g., accidentally printed environment variables). The MCP must not cache or persist log content beyond the duration of a single request.
- Authentication failures must return a generic `AUTH_FAILURE` error — the response must not echo back the token or reveal which credential was used.
- Role-based access: The MCP inherits whatever Jenkins permissions the supplied API token carries. No additional RBAC layer is implemented in Phase 1.

### 4.3 Observability

- All tool invocations must emit a structured log entry containing: tool name, job_name, build_id, response status (success / error code), and latency in milliseconds.
- Errors must include a correlation ID that is returned to the caller and also written to the MCP's own log, to aid support debugging.
- No log content from Jenkins builds must be written to the MCP's own structured logs (to avoid secret leakage in observability pipelines).

### 4.4 Determinism

- `get_jenkins_build_log` is fully deterministic — the same input always returns the same log lines (for a completed build).
- `analyze_build_failure` must use deterministic rule-based pattern matching only. LLM-based or probabilistic analysis is not permitted in Phase 1 to ensure reproducible results.
- `get_fix_suggestions` must return a deterministic suggestion set for a given `pattern_id`. Suggestions must not vary between calls.

### 4.5 Scalability

- Log volume per build can grow. The 2000-line truncation is a deliberate design choice to keep context manageable for LLM consumers. Future pagination (Story 4, Phase 2) will address larger logs.
- The pattern library for `analyze_build_failure` is expected to grow over time. It must be implemented as a versioned, externally configurable rule set, not hardcoded logic, to allow updates without redeployment.

### 4.6 Accessibility

Not applicable. This MCP exposes API/tool endpoints only — there is no user-facing UI in Phase 1.

### 4.7 Localization

Not applicable in Phase 1. All error messages and fix suggestions are in English only. Multi-language support is deferred to Phase 3.

---

## 5. Data Requirements

### 5.1 Log Payload

| Field | Type | Description |
|---|---|---|
| `lines` | `string[]` | Ordered array of console log lines (last 2000 max) |
| `total_lines_returned` | `integer` | Actual count of lines in the response |
| `is_build_complete` | `boolean` | True if build has finished; false if still running |
| `build_result` | `string \| null` | Final build result (SUCCESS, FAILURE, ABORTED, UNSTABLE) or null if in-progress |
| `retrieved_at` | `string` (ISO 8601) | Timestamp of when the log was fetched |

### 5.2 Truncation Policy

- Only the **last 2000 lines** of the console log are returned. This is intentional — build failures are almost always visible near the end of the log.
- If the build log has fewer than 2000 lines, all lines are returned.
- Pagination and retrieval of earlier log segments are out of scope for Phase 1.

### 5.3 PII and Secret Handling

- Build logs may contain sensitive values (API keys, passwords, tokens printed by build scripts). The MCP treats all log content as potentially sensitive.
- Log content must **not** be written to any persistent store, cache, or observability sink by this MCP.
- The MCP does not scan or redact secrets from log content — that is the responsibility of the Jenkins configuration (e.g., Credentials Masking Plugin).

### 5.4 Fixtures / Test Data

- A mock Jenkins API server must be available in the test environment providing:
  - A job with a successful build log (< 2000 lines)
  - A job with a failed build log (exactly 2000 lines, containing each supported failure pattern)
  - A job with an in-progress build (partial log)
  - A job name that does not exist (for 404 testing)
  - An auth-failure scenario (invalid token response)

### 5.5 Retention

- The MCP does not store or retain log data. All data is fetched from Jenkins on-demand per request and discarded after the response is returned.

---

## 6. Tool / Resource Contract

### Tool 1: `get_jenkins_build_log`

**Purpose:** Retrieve the last 2000 lines of a Jenkins build's console log. Read-only. No side effects.

**Input Schema:**

```json
{
  "name": "get_jenkins_build_log",
  "description": "Retrieves (READ-ONLY) the last 2000 lines of the console log for a specified Jenkins build. No state is modified. Returns log lines, build completion status, and build result.",
  "parameters": {
    "type": "object",
    "properties": {
      "job_name": {
        "type": "string",
        "description": "Full Jenkins job name. Use forward slashes for folder-based paths (e.g., 'my-folder/my-job'). Max 512 characters. Allowed characters: alphanumeric, hyphens, underscores, forward slashes, periods.",
        "maxLength": 512,
        "pattern": "^[a-zA-Z0-9_.\\-/]+$"
      },
      "build_id": {
        "type": "string",
        "description": "Jenkins build number as a string (e.g., '42') or the token 'lastBuild', 'lastFailedBuild', 'lastSuccessfulBuild'. Max 20 characters.",
        "maxLength": 20,
        "pattern": "^(lastBuild|lastFailedBuild|lastSuccessfulBuild|lastUnsuccessfulBuild|[1-9][0-9]*)$"
      }
    },
    "required": ["job_name", "build_id"]
  }
}
```

**Success Response:**

```json
{
  "status": "success",
  "correlation_id": "uuid-v4",
  "data": {
    "job_name": "my-folder/my-job",
    "build_id": "42",
    "lines": ["line 1 content", "line 2 content", "..."],
    "total_lines_returned": 2000,
    "is_build_complete": true,
    "build_result": "FAILURE",
    "retrieved_at": "2026-04-10T10:30:00Z"
  }
}
```

**Error Response:**

```json
{
  "status": "error",
  "correlation_id": "uuid-v4",
  "error": {
    "code": "JOB_NOT_FOUND",
    "message": "No Jenkins job found with name 'my-folder/my-job'."
  }
}
```

**Error Codes:**

| Code | HTTP Equivalent | Meaning |
|---|---|---|
| `JOB_NOT_FOUND` | 404 | The specified job_name does not exist |
| `BUILD_NOT_FOUND` | 404 | The build_id does not exist for the given job |
| `AUTH_FAILURE` | 401 / 403 | API token is missing, invalid, or lacks read permission |
| `CONNECTION_ERROR` | 503 / timeout | Jenkins is unreachable or the request timed out |
| `INVALID_INPUT` | 400 | Input fields fail validation (bad characters, exceeded length) |

---

### Tool 2: `analyze_build_failure`

**Purpose:** Analyze log lines from a Jenkins build and detect known failure patterns. Read-only. Deterministic rule-based matching only.

**Input Schema:**

```json
{
  "name": "analyze_build_failure",
  "description": "Analyzes (READ-ONLY) an array of Jenkins build log lines and returns detected failure patterns. Uses deterministic rule-based matching. Returns structured results including pattern IDs, labels, matching line ranges, and confidence levels.",
  "parameters": {
    "type": "object",
    "properties": {
      "log_lines": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Ordered array of build log lines to analyze. Maximum 2000 items.",
        "maxItems": 2000
      }
    },
    "required": ["log_lines"]
  }
}
```

**Success Response (pattern matched):**

```json
{
  "status": "success",
  "correlation_id": "uuid-v4",
  "data": {
    "patterns": [
      {
        "pattern_id": "JAVA_COMPILE_ERROR",
        "label": "Java Compilation Failure",
        "confidence": "high",
        "matching_line_range": { "start": 1420, "end": 1435 },
        "summary": "One or more Java source files failed to compile. Common causes include syntax errors, missing imports, or incompatible API changes."
      }
    ],
    "analyzed_line_count": 2000
  }
}
```

**Success Response (no pattern matched):**

```json
{
  "status": "success",
  "correlation_id": "uuid-v4",
  "data": {
    "patterns": [],
    "analyzed_line_count": 1200,
    "message": "No known failure pattern was detected in the provided log. Manual inspection is recommended."
  }
}
```

**Error Codes:**

| Code | Meaning |
|---|---|
| `INVALID_INPUT` | log_lines is null, empty, or exceeds 2000 items |

---

### Tool 3: `get_fix_suggestions`

**Purpose:** Return a deterministic set of fix suggestions for a known failure pattern. No external calls — lookup-based only. Read-only.

**Input Schema:**

```json
{
  "name": "get_fix_suggestions",
  "description": "Returns (READ-ONLY) actionable fix suggestions for a given Jenkins failure pattern ID. Suggestions are informational only — the developer must apply any fix manually after their own verification. No changes are made to Jenkins or any external system.",
  "parameters": {
    "type": "object",
    "properties": {
      "pattern_id": {
        "type": "string",
        "description": "The pattern_id returned by analyze_build_failure (e.g., 'JAVA_COMPILE_ERROR'). Max 100 characters.",
        "maxLength": 100,
        "pattern": "^[A-Z][A-Z0-9_]*$"
      }
    },
    "required": ["pattern_id"]
  }
}
```

**Success Response:**

```json
{
  "status": "success",
  "correlation_id": "uuid-v4",
  "data": {
    "pattern_id": "JAVA_COMPILE_ERROR",
    "label": "Java Compilation Failure",
    "suggestions": [
      {
        "title": "Check compiler error lines in the log",
        "description": "Identify the specific file and line number from the error message and open the source file to inspect the issue.",
        "manual_steps": [
          "Search the log for lines containing 'error:' to find the specific compiler message.",
          "Open the indicated source file at the reported line number.",
          "Correct the syntax error, missing import, or type mismatch.",
          "Commit the fix and re-run the build."
        ]
      }
    ],
    "disclaimer": "These suggestions are informational only. Review and apply them manually after your own verification. This tool does not modify any code or configuration."
  }
}
```

**Error Codes:**

| Code | Meaning |
|---|---|
| `UNKNOWN_PATTERN_ID` | The provided pattern_id is not present in the suggestion library |
| `INVALID_INPUT` | pattern_id fails format validation |

---

## 7. Edge Cases & Constraints

| # | Scenario | Expected Behavior |
|---|---|---|
| EC-1 | `job_name` contains a forward slash (folder path, e.g., `team/service/job`) | Supported. Forward slashes are valid and must be URL-encoded when calling the Jenkins API internally. |
| EC-2 | `build_id` is `"lastBuild"` and no builds exist yet for the job | Return `BUILD_NOT_FOUND` with a message indicating no builds have been run. |
| EC-3 | Log is empty (0 bytes, build started but produced no output) | Return `lines: []`, `total_lines_returned: 0`, and `is_build_complete` reflecting actual status. No error. |
| EC-4 | Jenkins returns a log mid-write (build is active) | Return whatever lines are available, with `is_build_complete: false`. Do not block or poll. |
| EC-5 | `log_lines` passed to `analyze_build_failure` contains only whitespace/blank lines | Process normally; blank lines do not cause an error. |
| EC-6 | Multiple failure patterns detected in the same log | Return all matched patterns in the `patterns` array, ordered by first matching line number ascending. |
| EC-7 | API token has write permissions (broader than needed) | MCP still only issues GET requests. Write permissions on the token do not cause the MCP to perform write operations. |
| EC-8 | `job_name` or `build_id` contains special characters outside the allowed pattern | Return `INVALID_INPUT` before making any Jenkins API call. |
| EC-9 | Jenkins API responds with HTTP 500 | Return `CONNECTION_ERROR` with the HTTP status code included in the error details. |
| EC-10 | Two concurrent calls for the same job/build | Both are handled independently. No locking or deduplication in Phase 1. |

---

## 8. Out of Scope

The following are explicitly **not** part of this MCP, now or in Phase 1:

- **Any mutating operation**: Triggering, re-running, aborting, or deleting builds.
- **Configuration changes**: Editing Jenkinsfiles, updating job configurations, or modifying pipeline definitions.
- **Automated fix application**: The MCP provides suggestions only. It will never apply a fix to code, configuration, or Jenkins settings.
- **Log pagination**: Retrieval of log segments beyond the last 2000 lines. Deferred to Phase 2.
- **GitHub Actions support**: Deferred to Phase 2.
- **Multi-language error messages / localization**: Deferred to Phase 3.
- **Secret scanning / redaction**: The MCP does not inspect or mask secrets in log content.
- **LLM-based or probabilistic analysis**: Phase 1 uses deterministic rule-based pattern matching only.
- **Build artifact retrieval**: Downloading test reports, coverage files, or other build artifacts.
- **Pipeline visualization**: Displaying stage graphs or pipeline structure.

---

## 9. Sign-Off

| Role | Name | Status | Date |
|---|---|---|---|
| Business Analyst | | ⬜ Pending | |
| Tech Lead | | ⬜ Pending | |
| QA Lead | | ⬜ Pending | |