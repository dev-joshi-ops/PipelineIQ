from pipeline_iq.config import get_settings
from .base import BaseCIProvider


def get_active_provider() -> BaseCIProvider:
    """Factory method to return the active CI/CD provider instance."""
    settings = get_settings()
    provider_name = settings.ci_provider.lower()

    if provider_name == "jenkins":
        from .jenkins import get_jenkins_client
        return get_jenkins_client()
    else:
        # Fallback or future providers (github, gitlab)
        raise ValueError(f"Unsupported CI provider: {provider_name}")
