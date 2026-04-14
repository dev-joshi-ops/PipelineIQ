from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
import datetime


class CIStatus(str, Enum):
    """Generic CI/CD build status."""

    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    IN_PROGRESS = "IN_PROGRESS"
    CANCELLED = "CANCELLED"
    UNSTABLE = "UNSTABLE"
    UNKNOWN = "UNKNOWN"


class BaseResource(BaseModel):
    """Generic CI/CD resource (e.g., Job, Repository, Pipeline)."""

    id: str = Field(..., description="Unique identifier for the resource")
    name: str = Field(..., description="Human-readable name")
    full_name: str = Field(..., description="Absolute path or full name of the resource")
    url: str = Field(..., description="Web URL for the resource")
    is_container: bool = Field(False, description="True if this resource contains other resources (e.g., a Folder)")


class BaseBuild(BaseModel):
    """Generic CI/CD build or workflow run."""

    build_id: str = Field(..., description="Unique identifier for the build")
    resource_id: str = Field(..., description="ID of the parent resource")
    number: int = Field(..., description="Sequential build number")
    status: CIStatus = Field(CIStatus.UNKNOWN, description="Current build status")
    url: str = Field(..., description="Web URL for the build")
    timestamp: datetime.datetime = Field(..., description="When the build started")
    duration_ms: Optional[int] = Field(None, description="Duration in milliseconds if complete")


class BaseLogResponse(BaseModel):
    """Generalized build log response."""

    resource_id: str
    build_id: str
    lines: List[str]
    is_complete: bool
    status: CIStatus
    retrieved_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
