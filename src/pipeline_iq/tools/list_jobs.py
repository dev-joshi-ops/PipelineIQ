import datetime
from pipeline_iq.integrations.jenkins_client import get_jenkins_client
from pipeline_iq.schemas.jenkins import JobListResponse, JobMetadata


async def list_jenkins_jobs(folder: str = "") -> JobListResponse:
    """
    Lists Jenkins jobs, optionally within a specific folder.
    Use this to discover available jobs for build log retrieval.
    """
    client = get_jenkins_client()
    raw_jobs = await client.list_jobs(folder)

    # Sort jobs by last_build_at descending, putting None at the end
    raw_jobs.sort(key=lambda x: x.get("last_build_at") or 0, reverse=True)

    # Limit to 10 jobs as requested
    top_jobs = raw_jobs[:10]

    jobs = []
    for j in top_jobs:
        lb_at = j.get("last_build_at")
        last_build_at = datetime.datetime.fromtimestamp(lb_at / 1000.0) if lb_at else None

        jobs.append(
            JobMetadata(
                name=j["name"],
                full_name=j["full_name"],
                url=j["url"],
                is_foldered=j["is_foldered"],
                last_build_at=last_build_at,
                last_build_result=j.get("last_build_result"),
            )
        )

    return JobListResponse(jobs=jobs, total_count=len(jobs))
