from mcp.server.fastmcp import FastMCP
from pipeline_iq.config import configure_logging
from pipeline_iq.tools import safe_tool
from pipeline_iq.tools.get_build_log import get_jenkins_build_log
from pipeline_iq.tools.analyze_failure import analyze_build_failure
from pipeline_iq.tools.get_suggestions import get_fix_suggestions
from pipeline_iq.tools.list_jobs import list_jenkins_jobs
from pipeline_iq.tools.list_builds import list_jenkins_builds
from pipeline_iq.tools.get_build_info import get_jenkins_build_info
from pipeline_iq.resources.pattern_loader import get_pattern_loader
from pipeline_iq.integrations.jenkins_client import get_jenkins_client
from pipeline_iq.schemas.jenkins import FolderRequest, BuildLogRequest

from pipeline_iq import __version__

# Initialize FastMCP server
mcp = FastMCP("PipelineIQ", version=__version__)

# --- Tools ---


@mcp.tool()
@safe_tool
async def list_jobs(folder: str = ""):
    """
    Lists Jenkins jobs, optionally within a specific folder.
    Use this to discover available jobs for build log retrieval.
    """
    # Validation
    FolderRequest(folder=folder)
    return await list_jenkins_jobs(folder)


@mcp.tool()
@safe_tool
async def list_builds(job_name: str, count: int = 10):
    """
    Lists the latest builds for a specific Jenkins job.
    """
    # Validation & Bounding
    BuildLogRequest(job_name=job_name, build_id="1")  # Reusing for job_name check
    count = min(max(count, 1), 100)
    return await list_jenkins_builds(job_name, count)


@mcp.tool()
@safe_tool
async def get_build_info(job_name: str, build_id: str):
    """
    Retrieves detailed metadata for a specific Jenkins build.
    """
    # Validation
    BuildLogRequest(job_name=job_name, build_id=build_id)
    return await get_jenkins_build_info(job_name, build_id)


@mcp.tool()
@safe_tool
async def get_build_log(job_name: str, build_id: str):
    """
    Retrieves and sanitizes the last 2000 lines of the console log for a Jenkins build.
    """
    # Explicit validation
    BuildLogRequest(job_name=job_name, build_id=build_id)
    return await get_jenkins_build_log(job_name, build_id)


@mcp.tool()
@safe_tool
async def analyze_failure(log_lines: list[str]):
    """
    Analyzes Jenkins build log lines and returns detected failure patterns.
    """
    # Input Bounding
    if len(log_lines) > 5000:
        log_lines = log_lines[-5000:]
    return await analyze_build_failure(log_lines)


@mcp.tool()
@safe_tool
async def get_suggestions(pattern_id: str):
    """
    Returns actionable fix suggestions for a given Jenkins failure pattern ID.
    """
    return await get_fix_suggestions(pattern_id)


# --- Resources ---


@mcp.resource("patterns://config")
def get_patterns_config() -> str:
    """Exposes the internal failure patterns configuration."""
    loader = get_pattern_loader()
    import json

    return json.dumps(loader.get_patterns(), indent=2)


# --- Prompts ---


@mcp.prompt("debug-failure")
def debug_failure_prompt(job_name: str, build_id: str):
    """Template for diagnosing a CI/CD build failure."""
    return f"""
I need help diagnosing a build failure in Jenkins.
Job: {job_name}
Build ID: {build_id}

Please follow these steps:
1. Fetch the build logs using `get_build_log`.
2. Analyze the logs for failure patterns using `analyze_failure`.
3. If patterns are found, get actionable suggestions using `get_suggestions`.
4. Explain the root cause and provide clear fix instructions.
"""


def main():
    """Synchronous entry point for the console script."""
    configure_logging()
    try:
        mcp.run()
    finally:
        # Safe cleanup of singleton client session
        client = get_jenkins_client()
        if client._client is not None:
            import asyncio

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(client.close())
                else:
                    loop.run_until_complete(client.close())
            except Exception:
                # Best effort cleanup
                pass


if __name__ == "__main__":
    main()
