import re
from typing import List
from pipeline_iq.schemas.jenkins import FailureAnalysisResponse, FailurePatternMatch
from pipeline_iq.resources.pattern_loader import get_pattern_loader


async def analyze_build_failure(log_lines: List[str]) -> FailureAnalysisResponse:
    """
    Analyzes Jenkins build log lines and returns detected failure patterns.
    """
    loader = get_pattern_loader()
    patterns = loader.get_patterns()
    matched_patterns = []

    for pattern in patterns:
        regex = pattern["regex"]
        try:
            compiled_regex = re.compile(regex)
            for i, line in enumerate(log_lines):
                if compiled_regex.search(line):
                    matched_patterns.append(
                        FailurePatternMatch(
                            pattern_id=pattern["pattern_id"],
                            label=pattern["label"],
                            confidence=pattern["confidence"],
                            matching_line_range={"start": i, "end": i},
                            summary=pattern["summary"],
                        )
                    )
                    # Break after first match for this pattern
                    break
        except re.error:
            # Skip invalid regexes in patterns.json
            continue

    return FailureAnalysisResponse(
        patterns=matched_patterns,
        analyzed_line_count=len(log_lines),
        message="No known failure pattern was detected in the provided log."
        if not matched_patterns
        else None,
    )
