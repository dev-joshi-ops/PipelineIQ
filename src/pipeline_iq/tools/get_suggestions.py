from pipeline_iq.schemas.jenkins import FixSuggestionsResponse, FixSuggestion
from pipeline_iq.resources.pattern_loader import get_pattern_loader


async def get_fix_suggestions(pattern_id: str) -> FixSuggestionsResponse:
    """
    Returns actionable fix suggestions for a given Jenkins failure pattern ID.
    """
    loader = get_pattern_loader()
    selected_pattern = loader.get_pattern(pattern_id)

    if not selected_pattern:
        # Note: In a production app, we might raise a custom exception
        # that the server handles and returns as an ErrorResponse.
        raise ValueError(f"The pattern_id '{pattern_id}' is not recognized.")

    suggestions = [
        FixSuggestion(
            title=s["title"], description=s["description"], manual_steps=s["manual_steps"]
        )
        for s in selected_pattern["suggestions"]
    ]

    return FixSuggestionsResponse(
        pattern_id=selected_pattern["pattern_id"],
        label=selected_pattern["label"],
        suggestions=suggestions,
    )
