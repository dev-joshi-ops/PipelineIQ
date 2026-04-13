import re
from typing import List
from loguru import logger

# Common secret patterns (tokens, passwords, keys)
# Note: These are heuristics and may need updates as new patterns are discovered.
SECRET_PATTERNS = [
    # Key-value pairs like password=mysecret or token: my-token
    # Use capturing groups to preserve the key and redact only the value
    (
        r"(password|token|secret|api_key|apikey|auth|pass|pwd|key)(\s*[=:]\s*)(\S+)",
        r"\1\2[REDACTED]",
    ),
    # Authorization headers
    (r"(bearer\s+)(\S+)", r"\1[REDACTED]"),
    (r"(basic\s+)([A-Za-z0-9+/=]+)", r"\1[REDACTED]"),
    # Specific token formats (e.g., Jenkins/GitHub style tokens)
    (r"\b([A-Za-z0-9]{40})\b", r"[REDACTED]"),
    # URLs with embedded credentials
    (r"(https?://)([^:]+:[^@]+)(@\S+)", r"\1[REDACTED]\3"),
]


def sanitize_log_lines(lines: List[str]) -> List[str]:
    """
    Redacts sensitive information from a list of log lines.
    """
    sanitized = []
    redaction_count = 0

    for line in lines:
        new_line = line
        for pattern, replacement in SECRET_PATTERNS:
            new_line, count = re.subn(pattern, replacement, new_line, flags=re.IGNORECASE)
            if count > 0:
                redaction_count += count
        sanitized.append(new_line)

    if redaction_count > 0:
        logger.debug(f"Sanitized {redaction_count} lines containing potential secrets.")

    return sanitized
