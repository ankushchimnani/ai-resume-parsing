#!/usr/bin/env python3
"""
Test script for the Resume Validation Service
This script demonstrates how to use the validation service with sample data.
"""

import json
from resume_validator import ResumeValidator
from resume_extraction import parse_resume, validate_resume_only, get_validation_checklist

def test_validation_with_sample_data():
    """Test the validation service with sample parsed resume data."""
    
    print("=== Resume Validation Service Test ===\n")
    
    # Initialize the validator
    validator = ResumeValidator()
    
    # Sample parsed resume data (this would normally come from parse_resume function)
    sample_resume = {
        "personal_details": {
            "name": "John Doe",
            "email": "john.doe@company.com",
            "phone": "123-456-7890",
            "location": "New York, NY"
        },
        "professional_presence": {
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "github_url": "https://github.com/johndoe",
            "portfolio_url": "https://johndoe.dev"
        },
        "summary": "Experienced software engineer with 5+ years of experience in Python, JavaScript, and cloud technologies. Passionate about building scalable applications and leading technical teams.",
        "skills": {
            "technical": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker"],
            "soft": ["Leadership", "Communication", "Problem Solving", "Team Collaboration"]
        },
        "experience": [
            {
                "company": "Tech Corp",
                "title": "Senior Software Engineer",
                "duration": "2022-2025",
                "location": "San Francisco, CA"
            },
            {
                "company": "Startup Inc",
                "title": "Software Engineer",
                "duration": "2020-2022",
                "location": "Austin, TX"
            }
        ],
        "education": [
            {
                "degree_or_course": "Bachelor of Science in Computer Science",
                "institution": "University of Technology",
                "duration": "2016-2020"
            }
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Built a full-stack e-commerce platform using React and Node.js",
                "features": ["User authentication", "Payment processing", "Inventory management"],
                "tech_stack": ["React", "Node.js", "MongoDB", "Stripe"]
            }
        ],
        "is_graduate": True,
        "other_details": "Certified AWS Solutions Architect"
    }
    
    print("Testing validation with sample resume data...")
    
    # Validate the sample resume
    validation_results = validator.validate_resume(sample_resume)
    
    print(f"\n=== Validation Results ===")
    print(f"Overall Score: {validation_results['overall_score']}%")
    print(f"Passed Validation: {'Yes' if validation_results['passed'] else 'No'}")
    
    print(f"\n=== Section Scores ===")
    for section_name, section_data in validation_results['sections'].items():
        score = section_data['score']
        weight = section_data['weight']
        print(f"{section_name.replace('_', ' ').title()}: {score:.1f}% (Weight: {weight}%)")
    
    print(f"\n=== Critical Issues ===")
    for issue in validation_results['critical_issues']:
        print(f"❌ {issue}")
    
    print(f"\n=== Recommendations ===")
    for rec in validation_results['recommendations']:
        print(f"💡 {rec}")
    
    return validation_results

def test_validation_with_incomplete_data():
    """Test validation with incomplete resume data to see how it handles missing information."""
    
    print("\n\n=== Testing with Incomplete Resume Data ===\n")
    
    validator = ResumeValidator()
    
    # Incomplete resume data
    incomplete_resume = {
        "personal_details": {
            "name": "Jane Smith",
            "email": "jane@gmail.com",  # Personal email
            "phone": "",  # Missing phone
            "location": "Boston, MA"
        },
        "professional_presence": {
            "linkedin_url": "",
            "github_url": "",
            "portfolio_url": ""
        },
        "summary": "Software developer",  # Too short
        "skills": {
            "technical": ["Python"],
            "soft": []
        },
        "experience": [
            {
                "company": "Company A",
                "title": "Developer",
                "duration": "2023-2024",
                "location": ""
            }
        ],
        "education": [
            {
                "degree_or_course": "Computer Science",
                "institution": "University",
                "duration": "2020-2024"
            }
        ],
        "projects": [],
        "is_graduate": True,
        "other_details": ""
    }
    
    validation_results = validator.validate_resume(incomplete_resume)
    
    print(f"Overall Score: {validation_results['overall_score']}%")
    print(f"Passed Validation: {'Yes' if validation_results['passed'] else 'No'}")
    
    print(f"\n=== Issues Found ===")
    for section_name, section_data in validation_results['sections'].items():
        issues = section_data['issues']
        if issues:
            print(f"\n{section_name.replace('_', ' ').title()}:")
            for issue in issues:
                print(f"  • {issue}")
    
    return validation_results

def show_checklist():
    """Display the validation checklist."""
    
    print("\n\n=== Resume Validation Checklist ===\n")
    checklist = get_validation_checklist()
    print(checklist)

def main():
    """Main test function."""
    
    try:
        # Test with complete sample data
        test_validation_with_sample_data()
        
        # Test with incomplete data
        test_validation_with_incomplete_data()
        
        # Show the checklist
        show_checklist()
        
        print("\n\n=== Test Complete ===")
        print("The validation service is working correctly!")
        
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 