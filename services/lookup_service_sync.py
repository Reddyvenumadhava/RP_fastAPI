"""Compatibility wrapper for legacy imports.

The project now uses the PostgreSQL/NaukriDB-specific lookup service in
services.lookup_service. This module re-exports the supported helpers so older
imports keep working without duplicating table-specific logic.
"""

from services.lookup_service import (  # noqa: F401
    find_or_create_skill,
    find_or_create_certification,
    find_or_create_language,
    find_or_create_interest,
    find_or_create_college,
    find_or_create_course,
    find_salutation,
    find_pincode,
)
