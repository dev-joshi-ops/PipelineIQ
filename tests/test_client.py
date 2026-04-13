import pytest
import respx
import httpx
from unittest.mock import patch, MagicMock
from pydantic import SecretStr
from pipeline_iq.schemas.jenkins import BuildLogRequest


@pytest.fixture
def mock_settings():
    with patch("pipeline_iq.integrations.jenkins_client.get_settings") as mock:
        mock_val = MagicMock()
        mock_val.jenkins_url = "http://jenkins.test"
        mock_val.jenkins_user = "user"
        mock_val.jenkins_token = SecretStr("token")
        mock_val.request_timeout = 5
        mock_val.max_log_lines = 2000
        mock.return_value = mock_val
        yield mock_val


@pytest.mark.asyncio
async def test_jenkins_client_get_build_log(mock_settings):
    from pipeline_iq.integrations.jenkins_client import JenkinsClient

    client = JenkinsClient()
    job_name = "test-job"
    build_id = "1"

    with respx.mock:
        respx.get("http://jenkins.test/job/test-job/1/consoleText").mock(
            return_value=httpx.Response(200, text="line1\nline2\nline3")
        )

        log_lines = await client.get_build_log(job_name, build_id)
        assert log_lines == ["line1", "line2", "line3"]
        await client.close()


@pytest.mark.asyncio
async def test_jenkins_client_get_build_info(mock_settings):
    from pipeline_iq.integrations.jenkins_client import JenkinsClient

    client = JenkinsClient()
    job_name = "test-job"
    build_id = "1"

    with respx.mock:
        respx.get("http://jenkins.test/job/test-job/1/api/json").mock(
            return_value=httpx.Response(200, json={"building": False, "result": "SUCCESS"})
        )

        info = await client.get_build_info(job_name, build_id)
        assert info["result"] == "SUCCESS"
        assert info["building"] is False
        await client.close()


def test_build_log_request_validation():
    # Valid
    req = BuildLogRequest(job_name="folder/job", build_id="42")
    assert req.job_name == "folder/job"

    # Invalid job name
    with pytest.raises(ValueError):
        BuildLogRequest(job_name="job space", build_id="42")

    # Invalid build id
    with pytest.raises(ValueError):
        BuildLogRequest(job_name="job", build_id="abc")


@pytest.mark.asyncio
async def test_jenkins_client_list_jobs(mock_settings):
    from pipeline_iq.integrations.jenkins_client import JenkinsClient

    client = JenkinsClient()

    mock_response = {
        "jobs": [
            {
                "name": "job-alpha",
                "fullName": "Job Alpha",
                "url": "http://alpha",
                "_class": "hudson.model.FreeStyleProject",
                "lastBuild": {"timestamp": 1000, "result": "SUCCESS"},
            },
            {
                "name": "job-beta",
                "fullName": "Job Beta",
                "url": "http://beta",
                "_class": "hudson.model.FreeStyleProject",
                "lastBuild": {"timestamp": 2000, "result": "FAILURE"},
            },
        ]
    }

    with respx.mock:
        respx.get("http://jenkins.test/api/json").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

        jobs = await client.list_jobs()
        assert len(jobs) == 2
        assert jobs[0]["name"] == "job-alpha"
        assert jobs[0]["last_build_at"] == 1000
        assert jobs[1]["last_build_result"] == "FAILURE"
        await client.close()
