import datetime
from pipeline_iq.integrations.jenkins_client import get_jenkins_client
from pipeline_iq.schemas.jenkins import BuildInfoResponse


async def get_jenkins_build_info(job_name: str, build_id: str) -> BuildInfoResponse:
    """
    Retrieves detailed metadata for a specific Jenkins build.
    """
    client = get_jenkins_client()
    data = await client.get_build_info(job_name, build_id)

    return BuildInfoResponse(
        job_name=job_name,
        number=data["number"],
        result=data.get("result"),
        url=data["url"],
        timestamp=datetime.datetime.fromtimestamp(data["timestamp"] / 1000.0),
        duration=data["duration"],
        building=data["building"],
        description=data.get("description"),
        artifacts=data.get("artifacts", []),
        actions=data.get("actions", []),
    )
