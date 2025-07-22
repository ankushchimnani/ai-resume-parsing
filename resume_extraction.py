import google.generativeai as genai
import os
import json
import mimetypes
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# IMPORTANT: Replace "YOUR_API_KEY" with your actual Google AI API key.
# You can get a key from https://aistudio.google.com/app/apikey
try:
    # It's recommended to set your API key as an environment variable
    # for better security.
    api_key = os.environ["GEMINI_API_KEY"]
except KeyError:
    print("------------------------------------------------------------------")
    print("ERROR: API key not found.")
    print("Please set the 'GEMINI_API_KEY' environment variable.")
    print("You can get a key from https://aistudio.google.com/app/apikey")
    print("------------------------------------------------------------------")
    api_key = "YOUR_API_KEY" # Fallback for demonstration

genai.configure(api_key=api_key)

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
        validation_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
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
        parsing_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        parsing_prompt = [
            "You are an expert resume parser.",
            "Extract the following details from the resume provided: Name, Email, Phone, Location, LinkedIn URL, GitHub URL, Portfolio URL, Professional Summary, Technical Skills, Soft Skills, all Professional Experience (including Company, Title, Duration, and Location), all Education (including Degree/Course, Institution, and Duration), and all Projects (including Name, Description, Features, and Tech Stack).",
            "Return the information as a clean, parsable JSON object. Do not include any text or markdown formatting before or after the JSON.",
            resume_file
        ]
        parsing_response = parsing_model.generate_content(parsing_prompt)

        # Clean up the response to ensure it's valid JSON
        cleaned_json_text = parsing_response.text.strip().replace("```json", "").replace("```", "")

        # --- 5. Return Parsed Data ---
        parsed_data = json.loads(cleaned_json_text)
        
        # Clean up the file from the server after processing
        genai.delete_file(resume_file.name)
        print("Processing complete.")
        
        return parsed_data

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


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

