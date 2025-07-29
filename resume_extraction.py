import google.generativeai as genai
import os
import json
import mimetypes
from dotenv import load_dotenv
from resume_validator import ResumeValidator

load_dotenv()

# --- Configuration ---
# IMPORTANT: Replace "YOUR_API_KEY" with your actual Google AI API key.
# You can get a key from https://aistudio.google.com/app/apikey
api_key = None

# Try to get API key from environment variables first (for local development)
api_key = os.environ.get("GEMINI_API_KEY")

# If not found in environment, try Streamlit secrets (for Streamlit Cloud)
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["GEMINI_API_KEY"]
    except (ImportError, AttributeError, KeyError):
        pass

# If still no API key, show error
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found! Please set it in your .env file for local development "
        "or in Streamlit secrets for cloud deployment."
    )

genai.configure(api_key=api_key)

# Initialize the resume validator
resume_validator = ResumeValidator()

def parse_resume(file_path: str) -> dict:
    """
    Uploads a PDF file, validates if it's a resume, parses it using the
    Gemini API, and returns the extracted details as a dictionary.

    Args:
        file_path: The local path to the PDF file.

    Returns:
        A dictionary containing the parsed resume data or an error message.
    """
    # --- 1. Input Validation ---
    if not os.path.exists(file_path):
        return {"error": f"File not found at path: {file_path}"}

    # Check if the file is a PDF based on its MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type != 'application/pdf':
        return {"error": "Invalid file type. Please upload a PDF document."}

    print(f"Processing '{file_path}'...")

    try:
        # --- 2. Upload File to Gemini ---
        print("Uploading file to Gemini...")
        resume_file = genai.upload_file(path=file_path, display_name="Resume PDF")
        print(f"File uploaded successfully: {resume_file.uri}")

        # --- 3. Content Validation (Is it a resume?) ---
        print("Validating document content...")
        validation_model = genai.GenerativeModel(model_name="gemini-2.5-pro")
        validation_prompt = [
            "You are an expert document analyzer.",
            "Analyze the content of the provided file and determine if it is a professional resume or CV.",
            "Respond with only 'yes' or 'no'.",
            resume_file
        ]
        validation_response = validation_model.generate_content(validation_prompt)

        if 'no' in validation_response.text.lower():
            # Clean up the uploaded file if it's not a resume
            genai.delete_file(resume_file.name)
            return {"error": "The uploaded document does not appear to be a resume."}

        print("Document validated as a resume.")

        # --- 4. Parse Resume Details ---
        print("Parsing resume details...")
        parsing_model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        parsing_prompt = [
            "You are a highly-skilled resume parser that strictly follows output formatting rules.",
            "Assume the current year is 2025.",
            "Your task is to analyze the provided resume and extract its information precisely into the JSON format defined below. Do not deviate from this schema.",
            "CRITICAL: Extract ALL information from the resume. Nothing should be missed or omitted.",
            """
The JSON output MUST conform to the following structure:
{
  "personal_details": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "location": "string"
  },
  "professional_presence": {
    "linkedin_url": "string",
    "github_url": "string",
    "portfolio_url": "string"
  },
  "summary": "string",
  "skills": {
    "technical": ["string", "string", ...],
    "soft": ["string", "string", ...]
  },
  "experience": [
    {
      "company": "string",
      "title": "string",
      "duration": "string",
      "location": "string"
    }
  ],
  "education": [
    {
      "degree_or_course": "string",
      "institution": "string",
      "duration": "string"
    }
  ],
  "projects": [
    {
      "name": "string",
      "description": "string",
      "features": ["string", "string", ...],
      "tech_stack": ["string", "string", ...]
    }
  ],
  "is_graduate": "boolean",
  "other_details": "string"
}
""",
            "URL EXTRACTION RULES:",
            "1. LinkedIn URLs: Look for:",
            "   - Full URLs: 'linkedin.com/in/username', 'https://linkedin.com/in/username'",
            "   - Profile identifiers: 'username' (if it looks like a LinkedIn profile ID)",
            "   - Any text that appears to be a LinkedIn profile identifier",
            "   - Construct full URL: https://linkedin.com/in/username",
            "2. GitHub URLs: Look for:",
            "   - Full URLs: 'github.com/username', 'https://github.com/username'",
            "   - Usernames that appear to be GitHub handles",
            "   - Construct full URL: https://github.com/username",
            "3. Portfolio URLs: Look for:",
            "   - Personal websites, portfolio links, deployed project URLs",
            "   - Any URLs that appear to be professional websites",
            "   - Extract the full URL including https://",
            "4. URL Construction: If only identifiers/usernames are found, construct the full URL with appropriate domain.",
            "5. LinkedIn Profile Detection: Look for LinkedIn profile identifiers in contact information, headers, or anywhere in the resume. Common patterns:",
            "   - Profile IDs like 'sanjana-kumari-050aa6314'",
            "   - Usernames that appear to be LinkedIn handles",
            "   - Any text that could be a LinkedIn profile identifier",
            "   - Always construct the full URL: https://linkedin.com/in/[profile-id]",
            "",
            "CONTENT EXTRACTION RULES:",
            "1. Extract ALL text content from the resume, including headers, footers, and any additional information",
            "2. If information doesn't fit into the structured fields, place it in 'other_details'",
            "3. Do not skip any sections, bullet points, or text",
            "4. Preserve all formatting and content exactly as it appears",
            "",
            "Rule for 'is_graduate': Carefully examine all entries in the 'education' section. If at least one entry is a completed undergraduate (e.g., Bachelor's, B.E.) or postgraduate (e.g., Master's, MBA) degree with a graduation end year of 2025 or earlier, then set this to 'true'. The flag should be true even if other degrees are still being pursued. Set it to 'false' only if no university degrees have been completed by the end of 2025.",
            "",
            "Rule for 'other_details': Place ANY text from the resume that does not fit into the structured fields above into this string. This includes:",
            "- Additional sections not covered by the schema",
            "- Awards, certifications, languages, hobbies, interests",
            "- Any text that appears in headers, footers, or margins",
            "- Additional contact information or social media links",
            "- Any other content that appears on the resume",
            "It is CRUCIAL that NO information is lost from the original resume.",
            "",
            "Final Instruction: Respond with ONLY the raw JSON object. Do not include any introductory text, explanations, or markdown formatting like ```json.",
            resume_file
        ]
        parsing_response = parsing_model.generate_content(parsing_prompt)

        # Clean up the response to ensure it's valid JSON
        cleaned_json_text = parsing_response.text.strip().replace("```json", "").replace("```", "")

        # --- 5. Parse and Validate Resume ---
        parsed_data = json.loads(cleaned_json_text)
        
        # --- 6. Validate against checklist ---
        print("Validating resume against checklist...")
        validation_results = resume_validator.validate_resume(parsed_data, resume_file.uri)
        
        # Add validation results to the response
        result = {
            "parsed_data": parsed_data,
            "validation": validation_results
        }
        
        # Clean up the file from the server after processing
        genai.delete_file(resume_file.name)
        print("Processing complete.")
        
        return result

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

def validate_resume_only(file_path: str) -> dict:
    """
    Validates a resume against the checklist without parsing it.
    This is useful when you already have parsed data and just want validation.
    
    Args:
        file_path: The local path to the PDF file.
        
    Returns:
        A dictionary containing only the validation results.
    """
    # First parse the resume
    parse_result = parse_resume(file_path)
    
    if "error" in parse_result:
        return parse_result
    
    # Return only the validation results
    return parse_result.get("validation", {})

def get_validation_checklist() -> str:
    """
    Returns the validation checklist document for reference.
    
    Returns:
        String containing the checklist document.
    """
    return resume_validator.get_checklist_document()


# --- Main Execution ---
if __name__ == "__main__":
    # To run this script, you need a PDF file.
    # We will create a dummy PDF for demonstration purposes.
    # In a real scenario, you would have the PDF file already.
    
    # NOTE: You need to install 'fpdf' to create the dummy PDF.
    # Run: pip install fpdf
    try:
        from fpdf import FPDF

        # Create a dummy valid resume PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="John Doe - Software Engineer", ln=True, align='C')
        pdf.multi_cell(0, 5, txt="Email: john.doe@email.com | Phone: 123-456-7890\n\nSummary: Experienced Software Engineer...\n\nSkills: Python, Java, SQL")
        valid_resume_path = "sample_resume.pdf"
        pdf.output(valid_resume_path)

        # Create a dummy non-resume PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Grocery List", ln=True, align='C')
        pdf.multi_cell(0, 10, txt="- Milk\n- Bread\n- Eggs")
        not_a_resume_path = "not_a_resume.pdf"
        pdf.output(not_a_resume_path)
        
        # Create a dummy non-PDF file
        invalid_file_path = "invalid_file.txt"
        with open(invalid_file_path, "w") as f:
            f.write("This is not a PDF.")

    except ImportError:
        print("\nFPDF library not found. Cannot create dummy PDF files.")
        print("Please install it using: pip install fpdf")
        print("Or provide a path to your own PDF resume file.\n")
        valid_resume_path = "iitrprai_2408137.pdf" # Using the uploaded file as a fallback
        not_a_resume_path = None
        invalid_file_path = None


    # --- Test Case 1: Valid Resume ---
    print("\n--- Testing with a VALID RESUME ---")
    if os.path.exists(valid_resume_path):
        resume_details = parse_resume(valid_resume_path)
        print(json.dumps(resume_details, indent=2))
    else:
        print(f"File not found: {valid_resume_path}. Skipping test.")


    # --- Test Case 2: Invalid File Type (Not a PDF) ---
    print("\n--- Testing with an INVALID FILE TYPE ---")
    if invalid_file_path and os.path.exists(invalid_file_path):
        invalid_file_details = parse_resume(invalid_file_path)
        print(json.dumps(invalid_file_details, indent=2))
    else:
        print("Dummy invalid file not created. Skipping test.")

    # --- Test Case 3: Valid PDF but Not a Resume ---
    print("\n--- Testing with a NON-RESUME PDF ---")
    if not_a_resume_path and os.path.exists(not_a_resume_path):
        not_resume_details = parse_resume(not_a_resume_path)
        print(json.dumps(not_resume_details, indent=2))
    else:
        print("Dummy non-resume PDF not created. Skipping test.")

