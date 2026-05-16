-- ============================================================================
-- NAUKRIDB - RESUME PARSING SYSTEM
-- Production-Ready Database Schema
-- Database: naukridb
-- Engine: InnoDB
-- Charset: utf8mb4
-- Collation: utf8mb4_unicode_ci
-- ============================================================================
-- DESIGN NOTES:
-- - All tables use tbl_cd_* naming convention (candidate database)
-- - Every table includes created_at and updated_at for audit trails
-- - Foreign keys use ON DELETE RESTRICT to preserve parsing history
-- - Parsed JSON stored in LONGTEXT for flexibility
-- - Resume versioning supported for multiple uploads
-- - Work status tracking (fresher/experienced)
-- - Grading system support for education records
-- ============================================================================

CREATE DATABASE IF NOT EXISTS naukridb;
USE naukridb;

SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================================
-- SECTION 1: MASTER/LOOKUP TABLES
-- ============================================================================

-- Skills Master - Reference table for all skills
CREATE TABLE IF NOT EXISTS tbl_cd_skills (
  skill_id INT AUTO_INCREMENT PRIMARY KEY,
  skill_name VARCHAR(200) NOT NULL UNIQUE,
  skill_category VARCHAR(100) DEFAULT 'General',
  description TEXT DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_skill_name (skill_name),
  KEY idx_skill_category (skill_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

-- Companies Master - Reference table for all companies
CREATE TABLE IF NOT EXISTS tbl_cd_companies (
  company_id INT AUTO_INCREMENT PRIMARY KEY,
  company_name VARCHAR(300) NOT NULL UNIQUE,
  industry VARCHAR(150) DEFAULT 'Not Specified',
  website VARCHAR(500) DEFAULT NULL,
  headquarters_location VARCHAR(200) DEFAULT NULL,
  company_size VARCHAR(50) DEFAULT NULL,
  founded_year INT DEFAULT NULL,
  description TEXT DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_company_name (company_name),
  KEY idx_industry (industry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

-- Job Titles Master - Reference table for job positions
CREATE TABLE IF NOT EXISTS tbl_cd_job_titles (
  job_title_id INT AUTO_INCREMENT PRIMARY KEY,
  job_title VARCHAR(200) NOT NULL UNIQUE,
  job_category VARCHAR(150) DEFAULT 'General',
  seniority_level ENUM('Entry Level', 'Mid Level', 'Senior', 'Lead', 'Manager', 'Director', 'Executive') DEFAULT 'Mid Level',
  description TEXT DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_job_title (job_title),
  KEY idx_job_category (job_category),
  KEY idx_seniority_level (seniority_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

-- Certifications Master - Reference table for certifications
CREATE TABLE IF NOT EXISTS tbl_cd_certifications (
  certification_id INT AUTO_INCREMENT PRIMARY KEY,
  certification_name VARCHAR(300) NOT NULL UNIQUE,
  issuing_organization VARCHAR(200) NOT NULL,
  certification_category VARCHAR(150) DEFAULT 'General',
  validity_months INT DEFAULT NULL,
  description TEXT DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_cert_name (certification_name),
  KEY idx_issuing_org (issuing_organization)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 2: CORE CANDIDATE TABLES
-- ============================================================================

-- Candidates - Main candidate profile table
CREATE TABLE IF NOT EXISTS tbl_cd_candidates (
  candidate_id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  phone VARCHAR(20) UNIQUE DEFAULT NULL,
  first_name VARCHAR(100) NOT NULL,
  middle_name VARCHAR(100) DEFAULT NULL,
  last_name VARCHAR(100) DEFAULT NULL,
  date_of_birth DATE DEFAULT NULL,
  gender ENUM('Male', 'Female', 'Other', 'Prefer Not to Say') DEFAULT 'Prefer Not to Say',
  work_status ENUM('experienced', 'fresher') NOT NULL DEFAULT 'fresher',
  total_experience_years DECIMAL(4, 2) DEFAULT 0.00,
  current_location VARCHAR(200) DEFAULT NULL,
  willing_to_relocate BOOLEAN DEFAULT FALSE,
  linkedin_url VARCHAR(500) DEFAULT NULL,
  github_url VARCHAR(500) DEFAULT NULL,
  portfolio_url VARCHAR(500) DEFAULT NULL,
  profile_summary TEXT DEFAULT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_email (email),
  KEY idx_phone (phone),
  KEY idx_work_status (work_status),
  KEY idx_candidate_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

-- Candidate Contacts - Contact information for candidates
CREATE TABLE IF NOT EXISTS tbl_cd_candidate_contacts (
  contact_id INT AUTO_INCREMENT PRIMARY KEY,
  candidate_id INT NOT NULL,
  contact_type ENUM('Email', 'Phone', 'LinkedIn', 'GitHub', 'Portfolio', 'Website', 'Other') NOT NULL,
  contact_value VARCHAR(500) NOT NULL,
  is_primary BOOLEAN DEFAULT FALSE,
  verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (candidate_id) REFERENCES tbl_cd_candidates(candidate_id) ON DELETE RESTRICT,
  UNIQUE KEY unique_contact (candidate_id, contact_type, contact_value),
  KEY idx_candidate_contact (candidate_id),
  KEY idx_contact_type (contact_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 3: RESUME UPLOAD & VERSIONING
-- ============================================================================

-- Resumes - Resume file uploads with versioning support
CREATE TABLE IF NOT EXISTS tbl_cd_resumes (
  resume_id INT AUTO_INCREMENT PRIMARY KEY,
  candidate_id INT NOT NULL,
  file_name VARCHAR(300) NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  file_size BIGINT DEFAULT 0,
  file_type VARCHAR(50) DEFAULT 'application/pdf',
  file_hash VARCHAR(255) DEFAULT NULL,
  resume_version INT DEFAULT 1,
  is_primary BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  source ENUM('Manual Upload', 'Job Portal', 'Email', 'ATS Integration', 'API') DEFAULT 'Manual Upload',
  upload_timestamp TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (candidate_id) REFERENCES tbl_cd_candidates(candidate_id) ON DELETE RESTRICT,
  KEY idx_candidate_resume (candidate_id),
  KEY idx_resume_version (resume_version),
  KEY idx_is_primary (is_primary),
  KEY idx_file_hash (file_hash),
  KEY idx_upload_timestamp (upload_timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 4: RESUME PARSING
-- ============================================================================

-- Resume Parsing Status - Track parsing progress and status
CREATE TABLE IF NOT EXISTS tbl_cd_resume_parsing_status (
  parsing_id INT AUTO_INCREMENT PRIMARY KEY,
  resume_id INT NOT NULL,
  parsing_status ENUM('Pending', 'Processing', 'Completed', 'Failed', 'Skipped') NOT NULL DEFAULT 'Pending',
  confidence_score DECIMAL(5, 4) DEFAULT 0.0000,
  parsing_timestamp TIMESTAMP NULL DEFAULT NULL,
  parsing_duration_ms INT DEFAULT NULL,
  error_message TEXT DEFAULT NULL,
  error_code VARCHAR(50) DEFAULT NULL,
  parser_version VARCHAR(50) DEFAULT '1.0',
  retry_count INT DEFAULT 0,
  last_retry_timestamp TIMESTAMP NULL DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (resume_id) REFERENCES tbl_cd_resumes(resume_id) ON DELETE RESTRICT,
  UNIQUE KEY unique_resume_parsing (resume_id),
  KEY idx_parsing_status (parsing_status),
  KEY idx_parsing_timestamp (parsing_timestamp),
  KEY idx_confidence_score (confidence_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

-- Parsed Resume JSON - Store complete parsed resume data
CREATE TABLE IF NOT EXISTS tbl_cd_parsed_resume_json (
  parsed_id INT AUTO_INCREMENT PRIMARY KEY,
  resume_id INT NOT NULL,
  parsed_json LONGTEXT NOT NULL,
  parsing_version VARCHAR(50) DEFAULT '1.0',
  extraction_metadata JSON DEFAULT NULL,
  raw_text LONGTEXT DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (resume_id) REFERENCES tbl_cd_resumes(resume_id) ON DELETE RESTRICT,
  UNIQUE KEY unique_parsed_resume (resume_id),
  KEY idx_resume_parsed (resume_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 5: CANDIDATE EDUCATION
-- ============================================================================

-- Education - Educational qualifications
CREATE TABLE IF NOT EXISTS tbl_cd_education (
  education_id INT AUTO_INCREMENT PRIMARY KEY,
  candidate_id INT NOT NULL,
  institution_name VARCHAR(300) NOT NULL,
  degree VARCHAR(100) NOT NULL,
  field_of_study VARCHAR(200) NOT NULL,
  start_date DATE DEFAULT NULL,
  end_date DATE DEFAULT NULL,
  is_pursuing BOOLEAN DEFAULT FALSE,
  grading_system ENUM(
    'Scale 10 Grading System',
    'Scale 4 Grading System',
    'Percentage Marks of 100 Maximum',
    'Course Requires Pass'
  ) DEFAULT 'Scale 10 Grading System',
  score_obtained DECIMAL(5, 2) DEFAULT NULL,
  maximum_score DECIMAL(5, 2) DEFAULT NULL,
  grade_letter VARCHAR(5) DEFAULT NULL,
  location VARCHAR(200) DEFAULT NULL,
  description TEXT DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (candidate_id) REFERENCES tbl_cd_candidates(candidate_id) ON DELETE RESTRICT,
  KEY idx_candidate_education (candidate_id),
  KEY idx_degree (degree),
  KEY idx_field_of_study (field_of_study)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 6: CANDIDATE EXPERIENCE
-- ============================================================================

-- Experience - Work experience records
CREATE TABLE IF NOT EXISTS tbl_cd_experience (
  experience_id INT AUTO_INCREMENT PRIMARY KEY,
  candidate_id INT NOT NULL,
  company_id INT DEFAULT NULL,
  company_name VARCHAR(300) NOT NULL,
  job_title_id INT DEFAULT NULL,
  job_title VARCHAR(200) NOT NULL,
  employment_type ENUM('Full-Time', 'Part-Time', 'Contract', 'Temporary', 'Freelance', 'Internship') DEFAULT 'Full-Time',
  location VARCHAR(200) DEFAULT NULL,
  start_date DATE NOT NULL,
  end_date DATE DEFAULT NULL,
  is_current BOOLEAN DEFAULT FALSE,
  work_description TEXT DEFAULT NULL,
  achievements TEXT DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (candidate_id) REFERENCES tbl_cd_candidates(candidate_id) ON DELETE RESTRICT,
  FOREIGN KEY (company_id) REFERENCES tbl_cd_companies(company_id) ON DELETE RESTRICT,
  FOREIGN KEY (job_title_id) REFERENCES tbl_cd_job_titles(job_title_id) ON DELETE RESTRICT,
  KEY idx_candidate_experience (candidate_id),
  KEY idx_company_experience (company_id),
  KEY idx_job_title_exp (job_title_id),
  KEY idx_is_current (is_current)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 7: CANDIDATE SKILLS (M2M)
-- ============================================================================

-- Candidate Skills - Many-to-many relationship between candidates and skills
CREATE TABLE IF NOT EXISTS tbl_cd_candidate_skills (
  candidate_skill_id INT AUTO_INCREMENT PRIMARY KEY,
  candidate_id INT NOT NULL,
  skill_id INT NOT NULL,
  proficiency_level ENUM('Beginner', 'Intermediate', 'Advanced', 'Expert') DEFAULT 'Intermediate',
  years_of_experience DECIMAL(4, 2) DEFAULT NULL,
  extracted_from_section VARCHAR(100) DEFAULT NULL,
  confidence_score DECIMAL(5, 4) DEFAULT 0.5000,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (candidate_id) REFERENCES tbl_cd_candidates(candidate_id) ON DELETE RESTRICT,
  FOREIGN KEY (skill_id) REFERENCES tbl_cd_skills(skill_id) ON DELETE RESTRICT,
  UNIQUE KEY unique_candidate_skill (candidate_id, skill_id),
  KEY idx_candidate_skills (candidate_id),
  KEY idx_skill (skill_id),
  KEY idx_proficiency_level (proficiency_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 8: CANDIDATE CERTIFICATIONS (M2M)
-- ============================================================================

-- Candidate Certifications - Many-to-many relationship between candidates and certifications
CREATE TABLE IF NOT EXISTS tbl_cd_candidate_certifications (
  candidate_cert_id INT AUTO_INCREMENT PRIMARY KEY,
  candidate_id INT NOT NULL,
  certification_id INT NOT NULL,
  issue_date DATE DEFAULT NULL,
  expiry_date DATE DEFAULT NULL,
  credential_id VARCHAR(150) DEFAULT NULL,
  credential_url VARCHAR(500) DEFAULT NULL,
  is_expired BOOLEAN DEFAULT FALSE,
  confidence_score DECIMAL(5, 4) DEFAULT 0.5000,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (candidate_id) REFERENCES tbl_cd_candidates(candidate_id) ON DELETE RESTRICT,
  FOREIGN KEY (certification_id) REFERENCES tbl_cd_certifications(certification_id) ON DELETE RESTRICT,
  UNIQUE KEY unique_candidate_cert (candidate_id, certification_id),
  KEY idx_candidate_certifications (candidate_id),
  KEY idx_certification (certification_id),
  KEY idx_expiry_date (expiry_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 9: CANDIDATE PROJECTS
-- ============================================================================

-- Projects - Portfolio projects and professional achievements
CREATE TABLE IF NOT EXISTS tbl_cd_projects (
  project_id INT AUTO_INCREMENT PRIMARY KEY,
  candidate_id INT NOT NULL,
  project_title VARCHAR(300) NOT NULL,
  project_description TEXT DEFAULT NULL,
  project_url VARCHAR(500) DEFAULT NULL,
  start_date DATE DEFAULT NULL,
  end_date DATE DEFAULT NULL,
  is_current BOOLEAN DEFAULT FALSE,
  technologies_used TEXT DEFAULT NULL,
  achievements TEXT DEFAULT NULL,
  team_size INT DEFAULT NULL,
  role VARCHAR(150) DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (candidate_id) REFERENCES tbl_cd_candidates(candidate_id) ON DELETE RESTRICT,
  KEY idx_candidate_projects (candidate_id),
  KEY idx_project_title (project_title)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 10: JOB DESCRIPTIONS
-- ============================================================================

-- Job Descriptions - Job postings and descriptions
CREATE TABLE IF NOT EXISTS tbl_cd_job_descriptions (
  job_id INT AUTO_INCREMENT PRIMARY KEY,
  company_id INT NOT NULL,
  job_title_id INT NOT NULL,
  job_title VARCHAR(200) NOT NULL,
  job_description TEXT NOT NULL,
  required_skills TEXT DEFAULT NULL,
  preferred_skills TEXT DEFAULT NULL,
  experience_required DECIMAL(4, 2) DEFAULT 0.00,
  experience_required_max DECIMAL(4, 2) DEFAULT NULL,
  salary_range_min DECIMAL(15, 2) DEFAULT NULL,
  salary_range_max DECIMAL(15, 2) DEFAULT NULL,
  salary_currency VARCHAR(10) DEFAULT 'USD',
  location VARCHAR(200) DEFAULT NULL,
  employment_type ENUM('Full-Time', 'Part-Time', 'Contract', 'Temporary', 'Freelance', 'Internship') DEFAULT 'Full-Time',
  job_status ENUM('Open', 'Closed', 'On Hold', 'Filled') DEFAULT 'Open',
  posted_date TIMESTAMP NOT NULL,
  closing_date DATE DEFAULT NULL,
  application_url VARCHAR(500) DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (company_id) REFERENCES tbl_cd_companies(company_id) ON DELETE RESTRICT,
  FOREIGN KEY (job_title_id) REFERENCES tbl_cd_job_titles(job_title_id) ON DELETE RESTRICT,
  KEY idx_company_jobs (company_id),
  KEY idx_job_title_desc (job_title_id),
  KEY idx_job_status (job_status),
  KEY idx_posted_date (posted_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 11: JOB APPLICATIONS
-- ============================================================================

-- Job Applications - Candidate applications to job postings
CREATE TABLE IF NOT EXISTS tbl_cd_job_applications (
  application_id INT AUTO_INCREMENT PRIMARY KEY,
  candidate_id INT NOT NULL,
  job_id INT NOT NULL,
  application_date TIMESTAMP NOT NULL,
  application_status ENUM('Applied', 'Shortlisted', 'Rejected', 'Interview Scheduled', 'Offered', 'Accepted', 'Declined') DEFAULT 'Applied',
  resume_used_id INT DEFAULT NULL,
  cover_letter TEXT DEFAULT NULL,
  application_notes TEXT DEFAULT NULL,
  last_status_update TIMESTAMP NULL DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (candidate_id) REFERENCES tbl_cd_candidates(candidate_id) ON DELETE RESTRICT,
  FOREIGN KEY (job_id) REFERENCES tbl_cd_job_descriptions(job_id) ON DELETE RESTRICT,
  FOREIGN KEY (resume_used_id) REFERENCES tbl_cd_resumes(resume_id) ON DELETE RESTRICT,
  UNIQUE KEY unique_job_application (candidate_id, job_id),
  KEY idx_candidate_applications (candidate_id),
  KEY idx_job_applications (job_id),
  KEY idx_application_status (application_status),
  KEY idx_application_date (application_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SECTION 12: INDEXES FOR PERFORMANCE
-- ============================================================================

-- Candidate Indexes (already defined above)
-- Resume Indexes
CREATE INDEX idx_resume_created ON tbl_cd_resumes(created_at);
CREATE INDEX idx_resume_is_active ON tbl_cd_resumes(is_active);

-- Parsing Status Indexes
CREATE INDEX idx_parsing_failed ON tbl_cd_resume_parsing_status(parsing_status) WHERE parsing_status = 'Failed';
CREATE INDEX idx_parsing_updated ON tbl_cd_resume_parsing_status(updated_at);

-- Education Indexes
CREATE INDEX idx_education_updated ON tbl_cd_education(updated_at);

-- Experience Indexes
CREATE INDEX idx_experience_updated ON tbl_cd_experience(updated_at);

-- Skills Indexes
CREATE INDEX idx_candidate_skills_confidence ON tbl_cd_candidate_skills(confidence_score);
CREATE INDEX idx_candidate_skills_updated ON tbl_cd_candidate_skills(updated_at);

-- Certifications Indexes
CREATE INDEX idx_certifications_expired ON tbl_cd_candidate_certifications(is_expired);

-- Projects Indexes
CREATE INDEX idx_projects_updated ON tbl_cd_projects(updated_at);

-- Job Applications Indexes
CREATE INDEX idx_application_updated ON tbl_cd_job_applications(updated_at);
CREATE INDEX idx_application_company ON tbl_cd_job_applications(candidate_id, application_status);

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- SCHEMA SUMMARY
-- ============================================================================
-- Total Tables: 18
--
-- MASTER/LOOKUP TABLES (4):
--   - tbl_cd_skills
--   - tbl_cd_companies
--   - tbl_cd_job_titles
--   - tbl_cd_certifications
--
-- CORE CANDIDATE TABLES (2):
--   - tbl_cd_candidates
--   - tbl_cd_candidate_contacts
--
-- RESUME MANAGEMENT (3):
--   - tbl_cd_resumes
--   - tbl_cd_resume_parsing_status
--   - tbl_cd_parsed_resume_json
--
-- CANDIDATE DETAILS (4):
--   - tbl_cd_education
--   - tbl_cd_experience
--   - tbl_cd_candidate_skills
--   - tbl_cd_candidate_certifications
--   - tbl_cd_projects (1 additional)
--
-- JOB MANAGEMENT (2):
--   - tbl_cd_job_descriptions
--   - tbl_cd_job_applications
--
-- KEY FEATURES:
--   ✓ Work Status Tracking (fresher/experienced)
--   ✓ Education Grading System Support (4 options)
--   ✓ Score Tracking (score_obtained, maximum_score)
--   ✓ Resume Versioning & Tracking
--   ✓ Parsing Status with Confidence Scores
--   ✓ Parsed JSON Storage (LONGTEXT)
--   ✓ M2M Relationships for Skills & Certifications
--   ✓ Comprehensive Audit Trail (created_at, updated_at)
--   ✓ Production-Ready Indexes
--   ✓ ON DELETE RESTRICT for Data Preservation
--   ✓ MySQL 8 & Azure MySQL Compatible
--   ✓ InnoDB Engine with Proper Constraints
--
-- ============================================================================
