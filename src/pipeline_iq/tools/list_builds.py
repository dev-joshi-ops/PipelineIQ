import datetime
from pipeline_iq.integrations import get_active_provider
from pipeline_iq.schemas.jenkins import BuildListResponse, BuildSummary


async def list_jenkins_builds(job_name: str, count: int = 10) -> BuildListResponse:
    """
    Lists the latest builds for a specific Jenkins job.
    """
    client = get_active_provider()
    raw_builds = await client.list_builds(job_name, count)

    builds = [
        BuildSummary(
            number=b["number"],
            result=b.get("result"),
            url=b["url"],
            timestamp=datetime.datetime.fromtimestamp(b["timestamp"] / 1000.0),
        )
        for b in raw_builds
    ]

    return BuildListResponse(job_name=job_name, builds=builds, count=len(builds))
