import asyncio
from database import engine
from sqlalchemy import text

async def list_all_tables():
    """List all tables currently in Azure SQL database"""
    query = """
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE='BASE TABLE' 
    ORDER BY TABLE_NAME
    """
    
    async with engine.connect() as conn:
        result = await conn.execute(text(query))
        tables = result.fetchall()
    
    print(f"\n{'='*60}")
    print(f"TABLES IN AZURE SQL DATABASE: campus5")
    print(f"{'='*60}\n")
    
    for i, (table_name,) in enumerate(tables, 1):
        print(f"{i:2d}. {table_name}")
    
    print(f"\n{'='*60}")
    print(f"TOTAL TABLES: {len(tables)}")
    print(f"{'='*60}\n")
    
    # List of tables that SHOULD exist
    required_tables = [
        'tbl_cd_msalutation', 'tbl_cd_mlanguages', 'tbl_cd_minterests', 
        'tbl_cd_mcourses', 'tbl_cd_mcolleges', 'tbl_cd_mcertifications', 
        'tbl_cd_mskills', 'tbl_cd_mmodule', 'tbl_cd_mdifficulty', 
        'tbl_cd_mround_result', 'tbl_cd_mattendance', 'tbl_cd_minterviewer',
        'tbl_cd_mcountries', 'tbl_cd_mstates', 'tbl_cd_mcities', 'tbl_cd_mpincodes',
        'tbl_cd_candidates', 'tbl_cd_student_school', 'tbl_cd_education',
        'tbl_cd_msemester', 'tbl_cd_msubjects', 'tbl_cd_college_sem_subject',
        'tbl_cd_student_subject_marks', 'tbl_cd_experience', 'tbl_cd_projects',
        'tbl_cd_m2m_std_skill', 'tbl_cd_m2m_std_lng', 'tbl_cd_m2m_std_interest',
        'tbl_cd_m2m_student_certification', 'tbl_cd_m2m_studentproject_skill',
        'tbl_cd_mquestions', 'tbl_cd_m2m_question_options',
        'tbl_cd_companies', 'tbl_cd_job_descriptions',
        'tbl_cd_student_address', 'tbl_cd_college_address', 'tbl_cd_company_address',
        'tbl_cd_jd_round_config', 'tbl_cd_m2m_jd_round_module',
        'tbl_cd_recruitment_drive',
        'tbl_cd_job_applications', 'tbl_cd_application_status_history',
        'tbl_cd_exam_session', 'tbl_cd_m2m_exam_question_response',
        'tbl_cd_interview_session', 'tbl_cd_m2m_session_module_score', 
        'tbl_cd_m2m_session_question_response'
        'tbl_cp_resume_hashes'  # This was auto-created
    ]
    
    existing_table_names = [t[0] for t in tables]
    
    print("\nMISSING TABLES:")
    print(f"{'='*60}")
    missing = []
    for table in required_tables:
        if table not in existing_table_names:
            missing.append(table)
            print(f"  ✗ {table}")
    
    if not missing:
        print("  ✓ ALL TABLES PRESENT!")
    
    print(f"\n  Total Missing: {len(missing)}/{len(required_tables)}")
    print(f"{'='*60}\n")
    
    return len(tables), len(missing)

if __name__ == "__main__":
    try:
        total, missing = asyncio.run(list_all_tables())
    except Exception as e:
        print(f"\nERROR: {e}")
        print(f"Make sure database.py is configured correctly")
