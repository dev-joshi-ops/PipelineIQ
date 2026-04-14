import datetime
from pipeline_iq.integrations import get_active_provider
from pipeline_iq.schemas.jenkins import BuildLogResponse
from pipeline_iq.utils.sanitizer import sanitize_log_lines


async def get_jenkins_build_log(job_name: str, build_id: str) -> BuildLogResponse:
    """
    Retrieves and sanitizes the last 2000 lines of the console log for a Jenkins build.
    """
    client = get_active_provider()

    # Fetch build info to check status/result
    # No need to validate here, server.py already did it
    build_info = await client.get_build_info(job_name, build_id)

    # Fetch log lines
    lines = await client.get_build_log(job_name, build_id)

    # Redact secrets
    sanitized_lines = sanitize_log_lines(lines)

    from pipeline_iq.schemas.jenkins import map_jenkins_status
    status = map_jenkins_status(
        build_info.get("result"), build_info.get("building", False)
    )

    return BuildLogResponse(
        resource_id=job_name,
        build_id=build_id,
        lines=sanitized_lines,
        total_lines_returned=len(sanitized_lines),
        is_complete=not build_info.get("building", False),
        status=status,
        build_result=build_info.get("result"),
        retrieved_at=datetime.datetime.now(),
    )
