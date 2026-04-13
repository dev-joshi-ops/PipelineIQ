# ADR 001: Selection of FastMCP for MCP Server Implementation

## Status
Accepted

## Context
Initial implementation of PipelineIQ used a proprietary Antigravity Python SDK. While functional, it lacked industry-standard decorators and metadata handling common in the broader MCP ecosystem. The requirement is to build a production-ready CI/CD debugger that is compatible with multiple agents (Antigravity, Claude, etc.).

## Decision
We decided to migrate the entire MCP server implementation from the Antigravity SDK to **FastMCP (`mcp`)**.

## Rationale
1.  **Standard Compliance**: FastMCP is the industry standard for Python-based MCP servers.
2.  **Developer Experience**: FastMCP provides clean decorators (`@mcp.tool`, `@mcp.resource`) which simplify registration and improve readability.
3.  **Automatic Validation**: FastMCP handles Pydantic validation for tool parameters out of the box.
4.  **Metadata Support**: Native support for tool descriptions and names, which are critical for LLM tool discovery.
5.  **Community Support**: Larger ecosystem of examples and community-driven improvements.

## Consequences
1.  **Breaking Changes**: Existing tool registration logic had to be rewritten.
2.  **Return Type Changes**: Tools must now return MCP-compliant content objects rather than arbitrary dictionaries.
3.  **Dependency Change**: `antigravity` SDK dependency was replaced by `mcp[cli]`.
