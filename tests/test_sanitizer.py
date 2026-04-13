from pipeline_iq.utils.sanitizer import sanitize_log_lines


def test_sanitize_password_equals():
    lines = ["Starting build...", "database_password=mysecret123", "Finished."]
    sanitized = sanitize_log_lines(lines)
    assert sanitized[1] == "database_password=[REDACTED]"
    assert sanitized[0] == "Starting build..."


def test_sanitize_bearer_token():
    lines = ["Authorization: Bearer my-secret-token-1234567"]
    sanitized = sanitize_log_lines(lines)
    assert sanitized[0] == "Authorization: Bearer [REDACTED]"


def test_sanitize_basic_auth():
    lines = ["Authorization: Basic dXNlcjpwYXNzd29yZA=="]
    sanitized = sanitize_log_lines(lines)
    assert sanitized[0] == "Authorization: Basic [REDACTED]"


def test_sanitize_jenkins_token_heuristic():
    # Jenkins tokens are often 40 character hex/alphanumeric
    token = "a" * 40
    lines = [f"Using token {token} for auth"]
    sanitized = sanitize_log_lines(lines)
    assert sanitized[0] == "Using token [REDACTED] for auth"


def test_sanitize_embedded_url_creds():
    lines = ["Cloning from https://user:pass@github.com/repo.git"]
    sanitized = sanitize_log_lines(lines)
    assert sanitized[0] == "Cloning from https://[REDACTED]@github.com/repo.git"


def test_no_secrets_no_redaction():
    lines = ["Build successful", "All tests passed"]
    sanitized = sanitize_log_lines(lines)
    assert sanitized == lines
