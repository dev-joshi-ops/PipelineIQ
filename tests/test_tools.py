import pytest
from pipeline_iq.tools.analyze_failure import analyze_build_failure
from pipeline_iq.tools.get_suggestions import get_fix_suggestions
from pipeline_iq.tools.list_jobs import list_jenkins_jobs
from unittest.mock import patch, AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_list_jenkins_jobs_sorting_and_limiting():
    # Mock jobs with different timestamps
    mock_jobs = [
        {
            "name": f"job-{i}",
            "full_name": f"Job {i}",
            "url": "url",
            "is_foldered": False,
            "last_build_at": i * 1000,
        }
        for i in range(15)
    ]

    with patch("pipeline_iq.tools.list_jobs.get_jenkins_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.list_jobs = AsyncMock(return_value=mock_jobs)

        result = await list_jenkins_jobs()

        # Should be limited to 10
        assert len(result.jobs) == 10
        # Should be sorted descending (highest timestamp first)
        assert result.jobs[0].name == "job-14"
        assert result.jobs[9].name == "job-5"


@pytest.mark.asyncio
async def test_analyze_java_compile_error():
    log_lines = [
        "Starting build...",
        "src/Main.java:10: error: cannot find symbol",
        "Finished with error",
    ]

    result = await analyze_build_failure(log_lines)
    assert len(result.patterns) == 1
    assert result.patterns[0].pattern_id == "JAVA_COMPILE_ERROR"


@pytest.mark.asyncio
async def test_get_fix_suggestions():
    pattern_id = "JAVA_COMPILE_ERROR"
    result = await get_fix_suggestions(pattern_id)

    assert result.pattern_id == "JAVA_COMPILE_ERROR"
    assert len(result.suggestions) > 0
    assert result.suggestions[0].manual_steps is not None


@pytest.mark.asyncio
async def test_get_suggestions_unknown_id():
    # With @safe_tool, it won't raise ValueError but return ErrorResponse
    # However, get_fix_suggestions is the internal function, server.py calls it.
    # If we call it directly, it still raises ValueError.
    # But wait, server.py uses @safe_tool which catches it.
    # To test the actual tool as seen by client, we'd test the decorated function.
    with pytest.raises(ValueError):
        await get_fix_suggestions("UNKNOWN_PATTERN")
