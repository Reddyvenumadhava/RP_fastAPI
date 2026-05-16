from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from schemas.lookup_schema import (
    LookupSkillResponse,
    LookupLanguageResponse,
    LookupInterestResponse,
    LookupCertificationResponse,
    LookupCollegeResponse,
    LookupCourseResponse,
    LookupSalutationResponse,
    LookupPincodeResponse,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Supported NaukriDB lookups
# ---------------------------------------------------------------------------

def find_or_create_skill(db: Session, name: str, complexity: str = "Intermediate") -> LookupSkillResponse:
    """Finds or creates a skill in tbl_cd_skills."""
    logger.debug(f"Looking up skill: {name}")

    result = db.execute(
        text("SELECT skill_id, skill_name, skill_category FROM tbl_cd_skills WHERE LOWER(skill_name) = LOWER(:name)"),
        {"name": name},
    )
    existing = result.fetchone()
    if existing:
        return LookupSkillResponse(skill_id=existing[0], name=existing[1], complexity=existing[2], is_new=False)

    next_id = db.execute(text("SELECT COALESCE(MAX(skill_id), 0) + 1 FROM tbl_cd_skills")).scalar()
    db.execute(
        text(
            """INSERT INTO tbl_cd_skills (skill_id, skill_name, skill_category, description)
            VALUES (:id, :name, :category, :description)"""
        ),
        {
            "id": next_id,
            "name": name,
            "category": complexity,
            "description": "No description",
        },
    )
    db.commit()
    return LookupSkillResponse(skill_id=next_id, name=name, complexity=complexity, is_new=True)


def find_or_create_certification(
    db: Session,
    certification_name: str,
    issuing_organization: str,
    certification_type: str = "General",
    is_lifetime: bool = None,
) -> LookupCertificationResponse:
    """Finds or creates a certification in tbl_cd_certifications."""
    logger.debug(f"Looking up certification: {certification_name} from {issuing_organization}")

    result = db.execute(
        text(
            """SELECT certification_id
            FROM tbl_cd_certifications
            WHERE LOWER(certification_name) = LOWER(:name)
            AND LOWER(issuing_organization) = LOWER(:org)"""
        ),
        {"name": certification_name, "org": issuing_organization},
    )
    existing = result.fetchone()
    if existing:
        return LookupCertificationResponse(
            certification_id=existing[0],
            certification_name=certification_name,
            certification_code="N/A",
            issuing_organization=issuing_organization,
            is_new=False,
        )

    next_id = db.execute(text("SELECT COALESCE(MAX(certification_id), 0) + 1 FROM tbl_cd_certifications")).scalar()
    db.execute(
        text(
            """INSERT INTO tbl_cd_certifications
            (certification_id, certification_name, issuing_organization, certification_category, validity_months, description)
            VALUES (:id, :name, :org, :category, :validity_months, :description)"""
        ),
        {
            "id": next_id,
            "name": certification_name,
            "org": issuing_organization,
            "category": certification_type,
            "validity_months": None,
            "description": None,
        },
    )
    db.commit()
    return LookupCertificationResponse(
        certification_id=next_id,
        certification_name=certification_name,
        certification_code="N/A",
        issuing_organization=issuing_organization,
        is_new=True,
    )


# ---------------------------------------------------------------------------
# Unsupported legacy lookups
# ---------------------------------------------------------------------------

def find_or_create_language(db: Session, language_name: str) -> LookupLanguageResponse:
    raise NotImplementedError("Language lookup is not modeled in NaukriDB")


def find_or_create_interest(db: Session, name: str) -> LookupInterestResponse:
    raise NotImplementedError("Interest lookup is not modeled in NaukriDB")


def find_or_create_college(db: Session, college_name: str) -> LookupCollegeResponse:
    raise NotImplementedError("College lookup is not modeled in NaukriDB")


def find_or_create_course(db: Session, course_name: str, specialization_name: str = "General") -> LookupCourseResponse:
    raise NotImplementedError("Course lookup is not modeled in NaukriDB")


def find_salutation(db: Session, value: str) -> LookupSalutationResponse:
    raise NotImplementedError("Salutation lookup is not modeled in NaukriDB")


def find_pincode(db: Session, pincode: str) -> LookupPincodeResponse:
    raise NotImplementedError("Pincode lookup is not modeled in NaukriDB")
