import json
import os
from functools import lru_cache
from typing import List, Dict, Any
from loguru import logger


class PatternLoader:
    """Singleton loader for failure patterns."""

    _instance = None
    _patterns = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PatternLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._patterns is None:
            self._load()

    def _load(self):
        """Loads and parses the patterns JSON file."""
        patterns_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "resources", "patterns.json"
        )
        try:
            with open(patterns_path, "r") as f:
                data = json.load(f)
                self._patterns = data.get("patterns", [])
                logger.info(f"Loaded {len(self._patterns)} failure patterns from {patterns_path}")
        except Exception as e:
            logger.error(f"Failed to load patterns from {patterns_path}: {e}")
            self._patterns = []

    def get_patterns(self) -> List[Dict[str, Any]]:
        """Returns the list of loaded failure patterns."""
        return self._patterns

    def get_pattern(self, pattern_id: str) -> Dict[str, Any]:
        """Returns a specific pattern by ID."""
        return next((p for p in self._patterns if p["pattern_id"] == pattern_id), None)


@lru_cache()
def get_pattern_loader() -> PatternLoader:
    """Returns a cached PatternLoader instance."""
    return PatternLoader()
