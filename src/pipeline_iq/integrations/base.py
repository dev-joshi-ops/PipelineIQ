from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pipeline_iq.schemas.base import BaseResource, BaseBuild, BaseLogResponse


class BaseCIProvider(ABC):
    """Abstract Base Class for all CI/CD providers."""

    @abstractmethod
    async def list_jobs(self, folder: str = "") -> List[Dict[str, Any]]:
        """
        List jobs or resources in a specific folder/scope.
        Returns a list of raw dictionaries that match JobMetadata schema.
        """
        pass

    @abstractmethod
    async def list_builds(self, job_name: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        List build history for a specific job.
        Returns a list of raw dictionaries that match BuildSummary schema.
        """
        pass

    @abstractmethod
    async def get_build_info(self, job_name: str, build_id: str) -> Dict[str, Any]:
        """
        Fetch detailed metadata for a specific build.
        Returns a raw dictionary that match BuildInfoResponse schema.
        """
        pass

    @abstractmethod
    async def get_build_log(self, job_name: str, build_id: str) -> List[str]:
        """
        Fetch the console log for a build.
        Should return the log lines (already sanitized or ready for sanitization).
        """
        pass

    @abstractmethod
    async def close(self):
        """Clean up resources (e.g., close HTTP sessions)."""
        pass
