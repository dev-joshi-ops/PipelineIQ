from functools import lru_cache
from .client import JenkinsClient


@lru_cache()
def get_jenkins_client() -> JenkinsClient:
    """Returns a cached JenkinsClient instance."""
    return JenkinsClient()
