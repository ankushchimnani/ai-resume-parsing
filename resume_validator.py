import google.generativeai as genai
import json
from typing import Dict, List, Tuple

class ResumeValidator:
    """
    A service to validate resumes against a predefined checklist of requirements.
    """
    
    def __init__(self):
        # Hardcoded checklist document - this can be customized based on your requirements
        self.checklist_document = """
        # 📋 **RESUME VALIDATION CHECKLIST**

        This document defines the mandatory requirements that every resume must meet to be considered valid for modern professional standards.

        ## 📞 **SECTION 1: CONTACT INFORMATION** *(MANDATORY)*
        - [ ] Active mobile number (professional voicemail preferred)
        - [ ] Professional email address (avoid nicknames, numbers, or informal handles)
        - [ ] Current location (City, State/Country format)
        - [ ] LinkedIn profile URL (active and optimized)
        - [ ] GitHub profile URL (required for technical roles, optional for others)
        - [ ] Portfolio/personal website (recommended for creative/technical roles)
        - [ ] All links must be functional and up-to-date

        ## 💼 **SECTION 2: PROFESSIONAL SUMMARY** *(MANDATORY)*
        - [ ] Concise summary (2-4 lines, 50-80 words)
        - [ ] Opens with relevant professional title or career focus
        - [ ] Highlights 2-3 key strengths or core competencies
        - [ ] Quantifies experience level when applicable
        - [ ] Uses third-person perspective (avoid "I", "me", "my")
        - [ ] Tailored to target role/industry
        - [ ] Free of clichés and generic phrases ("hard worker," "team player")

        ## 🎓 **SECTION 3: EDUCATION** *(MANDATORY)*
        - [ ] Listed in reverse chronological order (most recent first)
        - [ ] Includes highest level of education completed
        - [ ] Specifies degree type, major/field of study
        - [ ] Institution name and location
        - [ ] Graduation date (MM/YYYY format) or expected graduation
        - [ ] GPA included if 3.5+ and recent graduate
        - [ ] Relevant coursework, honors, or certifications if space permits

        ## 💻 **SECTION 4: TECHNICAL SKILLS** *(MANDATORY FOR TECHNICAL ROLES)*
        - [ ] Organized into logical categories (Languages, Frameworks, Tools, etc.)
        - [ ] Uses correct capitalization and spelling (JavaScript, React, HTML5, CSS3)
        - [ ] Lists specific technologies rather than broad terms
        - [ ] Prioritizes skills relevant to target positions
        - [ ] Includes proficiency levels where appropriate
        - [ ] Avoids obsolete or rarely-used technologies unless relevant
        - [ ] Updated to reflect current industry standards

        ## 🤝 **SECTION 5: CORE COMPETENCIES** *(MANDATORY)*
        - [ ] 4-6 workplace-relevant skills listed
        - [ ] Includes mix of technical and interpersonal skills
        - [ ] Examples: Problem-solving, Project Management, Data Analysis, Communication
        - [ ] Avoids basic traits (punctuality, honesty) in favor of developed skills
        - [ ] Aligns with job requirements and industry expectations
        - [ ] Uses industry-standard terminology

        ## 🚀 **SECTION 6: PROJECTS** *(RECOMMENDED FOR TECHNICAL ROLES)*
        - [ ] 2-4 most relevant projects included
        - [ ] Mix of individual and collaborative work
        - [ ] Clear, professional project titles (avoid "clone" terminology)
        - [ ] 2-3 bullet points per project describing impact and functionality
        - [ ] Technology stack clearly specified
        - [ ] Live demo and/or GitHub repository links provided
        - [ ] Quantifiable results or metrics when available
        - [ ] Uses action verbs and technical language appropriately

        ## 💼 **SECTION 7: PROFESSIONAL EXPERIENCE** *(IF APPLICABLE)*
        - [ ] Listed in reverse chronological order
        - [ ] Includes job title, company name, location, and dates (MM/YYYY format)
        - [ ] 3-5 bullet points per role highlighting achievements
        - [ ] Starts with strong action verbs
        - [ ] Quantifies accomplishments with metrics and numbers
        - [ ] Demonstrates career progression and increasing responsibility
        - [ ] Relevant internships, freelance, or contract work included
        - [ ] Explains employment gaps if longer than 3 months

        ## 🏆 **SECTION 8: CERTIFICATIONS & ACHIEVEMENTS** *(IF APPLICABLE)*
        - [ ] Only current, relevant certifications included
        - [ ] Certification name, issuing organization, and date
        - [ ] Digital badges or verification links when available
        - [ ] Professional licenses if required for role
        - [ ] Relevant awards, publications, or speaking engagements
        - [ ] Expiration dates noted for time-sensitive certifications

        ## 📄 **SECTION 9: FORMATTING & PRESENTATION** *(MANDATORY)*
        - [ ] 1-2 pages maximum (1 page preferred for entry-level, 2 pages for experienced)
        - [ ] Consistent, professional formatting throughout
        - [ ] Readable font (Arial, Calibri, or similar) in 10-12pt size
        - [ ] Appropriate use of white space and margins
        - [ ] Consistent bullet styles and indentation
        - [ ] Error-free spelling, grammar, and punctuation
        - [ ] Exported as PDF with professional filename (FirstName_LastName_Resume.pdf)
        - [ ] ATS-friendly format (no graphics, tables, or unusual formatting)
        - [ ] Print-friendly in black and white

        ## ❌ **CRITICAL ERRORS TO AVOID**
        - [ ] Incorrect technical terminology capitalization
        - [ ] Inconsistent date formats
        - [ ] Personal information (age, marital status, photo)
        - [ ] Unprofessional email addresses
        - [ ] Lengthy paragraphs instead of bullet points
        - [ ] Irrelevant or outdated information
        - [ ] First-person language in descriptions
        - [ ] Unverifiable claims or exaggerations
        - [ ] Poor file naming or non-PDF formats
        - [ ] Contact information in headers/footers (ATS issues)

        ---

        ## 📊 **SCORING METHODOLOGY**

        ### **Section Weights:**
        | Section | Weight | Critical for |
        |---------|--------|--------------|
        | Contact Information | 15% | All roles |
        | Professional Summary | 15% | All roles |
        | Education | 15% | Entry-level, Academic |
        | Technical Skills | 20% | Technical roles |
        | Core Competencies | 10% | All roles |
        | Projects | 15% | Technical, Creative |
        | Professional Experience | 20% | Experienced candidates |
        | Certifications | 5% | Specialized roles |
        | Formatting | 10% | All roles |

        ### **Pass/Fail Criteria:**
        - **Excellent**: 85%+ overall score
        - **Good**: 70-84% overall score  
        - **Needs Improvement**: 50-69% overall score
        - **Fail**: Below 50% overall score

        ### **Role-Specific Adjustments:**
        - **Technical Roles**: Projects and Technical Skills weighted higher
        - **Entry-Level**: Education and Projects emphasized over experience
        - **Senior-Level**: Professional Experience and Leadership competencies prioritized
        - **Creative Roles**: Portfolio and relevant projects emphasized

        ---

        ## ✅ **VALIDATION NOTES**
        1. All MANDATORY sections must be present and substantially complete
        2. Minimum 70% completion rate required for each mandatory section
        3. Industry-specific requirements may override general guidelines
        4. Resume should tell a cohesive professional story
        5. Content must be truthful and verifiable
        6. Regular updates recommended to reflect current skills and experience
        """
        
        # Define scoring weights for different sections
        self.section_weights = {
            "contact_information": 15,
            "professional_summary": 15,
            "education": 15,
            "technical_skills": 20,
            "core_competencies": 10,
            "projects": 15,
            "professional_experience": 20,
            "certifications": 5,
            "formatting": 10
        }
        
        # Define mandatory vs recommended items
        self.mandatory_items = {
            "contact_information": ["mobile", "email", "location", "linkedin"],
            "professional_summary": ["summary_present", "summary_length", "impersonal_language", "strong_start"],
            "education": ["education_present", "reverse_chronological", "degree_names", "institutions", "durations"],
            "technical_skills": ["skills_present", "correct_capitalization", "no_generic_terms", "organized"],
            "core_competencies": ["skills_present", "workplace_relevant", "not_traits", "mix_technical_interpersonal"],
            "projects": ["projects_present", "max_4_projects", "individual_collaborative", "action_words"],
            "professional_experience": ["experience_present", "role_company_location", "action_verbs", "quantifiable"],
            "certifications": ["relevant_certifications", "links_provided"],
            "formatting": ["structure_complete", "professional_content", "ats_friendly"]
        }
        
        self.recommended_items = {
            "contact_information": ["github", "portfolio"],
            "professional_summary": ["target_role", "key_strengths"],
            "education": ["higher_education_only", "gpa_if_high"],
            "technical_skills": ["specific_technologies", "proficiency_levels"],
            "core_competencies": ["4_6_skills", "industry_terminology"],
            "projects": ["tech_stack", "deployment_links", "no_clone_word", "metrics"],
            "professional_experience": ["duration_format", "career_progression"],
            "certifications": ["current_certifications", "professional_licenses"],
            "formatting": ["consistent_style", "error_free", "appropriate_length"]
        }

    def validate_resume(self, parsed_resume: Dict, resume_file_uri: str = None) -> Dict:
        """
        Validates a parsed resume against the checklist.
        
        Args:
            parsed_resume: The parsed resume data from parse_resume function
            resume_file_uri: Optional file URI for additional validation
            
        Returns:
            Dictionary containing validation results, scores, and recommendations
        """
        try:
            # Initialize validation results
            validation_results = {
                "overall_score": 0,
                "passed": False,
                "sections": {},
                "missing_items": [],
                "recommendations": [],
                "critical_issues": [],
                "detailed_analysis": {}
            }
            
            # Validate each section
            section_scores = {}
            
            # 1. Contact Information Validation
            contact_score, contact_issues = self._validate_contact_information(parsed_resume)
            section_scores["contact_information"] = contact_score
            validation_results["sections"]["contact_information"] = {
                "score": contact_score,
                "issues": contact_issues,
                "weight": self.section_weights["contact_information"]
            }
            
            # 2. Professional Summary Validation
            summary_score, summary_issues = self._validate_professional_summary(parsed_resume)
            section_scores["professional_summary"] = summary_score
            validation_results["sections"]["professional_summary"] = {
                "score": summary_score,
                "issues": summary_issues,
                "weight": self.section_weights["professional_summary"]
            }
            
            # 3. Education Validation
            education_score, education_issues = self._validate_education(parsed_resume)
            section_scores["education"] = education_score
            validation_results["sections"]["education"] = {
                "score": education_score,
                "issues": education_issues,
                "weight": self.section_weights["education"]
            }
            
            # 4. Technical Skills Validation
            tech_skills_score, tech_skills_issues = self._validate_technical_skills(parsed_resume)
            section_scores["technical_skills"] = tech_skills_score
            validation_results["sections"]["technical_skills"] = {
                "score": tech_skills_score,
                "issues": tech_skills_issues,
                "weight": self.section_weights["technical_skills"]
            }
            
            # 5. Core Competencies Validation
            core_comp_score, core_comp_issues = self._validate_core_competencies(parsed_resume)
            section_scores["core_competencies"] = core_comp_score
            validation_results["sections"]["core_competencies"] = {
                "score": core_comp_score,
                "issues": core_comp_issues,
                "weight": self.section_weights["core_competencies"]
            }
            
            # 6. Projects Validation
            projects_score, projects_issues = self._validate_projects(parsed_resume)
            section_scores["projects"] = projects_score
            validation_results["sections"]["projects"] = {
                "score": projects_score,
                "issues": projects_issues,
                "weight": self.section_weights["projects"]
            }
            
            # 7. Professional Experience Validation
            experience_score, experience_issues = self._validate_professional_experience(parsed_resume)
            section_scores["professional_experience"] = experience_score
            validation_results["sections"]["professional_experience"] = {
                "score": experience_score,
                "issues": experience_issues,
                "weight": self.section_weights["professional_experience"]
            }
            
            # 8. Certifications Validation
            cert_score, cert_issues = self._validate_certifications(parsed_resume)
            section_scores["certifications"] = cert_score
            validation_results["sections"]["certifications"] = {
                "score": cert_score,
                "issues": cert_issues,
                "weight": self.section_weights["certifications"]
            }
            
            # 9. Formatting Validation
            formatting_score, formatting_issues = self._validate_formatting(parsed_resume, resume_file_uri)
            section_scores["formatting"] = formatting_score
            validation_results["sections"]["formatting"] = {
                "score": formatting_score,
                "issues": formatting_issues,
                "weight": self.section_weights["formatting"]
            }
            
            # Calculate overall score
            total_score = 0
            total_weight = 0
            
            for section, score in section_scores.items():
                weight = self.section_weights.get(section, 0)
                # score is already a percentage (0-100), so we don't multiply by 100 again
                total_score += score * weight
                total_weight += weight
            
            if total_weight > 0:
                overall_score = total_score / total_weight
            else:
                overall_score = 0
                
            validation_results["overall_score"] = round(overall_score, 2)
            
            # Determine if resume passed validation with new scoring system
            if overall_score >= 85:
                status = "Excellent"
            elif overall_score >= 70:
                status = "Good"
            elif overall_score >= 50:
                status = "Needs Improvement"
            else:
                status = "Fail"
            
            validation_results["status"] = status
            validation_results["passed"] = overall_score >= 50  # Pass if 50% or higher
            
            # Generate recommendations
            validation_results["recommendations"] = self._generate_recommendations(validation_results)
            
            # Identify critical issues
            validation_results["critical_issues"] = self._identify_critical_issues(validation_results)
            
            return validation_results
            
        except Exception as e:
            return {
                "error": f"Validation failed: {str(e)}",
                "overall_score": 0,
                "passed": False
            }

    def _validate_contact_information(self, parsed_resume: Dict) -> Tuple[float, List[str]]:
        """Validate contact information section."""
        issues = []
        score = 0
        total_items = 6
        
        personal = parsed_resume.get("personal_details", {})
        presence = parsed_resume.get("professional_presence", {})
        
        # Check mobile number
        if personal.get("phone") and len(personal["phone"].strip()) > 0:
            score += 1
        else:
            issues.append("Mobile number is missing")
            
        # Check email
        email = personal.get("email", "")
        if email and "@" in email:
            # Check if it's a professional email
            if any(domain in email.lower() for domain in ["gmail.com", "yahoo.com", "hotmail.com"]):
                issues.append("Consider using a professional email address instead of personal email")
            score += 1
        else:
            issues.append("Professional email address is missing")
            
        # Check location (City, State format)
        location = personal.get("location", "")
        if location and len(location.strip()) > 0:
            if "," in location:  # Should have City, State format
                score += 1
            else:
                issues.append("Location should be in City, State format")
        else:
            issues.append("Location is missing")
            
        # Check LinkedIn URL
        if presence.get("linkedin_url") and len(presence["linkedin_url"].strip()) > 0:
            score += 1
        else:
            issues.append("LinkedIn URL is missing")
            
        # Check GitHub Link (recommended for technical roles)
        if presence.get("github_url") and len(presence["github_url"].strip()) > 0:
            score += 1
        else:
            issues.append("GitHub link is missing (recommended for technical roles)")
            
        # Check Portfolio Link (optional)
        if presence.get("portfolio_url") and len(presence["portfolio_url"].strip()) > 0:
            score += 1
        else:
            issues.append("Portfolio link is missing (optional but recommended)")
            
        return (score / total_items) * 100, issues



    def _validate_professional_summary(self, parsed_resume: Dict) -> Tuple[float, List[str]]:
        """Validate professional summary section."""
        issues = []
        score = 0
        total_items = 6
        
        summary = parsed_resume.get("summary", "")
        
        # Check if summary exists
        if summary and len(summary.strip()) > 0:
            score += 1
        else:
            issues.append("Professional summary is missing")
            return 0, issues
            
        # Check if summary is 3-4 lines maximum
        lines = summary.split('\n')
        line_count = len([line for line in lines if line.strip()])
        if 3 <= line_count <= 4:
            score += 1
        else:
            issues.append("Summary should be 3-4 lines maximum")
            
        # Check if summary starts with strong, relevant adjective
        strong_adjectives = ["detail-oriented", "experienced", "skilled", "passionate", "dedicated", "results-driven", "innovative", "creative"]
        summary_lower = summary.lower()
        if any(adj in summary_lower for adj in strong_adjectives):
            score += 1
        else:
            issues.append("Summary should start with a strong, relevant adjective")
            
        # Check if summary includes target role
        role_indicators = ["developer", "engineer", "analyst", "manager", "specialist", "consultant", "designer"]
        if any(role in summary_lower for role in role_indicators):
            score += 1
        else:
            issues.append("Summary should include target role")
            
        # Check if summary mentions key strengths
        strength_indicators = ["skills", "strengths", "expertise", "proficient", "experienced in"]
        if any(strength in summary_lower for strength in strength_indicators):
            score += 1
        else:
            issues.append("Summary should mention key strengths")
            
        # Check if summary avoids "I", "me", "my" (impersonal language)
        personal_pronouns = ["i ", " me ", " my ", "i'm", "i've", "i'll"]
        if not any(pronoun in summary_lower for pronoun in personal_pronouns):
            score += 1
        else:
            issues.append("Summary should avoid 'I', 'me', 'my' (use impersonal language)")
            
        return (score / total_items) * 100, issues

    def _validate_technical_skills(self, parsed_resume: Dict) -> Tuple[float, List[str]]:
        """Validate technical skills section."""
        issues = []
        score = 0
        total_items = 4
        
        skills = parsed_resume.get("skills", {})
        technical = skills.get("technical", [])
        
        # Check if technical skills are present
        if technical and len(technical) > 0:
            score += 1
        else:
            issues.append("Technical skills are missing")
            return 0, issues
            
        # Check correct capitalization
        correct_tech_terms = ["HTML", "CSS", "JavaScript", "React", "Node.js", "Express.js", "MongoDB", "Git", "GitHub", "MySQL", "Python", "Java", "C++", "TypeScript", "Angular", "Vue.js", "Docker", "AWS", "Azure", "Linux", "REST", "API", "JSON", "XML", "SQL", "NoSQL", "Redis", "PostgreSQL", "Firebase", "Heroku", "Vercel", "Netlify"]
        incorrect_terms = []
        for skill in technical:
            if skill.lower() in [term.lower() for term in correct_tech_terms]:
                if skill not in correct_tech_terms:
                    incorrect_terms.append(skill)
        
        if not incorrect_terms:
            score += 1
        else:
            issues.append(f"Incorrect capitalization: {', '.join(incorrect_terms)}")
            
        # Check for generic terms like "Full Stack"
        generic_terms = ["full stack", "fullstack", "web development", "software development", "programming"]
        has_generic = any(term in ' '.join(technical).lower() for term in generic_terms)
        if not has_generic:
            score += 1
        else:
            issues.append("Avoid generic terms like 'Full Stack' - break down into specific skills")
            
        # Check if skills are organized
        if len(technical) >= 3:  # At least 3 technical skills
            score += 1
        else:
            issues.append("Include at least 3 relevant technical skills")
            
        return (score / total_items) * 100, issues

    def _validate_core_competencies(self, parsed_resume: Dict) -> Tuple[float, List[str]]:
        """Validate core competencies section."""
        issues = []
        score = 0
        total_items = 6
        
        skills = parsed_resume.get("skills", {})
        soft = skills.get("soft", [])
        
        # Check if core competencies are present
        if soft and len(soft) > 0:
            score += 1
        else:
            issues.append("Core competencies are missing")
            return 0, issues
            
        # Check for 4-6 workplace-relevant skills
        workplace_skills = ["problem-solving", "project management", "data analysis", "communication", "leadership", "teamwork", "collaboration", "critical thinking", "creativity", "organization", "planning", "negotiation", "presentation", "mentoring", "strategic thinking", "analytical skills", "decision making", "time management", "adaptability", "innovation"]
        trait_words = ["honesty", "punctuality", "loyalty", "dedication", "hardworking", "responsible", "reliable", "trustworthy"]
        
        relevant_skills = []
        trait_issues = []
        for skill in soft:
            skill_lower = skill.lower()
            if skill_lower in workplace_skills:
                relevant_skills.append(skill)
            elif skill_lower in trait_words:
                trait_issues.append(skill)
        
        # Check for 4-6 skills
        if 4 <= len(relevant_skills) <= 6:
            score += 1
        else:
            issues.append("Include 4-6 workplace-relevant core competencies")
            
        # Check for mix of technical and interpersonal skills
        technical_indicators = ["data analysis", "problem-solving", "analytical skills", "technical skills", "programming", "coding"]
        interpersonal_indicators = ["communication", "leadership", "teamwork", "collaboration", "presentation", "mentoring"]
        
        has_technical = any(indicator in ' '.join(relevant_skills).lower() for indicator in technical_indicators)
        has_interpersonal = any(indicator in ' '.join(relevant_skills).lower() for indicator in interpersonal_indicators)
        
        if has_technical and has_interpersonal:
            score += 1
        else:
            issues.append("Include mix of technical and interpersonal skills")
            
        # Check for industry-standard terminology
        industry_terms = ["project management", "data analysis", "communication", "leadership", "problem-solving", "strategic thinking", "analytical skills"]
        has_industry_terms = any(term in ' '.join(relevant_skills).lower() for term in industry_terms)
        if has_industry_terms:
            score += 1
        else:
            issues.append("Use industry-standard terminology")
            
        # Check for alignment with job requirements
        if len(relevant_skills) >= 3:
            score += 1
        else:
            issues.append("Align competencies with job requirements")
            
        # Check for avoiding traits
        if trait_issues:
            issues.append(f"Avoid basic traits like: {', '.join(trait_issues)} - these are traits, not skills")
        else:
            score += 1
            
        return (score / total_items) * 100, issues

    def _validate_professional_experience(self, parsed_resume: Dict) -> Tuple[float, List[str]]:
        """Validate professional experience section."""
        issues = []
        score = 0
        total_items = 8
        
        experience = parsed_resume.get("experience", [])
        
        # Check if experience section exists (any type of experience)
        if experience and len(experience) > 0:
            score += 1
        else:
            issues.append("Professional experience section is missing (include any type of experience)")
            return 0, issues
            
        # Check reverse chronological order
        if len(experience) >= 2:
            # Basic check - assume first entry is most recent
            score += 1
        else:
            score += 1  # Single entry is fine
            
        # Validate each experience entry
        for i, exp in enumerate(experience):
            # Check job title, company name, location, and dates
            has_title = exp.get("title") and len(exp["title"].strip()) > 0
            has_company = exp.get("company") and len(exp["company"].strip()) > 0
            has_location = exp.get("location") and len(exp["location"].strip()) > 0
            has_duration = exp.get("duration") and len(exp["duration"].strip()) > 0
            
            if has_title and has_company and has_location and has_duration:
                score += 0.5
            else:
                missing = []
                if not has_title:
                    missing.append("job title")
                if not has_company:
                    missing.append("company name")
                if not has_location:
                    missing.append("location")
                if not has_duration:
                    missing.append("dates")
                issues.append(f"Experience {i+1} missing: {', '.join(missing)}")
                
        # Check for 3-5 bullet points per role
        for i, exp in enumerate(experience):
            description = exp.get("description", "")
            if description:
                bullet_points = description.split('\n')
                bullet_count = len([bp for bp in bullet_points if bp.strip() and (bp.strip().startswith('-') or bp.strip().startswith('•'))])
                if 3 <= bullet_count <= 5:
                    score += 0.5
                else:
                    issues.append(f"Experience {i+1} should have 3-5 bullet points highlighting achievements")
                    
        # Check for strong action verbs
        action_verbs = ["developed", "implemented", "managed", "led", "created", "designed", "built", "improved", "increased", "decreased", "optimized", "coordinated", "analyzed", "resolved", "handled", "maintained", "established", "launched", "delivered", "achieved"]
        has_action_verbs = False
        for exp in experience:
            description = exp.get("description", "").lower()
            if any(verb in description for verb in action_verbs):
                has_action_verbs = True
                break
        
        if has_action_verbs:
            score += 1
        else:
            issues.append("Start bullet points with strong action verbs")
            
        # Check for quantifiable accomplishments
        quantifiable_indicators = ["%", "percent", "increase", "decrease", "improved", "reduced", "handled", "managed", "led", "team of", "users", "customers", "revenue", "sales", "efficiency", "growth", "savings", "reduction", "improvement"]
        has_quantifiable = False
        for exp in experience:
            description = exp.get("description", "").lower()
            if any(indicator in description for indicator in quantifiable_indicators):
                has_quantifiable = True
                break
        
        if has_quantifiable:
            score += 1
        else:
            issues.append("Quantify accomplishments with metrics and numbers")
            
        # Check for career progression
        if len(experience) >= 2:
            score += 1
        else:
            issues.append("Demonstrate career progression and increasing responsibility")
            
        # Cap the score at total_items
        score = min(score, total_items)
        
        return (score / total_items) * 100, issues

    def _validate_education(self, parsed_resume: Dict) -> Tuple[float, List[str]]:
        """Validate education section."""
        issues = []
        score = 0
        total_items = 4
        
        education = parsed_resume.get("education", [])
        
        # Check if education section exists
        if education and len(education) > 0:
            score += 1
        else:
            issues.append("Education section is missing")
            return 0, issues
            
        # Validate each education entry
        for i, edu in enumerate(education):
            # Check degree name
            if edu.get("degree_or_course") and len(edu["degree_or_course"].strip()) > 0:
                score += 0.5
            else:
                issues.append(f"Degree/course name missing in education {i+1}")
                
            # Check institution
            if edu.get("institution") and len(edu["institution"].strip()) > 0:
                score += 0.5
            else:
                issues.append(f"Institution name missing in education {i+1}")
                
            # Check duration
            if edu.get("duration") and len(edu["duration"].strip()) > 0:
                score += 0.5
            else:
                issues.append(f"Duration missing in education {i+1}")
                
        # Cap the score at total_items
        score = min(score, total_items)
        
        return (score / total_items) * 100, issues

    def _validate_projects(self, parsed_resume: Dict) -> Tuple[float, List[str]]:
        """Validate projects section."""
        issues = []
        score = 0
        total_items = 8
        
        projects = parsed_resume.get("projects", [])
        
        # Check if projects section exists
        if projects and len(projects) > 0:
            score += 1
        else:
            issues.append("Projects section is missing (recommended for technical roles)")
            return 0, issues
            
        # Check maximum 3 projects
        if len(projects) <= 3:
            score += 1
        else:
            issues.append("Maximum 3 projects should be included")
            
        # Check for solo project
        has_solo = False
        for proj in projects:
            description = proj.get("description", "").lower()
            if any(word in description for word in ["solo", "individual", "personal", "built by me"]):
                has_solo = True
                break
        if has_solo:
            score += 1
        else:
            issues.append("Include at least 1 solo project")
            
        # Check for team project
        has_team = False
        for proj in projects:
            description = proj.get("description", "").lower()
            if any(word in description for word in ["team", "collaborative", "group", "we", "our"]):
                has_team = True
                break
        if has_team:
            score += 1
        else:
            issues.append("Include at least 1 collaborative/team project (if available)")
            
        # Validate each project entry
        for i, proj in enumerate(projects):
            # Check project name (avoid "clone" word)
            name = proj.get("name", "")
            if name and len(name.strip()) > 0:
                if "clone" not in name.lower():
                    score += 0.5
                else:
                    issues.append(f"Project {i+1} title contains 'clone' - use more descriptive title")
            else:
                issues.append(f"Project name missing in project {i+1}")
                
            # Check description with action words
            description = proj.get("description", "")
            if description and len(description.strip()) > 0:
                action_words = ["built", "designed", "developed", "created", "implemented", "integrated", "deployed", "constructed", "architected", "engineered"]
                if any(word in description.lower() for word in action_words):
                    score += 0.5
                else:
                    issues.append(f"Project {i+1} description should start with action words")
            else:
                issues.append(f"Project description missing in project {i+1}")
                
            # Check tech stack
            tech_stack = proj.get("tech_stack", [])
            if tech_stack and len(tech_stack) > 0:
                score += 0.5
            else:
                issues.append(f"Technology stack missing in project {i+1}")
                
        # Cap the score at total_items
        score = min(score, total_items)
        
        return (score / total_items) * 100, issues

    def _validate_certifications(self, parsed_resume: Dict) -> Tuple[float, List[str]]:
        """Validate certifications section."""
        issues = []
        score = 0
        total_items = 6
        
        # Check if certifications exist in other_details or as a separate field
        other_details = parsed_resume.get("other_details", "")
        certifications = []
        
        # Look for certification patterns in other_details
        cert_indicators = ["certification", "certificate", "certified", "freecodecamp", "coursera", "udemy", "edx", "linkedin learning", "aws", "azure", "google", "microsoft"]
        if any(indicator in other_details.lower() for indicator in cert_indicators):
            certifications.append("Found in other details")
            
        # Check if certifications are present
        if certifications:
            score += 1
        else:
            issues.append("No relevant certifications found (optional but recommended)")
            return 0, issues
            
        # Check if certifications are current and relevant
        relevant_cert_indicators = ["javascript", "python", "react", "node", "aws", "azure", "docker", "kubernetes", "data structures", "algorithms", "web development", "software engineering", "cloud", "devops", "machine learning", "data science"]
        has_relevant = any(indicator in other_details.lower() for indicator in relevant_cert_indicators)
        if has_relevant:
            score += 1
        else:
            issues.append("Include only current, relevant certifications")
            
        # Check if certification details are provided
        detail_indicators = ["certified", "certification", "certificate"]
        has_details = any(indicator in other_details.lower() for indicator in detail_indicators)
        if has_details:
            score += 1
        else:
            issues.append("Specify certification name and issuing organization")
            
        # Check if links are provided (basic check)
        link_indicators = ["http", "www", ".com", ".org", ".edu", "linkedin.com", "github.com"]
        has_links = any(indicator in other_details.lower() for indicator in link_indicators)
        if has_links:
            score += 1
        else:
            issues.append("Provide digital badges or verification links")
            
        # Check for professional licenses if applicable
        license_indicators = ["license", "licensed", "professional license"]
        has_licenses = any(indicator in other_details.lower() for indicator in license_indicators)
        if has_licenses:
            score += 1
        else:
            issues.append("Include professional licenses if required for role")
            
        # Check for awards or achievements
        achievement_indicators = ["award", "achievement", "honor", "recognition", "publication", "speaking"]
        has_achievements = any(indicator in other_details.lower() for indicator in achievement_indicators)
        if has_achievements:
            score += 1
        else:
            issues.append("Include relevant awards, publications, or speaking engagements")
            
        return (score / total_items) * 100, issues

    def _validate_formatting(self, parsed_resume: Dict, resume_file_uri: str = None) -> Tuple[float, List[str]]:
        """Validate formatting and presentation."""
        issues = []
        score = 0
        total_items = 9
        
        # Check if data is well-structured (basic formatting check)
        if all(key in parsed_resume for key in ["personal_details", "skills", "experience", "education"]):
            score += 1
        else:
            issues.append("Resume structure is incomplete")
            
        # Check if personal details are complete
        personal = parsed_resume.get("personal_details", {})
        if all(key in personal for key in ["name", "email", "phone", "location"]):
            score += 1
        else:
            issues.append("Personal details section is incomplete")
            
        # Check if skills are organized
        skills = parsed_resume.get("skills", {})
        if "technical" in skills and "soft" in skills:
            score += 1
        else:
            issues.append("Skills should be organized by category")
            
        # Check if experience entries have required fields
        experience = parsed_resume.get("experience", [])
        if experience:
            valid_entries = 0
            for exp in experience:
                if all(key in exp for key in ["company", "title", "duration"]):
                    valid_entries += 1
            if valid_entries == len(experience):
                score += 1
            else:
                issues.append("Some experience entries are missing required information")
        else:
            issues.append("No work experience found")
            
        # Check for consistent formatting (basic check)
        if len(parsed_resume) >= 5:  # Has multiple sections
            score += 1
        else:
            issues.append("Resume should have consistent, professional formatting")
            
        # Check for professional content
        professional_indicators = ["experience", "skills", "education", "projects"]
        has_professional_content = any(indicator in str(parsed_resume).lower() for indicator in professional_indicators)
        if has_professional_content:
            score += 1
        else:
            issues.append("Resume should contain professional content")
            
        # Check for appropriate length (basic check)
        total_content = len(str(parsed_resume))
        if 500 <= total_content <= 5000:  # Reasonable content length
            score += 1
        else:
            issues.append("Resume should be 1-2 pages maximum")
            
        # Check for error-free content (basic check)
        error_indicators = ["error", "missing", "incomplete", "n/a", "none"]
        has_errors = any(indicator in str(parsed_resume).lower() for indicator in error_indicators)
        if not has_errors:
            score += 1
        else:
            issues.append("Resume should be error-free with proper spelling and grammar")
            
        # Check for ATS-friendly format (basic check)
        ats_friendly = True
        if "graphics" in str(parsed_resume).lower() or "images" in str(parsed_resume).lower():
            ats_friendly = False
        if ats_friendly:
            score += 1
        else:
            issues.append("Use ATS-friendly format (no graphics, tables, or unusual formatting)")
            
        return (score / total_items) * 100, issues

    def _generate_recommendations(self, validation_results: Dict) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        sections = validation_results.get("sections", {})
        
        # Contact information recommendations
        if sections.get("contact_information", {}).get("score", 0) < 100:
            recommendations.append("Complete contact information: mobile, professional email, location, LinkedIn, GitHub, and portfolio")
            
        # Professional summary recommendations
        if sections.get("professional_summary", {}).get("score", 0) < 100:
            recommendations.append("Write a 3-4 line professional summary starting with a strong adjective and avoiding 'I', 'me', 'my'")
            
        # Education recommendations
        if sections.get("education", {}).get("score", 0) < 100:
            recommendations.append("Complete education section with degree, institution, and duration in MM/YYYY format")
            
        # Technical skills recommendations
        if sections.get("technical_skills", {}).get("score", 0) < 100:
            recommendations.append("Include relevant technical skills with correct capitalization and avoid generic terms")
            
        # Soft skills recommendations
        if sections.get("soft_skills", {}).get("score", 0) < 100:
            recommendations.append("Include 3-4 workplace-relevant soft skills, not traits like 'honesty' or 'punctuality'")
            
        # Projects recommendations
        if sections.get("projects", {}).get("score", 0) < 100:
            recommendations.append("Include maximum 3 projects with solo and team projects, action words, and tech stack")
            
        # Work experience recommendations
        if sections.get("work_experience", {}).get("score", 0) < 100:
            recommendations.append("Include any type of experience with role, company, location, duration, and quantifiable achievements")
            
        # Certifications recommendations
        if sections.get("certifications", {}).get("score", 0) < 100:
            recommendations.append("Include relevant certifications with links to certificates")
            
        return recommendations

    def _identify_critical_issues(self, validation_results: Dict) -> List[str]:
        """Identify critical issues that must be fixed."""
        critical_issues = []
        
        sections = validation_results.get("sections", {})
        
        # Check for missing mandatory sections
        mandatory_sections = ["contact_information", "professional_summary", "education", "technical_skills", "soft_skills"]
        for section in mandatory_sections:
            if section not in sections or sections[section].get("score", 0) < 50:
                critical_issues.append(f"Critical: {section.replace('_', ' ').title()} section is missing or incomplete")
                
        # Check overall score
        if validation_results.get("overall_score", 0) < 50:
            critical_issues.append("Critical: Resume needs significant improvements to meet minimum standards")
            
        return critical_issues

    def get_checklist_document(self) -> str:
        """Return the checklist document for reference."""
        return self.checklist_document 