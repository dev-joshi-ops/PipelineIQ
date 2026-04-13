---
name: performance-profiler
description: Profile MCP startup, tool execution latency, provider API calls, parsing overhead, and large-log handling. Use when tool calls feel slow, CI debugging output is delayed, or you need a repeatable performance audit and follow-up optimization plan.
---

# Performance Profiler

## Steps

### 1. Define Baseline Metrics
Before optimizing, measure the current state.

#### Server Metrics
| Metric | How to Measure | Target |
|---|---|---|
| Server startup time | Measure process launch to ready state | Keep local startup fast and predictable |
| Tool latency (p50, p95) | Structured timing logs or profiler | p95 should stay within agreed SLO |
| Provider call latency | Instrument outbound client timings | Identify slow calls and retry churn |
| Payload processing time | Time normalization, parsing, and heuristic stages | Keep dominant hotspots visible |
| Memory growth on large logs | Profile bounded large-log analysis | No unbounded growth with representative fixtures |

### 2. Profile Server Startup
```bash
py-spy record -o profile.svg -- python -m pipeline_iq.server
```

Look for:
- [ ] Slow import chains
- [ ] Excessive work during registration
- [ ] Eager network calls or config loading during startup

### 3. Profile Tool Execution
- Instrument representative tool calls end to end.
- Measure validation time, provider call time, parse time, and render time separately.
- Identify tools with p95 outliers or highly variable performance.
- Check whether expensive repeated work should be cached or memoized safely.

### 4. Profile Provider Interactions
- Review timeouts, retries, pagination, and log download paths.
- Look for:
  - [ ] Over-fetching large logs when only a window is needed
  - [ ] Repeated metadata calls that could be coalesced
  - [ ] Retry storms during provider throttling
  - [ ] Slow decompression or archive handling

### 5. Stress Large-Log Handling
- Use representative large fixtures from `tests/fixtures/`.
- Measure:
  - [ ] Truncation behavior
  - [ ] Chunking and paging costs
  - [ ] Regex or heuristic hot spots
  - [ ] Peak memory usage

### 6. Document Findings
Create an audit report:

```markdown
## Performance Audit - <Date>

### Summary
- Startup time: XXXms - pass/fail
- Tool p95: XXXms - pass/fail
- Large-log analysis memory: XXXMB - pass/fail

### Findings
| # | Area | Issue | Impact | Fix | Effort |
|---|---|---|---|---|---|
| 1 | Integration | GitHub log download fetches entire archive unnecessarily | High | Add bounded window retrieval | 2h |
| 2 | Parsing | Regex backtracking on noisy logs | Medium | Replace with anchored patterns | 1h |

### Action Items
- [ ] Create tickets for each finding
- [ ] Prioritize by impact and effort
```

### 7. Create Optimization Tickets
For each finding, create a ticket following `.agents/rules/pm.md`:
- Include title, priority, story points, description, and acceptance criteria.
- Link back to the audit report.
