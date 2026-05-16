from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
from datetime import date
from schemas.student_schema import SaveStudentRequest, SaveStudentResponse
from schemas.education_schema import SaveSchoolRequest, SaveEducationRequest
from schemas.workexp_schema import SaveWorkExpRequest, SaveWorkExpResponse
from schemas.project_schema import SaveProjectRequest, SaveProjectResponse
from schemas.address_schema import SaveAddressRequest, SaveAddressResponse
from utils.date_utils import safe_date

logger = logging.getLogger(__name__)


def save_student(db: Session, data: SaveStudentRequest) -> SaveStudentResponse:
    """
    Saves a student record to tbl_cp_student.
    Returns existing student_id if email already exists.
    
    Parameters:
        db: Database session
        data: SaveStudentRequest with student details
        
    Returns:
        SaveStudentResponse with student_id and already_exists flag
    """
    logger.debug(f"Checking if student exists: {data.email}")
    
    # Check if candidate with same email exists in new NaukriDB table
    result = db.execute(
        text("SELECT candidate_id FROM tbl_cd_candidates WHERE email = :email"),
        {"email": data.email}
    )
    existing = result.fetchone()

    if existing:
        logger.debug(f"Candidate already exists: {existing[0]}")
        return SaveStudentResponse(candidate_id=existing[0], already_exists=True)

    # Apply defaults and safe parsing
    date_of_birth = safe_date(data.date_of_birth, date(1900, 1, 1))

    # Insert new candidate (MySQL)
    insert_sql = text(
        """
        INSERT INTO tbl_cd_candidates
        (email, phone, first_name, middle_name, last_name, date_of_birth, current_location,
         gender, linkedin_url, github_url, portfolio_url, profile_summary, is_active)
        VALUES
        (:email, :phone, :first_name, :middle_name, :last_name, :date_of_birth, :current_city,
         :gender, :linkedin_url, :github_url, :portfolio_url, :profile_summary, :is_active)
        """
    )

    result = db.execute(
        insert_sql,
        {
            "email": data.email,
            "phone": data.contact_number,
            "first_name": data.first_name,
            "middle_name": data.middle_name or '',
            "last_name": data.last_name or '',
            "date_of_birth": date_of_birth,
            "current_city": data.current_city or 'Not Specified',
            "gender": data.gender or 'Prefer Not to Say',
            "linkedin_url": data.linkedin_url or '',
            "github_url": data.github_url or '',
            "portfolio_url": data.portfolio_url or '',
            "profile_summary": None,
            "is_active": True
        }
    )
    new_id = result.lastrowid
    db.commit()
    logger.debug(f"Candidate saved: {new_id}")

    return SaveStudentResponse(candidate_id=new_id, already_exists=False)


def save_school(db: Session, data: SaveSchoolRequest):
    """
    Saves a school record to tbl_cp_student_school.
    
    Parameters:
        db: Database session
        data: SaveSchoolRequest with school details
        
    Returns:
        dict with school_id
    """
    logger.debug(f"Saving school for student: {data.student_id}")
    
    # Store school-level education in tbl_cd_education with degree set to standard.
    insert_sql = text(
        """
        INSERT INTO tbl_cd_education
        (candidate_id, institution_name, degree, field_of_study, start_date, end_date, is_pursuing, grading_system, score_obtained, maximum_score)
        VALUES
        (:candidate_id, :institution_name, :degree, :field_of_study, :start_date, :end_date, :is_pursuing, :grading_system, :score_obtained, :maximum_score)
        """
    )

    result = db.execute(
        insert_sql,
        {
            "candidate_id": data.student_id,
            "institution_name": data.school_name or 'Not Specified',
            "degree": data.standard,
            "field_of_study": data.board or 'General',
            "start_date": safe_date(None, None),
            "end_date": safe_date(None, None),
            "is_pursuing": False,
            "grading_system": data.grading_system or 'Percentage Marks of 100 Maximum',
            "score_obtained": data.score_obtained or data.percentage or 0.00,
            "maximum_score": data.maximum_score or 100.00
        }
    )
    new_id = result.lastrowid
    db.commit()
    logger.debug(f"School saved as education record: {new_id}")
    return {"education_id": new_id}


def save_education(db: Session, data: SaveEducationRequest):
    """
    Saves a college education record to tbl_cp_student_education.
    
    Parameters:
        db: Database session
        data: SaveEducationRequest with education details
        
    Returns:
        dict with edu_id
    """
    logger.debug(f"Saving education for student: {data.student_id}")
    
    # Insert college education into tbl_cd_education using direct NaukriDB fields.
    insert_sql = text(
        """
        INSERT INTO tbl_cd_education
        (candidate_id, institution_name, degree, field_of_study, start_date, end_date, is_pursuing, grading_system, score_obtained, maximum_score)
        VALUES
        (:candidate_id, :institution_name, :degree, :field_of_study, :start_date, :end_date, :is_pursuing, :grading_system, :score_obtained, :maximum_score)
        """
    )

    result = db.execute(
        insert_sql,
        {
            "candidate_id": data.student_id,
            "institution_name": data.institution_name,
            "degree": data.degree,
            "field_of_study": data.field_of_study,
            "start_date": safe_date(data.start_date, None),
            "end_date": safe_date(data.end_date, None),
            "is_pursuing": data.is_pursuing or False,
            "grading_system": data.grading_system or 'Scale 10 Grading System',
            "score_obtained": data.score_obtained,
            "maximum_score": data.maximum_score
        }
    )
    new_id = result.lastrowid
    db.commit()
    logger.debug(f"Education saved: {new_id}")
    return {"education_id": new_id}


def save_workexp(db: Session, data: SaveWorkExpRequest) -> SaveWorkExpResponse:
    """
    Saves a work experience record to tbl_cp_student_workexp.
    
    Parameters:
        db: Database session
        data: SaveWorkExpRequest with work experience details
        
    Returns:
        SaveWorkExpResponse with workexp_id
    """
    logger.debug(f"Saving work experience for student: {data.student_id}")
    
    # Insert into tbl_cd_experience (MySQL)
    start_date = safe_date(data.start_date, date(1900, 1, 1))
    if data.is_current:
        end_date = None
    else:
        end_date = safe_date(data.end_date, date(1900, 1, 1))

    insert_sql = text(
        """
        INSERT INTO tbl_cd_experience
        (candidate_id, company_id, company_name, job_title_id, job_title, employment_type, location, start_date, end_date, is_current, work_description, achievements)
        VALUES
        (:candidate_id, :company_id, :company_name, :job_title_id, :job_title, :employment_type, :location, :start_date, :end_date, :is_current, :work_description, :achievements)
        """
    )

    result = db.execute(
        insert_sql,
        {
            "candidate_id": data.student_id,
            "company_id": None,
            "company_name": data.company_name,
            "job_title_id": None,
            "job_title": data.designation or 'Not Specified',
            "employment_type": data.employment_type or 'Full-Time',
            "location": data.company_location or 'Not Specified',
            "start_date": start_date,
            "end_date": end_date,
            "is_current": data.is_current,
            "work_description": None,
            "achievements": None
        }
    )
    new_id = result.lastrowid
    db.commit()
    logger.debug(f"Work experience saved: {new_id}")
    return SaveWorkExpResponse(workexp_id=new_id)


def save_project(db: Session, data: SaveProjectRequest) -> SaveProjectResponse:
    """
    Saves a project record to tbl_cp_studentprojects.
    
    Parameters:
        db: Database session
        data: SaveProjectRequest with project details
        
    Returns:
        SaveProjectResponse with project_id
    """
    logger.debug(f"Saving project for student: {data.student_id}")
    
    # Insert into tbl_cd_projects (MySQL)
    start_date = safe_date(data.project_start_date, date(1900, 1, 1))
    end_date = safe_date(data.project_end_date, date(1900, 1, 1))

    insert_sql = text(
        """
        INSERT INTO tbl_cd_projects
        (candidate_id, project_title, project_description, project_url, start_date, end_date, is_current, technologies_used, achievements, team_size, role)
        VALUES
        (:candidate_id, :project_title, :project_description, :project_url, :start_date, :end_date, :is_current, :technologies_used, :achievements, :team_size, :role)
        """
    )

    result = db.execute(
        insert_sql,
        {
            "candidate_id": data.student_id,
            "project_title": data.project_title,
            "project_description": data.project_description,
            "project_url": None,
            "start_date": start_date,
            "end_date": end_date,
            "is_current": False,
            "technologies_used": None,
            "achievements": data.achievements,
            "team_size": None,
            "role": None
        }
    )
    new_id = result.lastrowid
    db.commit()
    logger.debug(f"Project saved: {new_id}")
    return SaveProjectResponse(project_id=new_id)


def save_project_skill(db: Session, project_id: int, skill_id: int):
    """
    Saves a project-skill many-to-many relationship to tbl_cp_m2m_studentproject_skill.
    Does not error if relationship already exists.
    
    Parameters:
        db: Database session
        project_id: Project ID
        skill_id: Skill ID
        
    Returns:
        dict with already_exists flag
    """
    logger.debug(f"Saving project skill: project_id={project_id}, skill_id={skill_id}")
    
    # Map project skill to candidate skill: find candidate for project, then insert into tbl_cd_candidate_skills
    res = db.execute(text("SELECT candidate_id FROM tbl_cd_projects WHERE project_id = :project_id"), {"project_id": project_id})
    row = res.fetchone()
    if not row:
        logger.debug("Project not found for project_skill insertion")
        return {"already_exists": False, "note": "project_not_found"}

    candidate_id = row[0]

    # Check if candidate skill already exists
    exists = db.execute(
        text("SELECT candidate_skill_id FROM tbl_cd_candidate_skills WHERE candidate_id = :candidate_id AND skill_id = :skill_id"),
        {"candidate_id": candidate_id, "skill_id": skill_id}
    )
    if exists.fetchone():
        logger.debug("Project skill already exists as candidate skill")
        return {"already_exists": True}

    db.execute(
        text("INSERT INTO tbl_cd_candidate_skills (candidate_id, skill_id) VALUES (:candidate_id, :skill_id)"),
        {"candidate_id": candidate_id, "skill_id": skill_id}
    )
    db.commit()
    logger.debug("Project skill saved as candidate skill")
    return {"already_exists": False}


def save_student_skill(db: Session, student_id: int, skill_id: int):
    """
    Saves a student-skill many-to-many relationship to tbl_cp_m2m_std_skill.
    Does not error if relationship already exists.
    
    Parameters:
        db: Database session
        student_id: Student ID
        skill_id: Skill ID
        
    Returns:
        dict with already_exists flag
    """
    logger.debug(f"Saving student skill: student_id={student_id}, skill_id={skill_id}")
    
    # Check if already exists
    result = db.execute(
        text("SELECT candidate_skill_id FROM tbl_cd_candidate_skills WHERE candidate_id = :candidate_id AND skill_id = :skill_id"),
        {"candidate_id": student_id, "skill_id": skill_id}
    )

    if result.fetchone():
        logger.debug(f"Candidate skill already exists")
        return {"already_exists": True}

    # Insert new relationship
    db.execute(
        text("INSERT INTO tbl_cd_candidate_skills (candidate_id, skill_id) VALUES (:candidate_id, :skill_id)"),
        {"candidate_id": student_id, "skill_id": skill_id}
    )
    db.commit()
    logger.debug(f"Candidate skill saved")

    return {"already_exists": False}


def save_student_language(db: Session, student_id: int, language_id: int):
    """
    Saves a student-language many-to-many relationship to tbl_cp_m2m_std_lng.
    
    Parameters:
        db: Database session
        student_id: Student ID
        language_id: Language ID
        
    Returns:
        dict with already_exists flag
    """
    logger.debug(f"Saving student language: student_id={student_id}, language_id={language_id}")
    
    # Check if already exists
    result = db.execute(
        text("SELECT row_id FROM tbl_cp_m2m_std_lng WHERE student_id = :student_id AND language_id = :language_id"),
        {"student_id": student_id, "language_id": language_id}
    )
    
    if result.fetchone():
        logger.debug(f"Student language already exists")
        return {"already_exists": True}
    
    # Insert new relationship
    db.execute(
        text("""INSERT INTO tbl_cp_m2m_std_lng (student_id, language_id)
                VALUES (:student_id, :language_id)"""),
        {"student_id": student_id, "language_id": language_id}
    )
    db.commit()
    logger.debug(f"Student language saved")
    
    return {"already_exists": False}


def save_student_interest(db: Session, student_id: int, interest_id: int):
    """
    Saves a student-interest many-to-many relationship to tbl_cp_m2m_std_interest.
    
    Parameters:
        db: Database session
        student_id: Student ID
        interest_id: Interest ID
        
    Returns:
        dict with already_exists flag
    """
    logger.debug(f"Saving student interest: student_id={student_id}, interest_id={interest_id}")
    
    # Check if already exists
    result = db.execute(
        text("SELECT row_id FROM tbl_cp_m2m_std_interest WHERE student_id = :student_id AND interest_id = :interest_id"),
        {"student_id": student_id, "interest_id": interest_id}
    )
    
    if result.fetchone():
        logger.debug(f"Student interest already exists")
        return {"already_exists": True}
    
    # Insert new relationship
    db.execute(
        text("""INSERT INTO tbl_cp_m2m_std_interest (student_id, interest_id)
                VALUES (:student_id, :interest_id)"""),
        {"student_id": student_id, "interest_id": interest_id}
    )
    db.commit()
    logger.debug(f"Student interest saved")
    
    return {"already_exists": False}


def save_student_certification(db: Session, data: dict):
    """
    Saves a student-certification many-to-many relationship to tbl_cp_m2m_student_certification.
    
    Parameters:
        db: Database session
        data: Dict with student_id, certification_id, and optional dates/urls
        
    Returns:
        dict with already_exists flag
    """
    logger.debug(f"Saving student certification: student_id={data.get('student_id')}, cert_id={data.get('certification_id')}")
    
    # Check if already exists
    result = db.execute(
        text("SELECT candidate_cert_id FROM tbl_cd_candidate_certifications WHERE candidate_id = :candidate_id AND certification_id = :certification_id"),
        {"candidate_id": data["student_id"], "certification_id": data["certification_id"]}
    )
    
    if result.fetchone():
        logger.debug(f"Student certification already exists")
        return {"already_exists": True}
    
    # Handle dates
    issue_date = safe_date(data.get("issue_date"), date(1900, 1, 1))
    expiry_date = safe_date(data.get("expiry_date"), date(9999, 12, 31))
    
    # Insert new relationship
    db.execute(
        text(
            """INSERT INTO tbl_cd_candidate_certifications 
                (candidate_id, certification_id, issue_date, expiry_date, credential_url, credential_id, is_expired)
                VALUES (:candidate_id, :certification_id, :issue_date, :expiry_date, :credential_url, :credential_id, :is_expired)"""
        ),
        {
            "candidate_id": data["student_id"],
            "certification_id": data["certification_id"],
            "issue_date": issue_date.strftime('%Y-%m-%d'),
            "expiry_date": expiry_date.strftime('%Y-%m-%d'),
            "credential_url": data.get("certificate_url") or '',
            "credential_id": data.get("credential_id") or '',
            "is_expired": False
        }
    )
    db.commit()
    logger.debug(f"Student certification saved")
    
    return {"already_exists": False}


def save_address(db: Session, data: SaveAddressRequest) -> SaveAddressResponse:
    """
    Saves an address record to tbl_cp_student_address.
    
    Parameters:
        db: Database session
        data: SaveAddressRequest with address details
        
    Returns:
        SaveAddressResponse with address_id
    """
    logger.debug(f"Saving address for student: {data.student_id}")
    
    # Insert into tbl_cd_student_address (MySQL)
    insert_sql = text(
        "INSERT INTO tbl_cd_student_address (candidate_id, address_line_1, address_line_2, care_of, landmark, pincode_id, latitude, longitude, address_type, address_expiry)"
        " VALUES (:candidate_id, :address_line_1, :address_line_2, :care_of, :landmark, :pincode_id, :latitude, :longitude, :address_type, :address_expiry)"
    )

    result = db.execute(
        insert_sql,
        {
            "candidate_id": data.student_id,
            "address_line_1": data.address_line_1,
            "address_line_2": data.address_line_2 or '',
            "care_of": data.care_of or '',
            "landmark": data.landmark or 'No Landmark',
            "pincode_id": data.pincode_id,
            "latitude": 0.0,
            "longitude": 0.0,
            "address_type": data.address_type or 'current',
            "address_expiry": '9999-12-31'
        }
    )
    new_id = result.lastrowid
    db.commit()
    logger.debug(f"Address saved: {new_id}")

    return SaveAddressResponse(address_id=new_id)
