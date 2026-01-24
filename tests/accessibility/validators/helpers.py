"""Shared helper utilities for accessibility validators."""

from __future__ import annotations

from typing import Optional

from bs4 import Tag


def _format_violation(message: str, filename: str = "index.html", element: Optional[Tag] = None) -> str:
    """Format an accessibility violation message consistently.

    Args:
        message: Human-readable description of the violation.
        filename: Optional filename for error reporting.
        element: Optional HTML element involved in violation.

    Returns:
        Formatted violation message string.
    """
    violation = f"{filename}: {message}"
    if element is not None:
        violation += f" [line approx. {getattr(element, 'sourceline', 'unknown')}]"
    return violation
