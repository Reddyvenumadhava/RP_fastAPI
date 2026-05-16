from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.common_schema import SuccessResponse, ErrorResponse
from schemas.lookup_schema import (
    LookupSkillRequest, LookupSkillResponse,
    LookupLanguageRequest, LookupLanguageResponse,
    LookupInterestRequest, LookupInterestResponse,
    LookupCertificationRequest, LookupCertificationResponse,
    LookupCollegeRequest, LookupCollegeResponse,
    LookupCourseRequest, LookupCourseResponse,
    LookupSalutationRequest, LookupSalutationResponse,
    LookupPincodeRequest, LookupPincodeResponse
)
from utils.response_utils import success_response, error_response
from services import lookup_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/skill", response_model=SuccessResponse)
def lookup_skill(request: LookupSkillRequest, db: Session = Depends(get_db)):
    """Finds or creates a skill."""
    try:
        result = lookup_service.find_or_create_skill(db, request.name, request.complexity)
        return success_response(result.model_dump())
    except Exception as e:
        logger.error(f"Error in /lookup/skill: {e}")
        return error_response(str(e), status_code=400)


@router.post("/language", response_model=SuccessResponse)
def lookup_language(request: LookupLanguageRequest, db: Session = Depends(get_db)):
    """Language lookup is not modeled in NaukriDB."""
    return error_response("Language lookup is not supported in NaukriDB", status_code=501)


@router.post("/interest", response_model=SuccessResponse)
def lookup_interest(request: LookupInterestRequest, db: Session = Depends(get_db)):
    """Interest lookup is not modeled in NaukriDB."""
    return error_response("Interest lookup is not supported in NaukriDB", status_code=501)


@router.post("/certification", response_model=SuccessResponse)
def lookup_certification(request: LookupCertificationRequest, db: Session = Depends(get_db)):
    """Finds or creates a certification."""
    try:
        result = lookup_service.find_or_create_certification(
            db,
            request.certification_name,
            request.issuing_organization,
            request.certification_type or "General",
            request.is_lifetime
        )
        return success_response(result.model_dump())
    except Exception as e:
        logger.error(f"Error in /lookup/certification: {e}")
        return error_response(str(e), status_code=400)


@router.post("/college", response_model=SuccessResponse)
def lookup_college(request: LookupCollegeRequest, db: Session = Depends(get_db)):
    """College lookup is folded into company/company-like records in NaukriDB."""
    return error_response("College lookup is not supported in NaukriDB", status_code=501)


@router.post("/course", response_model=SuccessResponse)
def lookup_course(request: LookupCourseRequest, db: Session = Depends(get_db)):
    """Course lookup is not modeled in NaukriDB."""
    return error_response("Course lookup is not supported in NaukriDB", status_code=501)


@router.post("/salutation", response_model=SuccessResponse)
def lookup_salutation(request: LookupSalutationRequest, db: Session = Depends(get_db)):
    """Salutation lookup is not modeled in NaukriDB."""
    return error_response("Salutation lookup is not supported in NaukriDB", status_code=501)


@router.post("/pincode", response_model=SuccessResponse)
def lookup_pincode(request: LookupPincodeRequest, db: Session = Depends(get_db)):
    """Pincode lookup is not modeled in NaukriDB."""
    return error_response("Pincode lookup is not supported in NaukriDB", status_code=501)
