from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator
import datetime
import re

# Reusable regex patterns for validation
JOB_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_.\-/]+$")
BUILD_ID_PATTERN = re.compile(r"^[1-9][0-9]*$")
ALLOWED_BUILD_TOKENS = {
    "lastBuild",
    "lastFailedBuild",
    "lastSuccessfulBuild",
    "lastUnsuccessfulBuild",
}
FOLDER_PATTERN = re.compile(r"^[a-zA-Z0-9_.\-/]*$")  # Allow empty


class ErrorResponse(BaseModel):
    """Unified error response for all tools."""

    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict] = Field(None, description="Additional error context")


class JobMetadata(BaseModel):
    """Metadata for a Jenkins job."""

    name: str
    full_name: str
    url: str
    is_foldered: bool = False
    last_build_at: Optional[datetime.datetime] = None
    last_build_result: Optional[str] = None


class JobListResponse(BaseModel):
    """Response model for list_jenkins_jobs."""

    jobs: List[JobMetadata]
    total_count: int


class BuildLogRequest(BaseModel):
    """Request model for get_jenkins_build_log."""

    job_name: str = Field(
        ..., description="Full Jenkins job name. Use forward slashes for folders."
    )
    build_id: str = Field(..., description="Build number or token like 'lastBuild'")

    @field_validator("job_name")
    @classmethod
    def validate_job_name(cls, v: str) -> str:
        if not JOB_NAME_PATTERN.match(v):
            raise ValueError(
                "Invalid characters in job_name. Only alphanumeric, dash, underscore, dot, and slash are allowed."
            )
        if ".." in v:
            raise ValueError("Path traversal sequences are not allowed in job_name.")
        return v

    @field_validator("build_id")
    @classmethod
    def validate_build_id(cls, v: str) -> str:
        if v in ALLOWED_BUILD_TOKENS:
            return v
        if not BUILD_ID_PATTERN.match(v):
            raise ValueError("build_id must be a positive integer or a valid Jenkins token.")
        return v


class FolderRequest(BaseModel):
    """Request model for list_jenkins_jobs."""

    folder: str = Field("", description="Optional folder path to start discovery from.")

    @field_validator("folder")
    @classmethod
    def validate_folder(cls, v: str) -> str:
        if not FOLDER_PATTERN.match(v):
            raise ValueError("Invalid characters in folder path.")
        if ".." in v:
            raise ValueError("Path traversal sequences are not allowed.")
        return v


class BuildLogResponse(BaseModel):
    """Response model for get_jenkins_build_log."""

    job_name: str
    build_id: str
    lines: List[str]
    total_lines_returned: int
    is_build_complete: bool
    build_result: Optional[str]
    retrieved_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class FailurePatternMatch(BaseModel):
    """A matched failure pattern."""

    pattern_id: str
    label: str
    confidence: str
    matching_line_range: Dict[str, int]  # {"start": int, "end": int}
    summary: str


class FailureAnalysisResponse(BaseModel):
    """Response model for analyze_build_failure."""

    patterns: List[FailurePatternMatch]
    analyzed_line_count: int
    message: Optional[str] = None


class FixSuggestion(BaseModel):
    """A specific fix suggestion."""

    title: str
    description: str
    manual_steps: List[str]


class FixSuggestionsResponse(BaseModel):
    """Response model for get_fix_suggestions."""

    pattern_id: str
    label: str
    suggestions: List[FixSuggestion]
    disclaimer: str = "These suggestions are informational only. Review and apply them manually."


class BuildSummary(BaseModel):
    """Brief summary of a build."""

    number: int
    result: Optional[str]
    url: str
    timestamp: datetime.datetime


class BuildListResponse(BaseModel):
    """Response model for list_jenkins_builds."""

    job_name: str
    builds: List[BuildSummary]
    count: int


class BuildInfoResponse(BaseModel):
    """Detailed metadata for a specific build."""

    job_name: str
    number: int
    result: Optional[str]
    url: str
    timestamp: datetime.datetime
    duration: int = Field(..., description="Duration in milliseconds")
    building: bool
    description: Optional[str] = None
    artifacts: List[Dict] = []
    actions: List[Dict] = []
