import datetime
from pipeline_iq.integrations.jenkins_client import get_jenkins_client
from pipeline_iq.schemas.jenkins import BuildListResponse, BuildSummary


async def list_jenkins_builds(job_name: str, count: int = 10) -> BuildListResponse:
    """
    Lists the latest builds for a specific Jenkins job.
    """
    client = get_jenkins_client()
    raw_builds = await client.get_latest_builds(job_name, count)

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
