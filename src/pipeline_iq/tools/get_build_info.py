import datetime
from pipeline_iq.integrations import get_active_provider
from pipeline_iq.schemas.jenkins import BuildInfoResponse, map_jenkins_status


async def get_jenkins_build_info(job_name: str, build_id: str) -> BuildInfoResponse:
    """
    Retrieves detailed metadata for a specific Jenkins build.
    """
    client = get_active_provider()
    data = await client.get_build_info(job_name, build_id)

    return BuildInfoResponse(
        resource_id=job_name,
        build_id=build_id,
        number=data["number"],
        status=map_jenkins_status(data.get("result"), data.get("building", False)),
        url=data["url"],
        timestamp=datetime.datetime.fromtimestamp(data["timestamp"] / 1000.0),
        duration_ms=data["duration"],
        building=data["building"],
        description=data.get("description"),
        artifacts=data.get("artifacts", []),
        actions=data.get("actions", []),
    )
