import httpx
from typing import List, Dict, Any, Optional
from loguru import logger
from pipeline_iq.config import get_settings
from pipeline_iq.integrations.base import BaseCIProvider


class JenkinsClient(BaseCIProvider):
    """Persistent client for interacting with Jenkins API."""

    _client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Lazy-loaded persistent httpx client."""
        if self._client is None:
            settings = get_settings()
            auth = (settings.jenkins_user, settings.jenkins_token.get_secret_value())
            self._client = httpx.AsyncClient(
                auth=auth,
                timeout=httpx.Timeout(settings.request_timeout, connect=5.0),
                base_url=settings.jenkins_url.rstrip("/"),
                headers={"Accept": "application/json"},
                follow_redirects=False,
            )
            logger.info("Initialized Jenkins persistence client")
        return self._client

    async def close(self):
        """Closes the underlying httpx client."""
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.info("Jenkins client session closed.")

    def _get_job_url_path(self, job_name: str) -> str:
        """Constructs a Jenkins-compliant URL path for jobs, including folder support."""
        # Jenkins folder jobs follow the pattern job/folder/job/subfolder/job/jobname
        segments = job_name.strip("/").split("/")
        return "/".join(f"job/{s}" for s in segments)

    async def list_jobs(self, folder: str = "") -> List[Dict[str, Any]]:
        """
        Recursively discovers Jenkins jobs.

        Args:
            folder: Optional folder path to start discovery from.

        Returns:
            A list of job metadata dictionaries.
        """
        url_path = self._get_job_url_path(folder) if folder else ""
        path = f"{url_path}/api/json" if url_path else "api/json"

        try:
            tree = "jobs[name,fullName,url,color,_class,lastBuild[timestamp,result]]"
            response = await self.client.get(path, params={"tree": tree})
            response.raise_for_status()
            data = response.json()

            jobs = []
            for job in data.get("jobs", []):
                # Is it a folder? (Common class name for folders)
                is_folder = "Folder" in job.get(
                    "_class", ""
                ) or "WorkflowMultiBranchProject" in job.get("_class", "")

                last_build = job.get("lastBuild")
                job_meta = {
                    "name": job["name"],
                    "full_name": job["fullName"],
                    "url": job["url"],
                    "is_foldered": is_folder,
                    "last_build_at": last_build.get("timestamp") if last_build else None,
                    "last_build_result": last_build.get("result") if last_build else None,
                }
                jobs.append(job_meta)

            return jobs
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to list jobs in '{folder}': {e.response.status_code} {e.response.text}"
            )
            raise
        except Exception as e:
            logger.error(f"Unexpected error listing jobs: {e}")
            raise

    async def get_build_info(self, job_name: str, build_id: str) -> Dict[str, Any]:
        """Fetch build metadata from Jenkins."""
        job_path = self._get_job_url_path(job_name)
        path = f"{job_path}/{build_id}/api/json"

        try:
            response = await self.client.get(path)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to get build info for {job_name} #{build_id}: {e.response.status_code}"
            )
            raise

    async def get_build_log(self, job_name: str, build_id: str) -> List[str]:
        """Fetch the console log for a Jenkins build."""
        job_path = self._get_job_url_path(job_name)
        path = f"{job_path}/{build_id}/consoleText"

        try:
            response = await self.client.get(path)
            response.raise_for_status()

            settings = get_settings()
            lines = response.text.splitlines()
            return lines[-settings.max_log_lines :]
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Failed to fetch logs for {job_name} #{build_id}: {e.response.status_code}"
            )
            raise

    async def list_builds(self, job_name: str, count: int = 10) -> List[Dict[str, Any]]:
        """Fetch the latest builds for a specific job."""
        job_path = self._get_job_url_path(job_name)
        # Fetch build numbers, results, urls, and timestamps
        path = f"{job_path}/api/json"
        tree = f"builds[number,url,result,timestamp]{{0,{count}}}"

        try:
            response = await self.client.get(path, params={"tree": tree})
            response.raise_for_status()
            data = response.json()
            return data.get("builds", [])
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to fetch builds for {job_name}: {e.response.status_code}")
            raise
