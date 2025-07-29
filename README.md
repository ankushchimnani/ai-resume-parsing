# Resume Gemini Extractor & Validator

A comprehensive tool to parse and validate multiple PDF resumes using Google Gemini API, with a modern web UI for bulk upload, validation against a predefined checklist, and JSON download.

## Features
- **Bulk Resume Processing**: Upload and parse multiple PDF resumes at once
- **Professional URL Extraction**: Automatically detect and extract LinkedIn, GitHub, and portfolio URLs
- **Complete Content Preservation**: Ensure no resume content is lost with raw text backup
- **Resume Validation**: Automatic validation against a comprehensive checklist
- **Detailed Analytics**: View parsing success rates and validation scores
- **Section-by-Section Analysis**: Detailed breakdown of resume quality by section
- **Recommendations**: Get specific recommendations for improving resumes
- **Modern UI**: Clean, responsive Streamlit interface with progress tracking and clickable URLs
- **JSON Export**: Download all parsed and validated results as a single JSON file

## 📋 Resume Validation Checklist

The system validates resumes against a comprehensive checklist for modern professional standards:

### **Mandatory Sections**
- **Contact Information**: Active mobile, professional email, location, LinkedIn URL
- **Professional Summary**: Concise summary (2-4 lines), third-person perspective, tailored to role
- **Education**: Reverse chronological order, degree type, institution, graduation date
- **Technical Skills**: Organized categories, correct capitalization, specific technologies
- **Core Competencies**: 4-6 workplace-relevant skills, mix of technical and interpersonal
- **Formatting**: Professional appearance, ATS-friendly, error-free content

### **Recommended Sections**
- **Projects**: 2-4 relevant projects, tech stack, live demos, quantifiable results
- **Professional Experience**: Reverse chronological, action verbs, quantifiable achievements
- **Certifications**: Current, relevant certifications with verification links

### **Quality Standards**
- **ATS-Friendly**: No graphics, tables, or unusual formatting
- **Professional Language**: No first-person language, industry-standard terminology
- **Error-Free**: Proper spelling, grammar, and consistent formatting

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/resume_gemini_extractor.git
   cd resume_gemini_extractor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Get your key from: https://aistudio.google.com/app/apikey

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
   - The app will open in your browser at `http://localhost:8501`

## Usage

### Web Interface (Recommended)
1. Open the Streamlit app in your browser
2. Upload multiple PDF resumes using the file uploader
3. View real-time processing progress
4. Review parsing results and validation scores
5. Check detailed validation breakdown by section
6. Download results as JSON

### Command Line Testing
```bash
# Test the validation service with sample data
python test_validation.py

# Parse a single resume file
python resume_extraction.py
```

## 📊 Validation Scoring

The system provides a comprehensive scoring system with modern professional standards:

### **Overall Score Categories**
- **🏆 Excellent**: 85%+ overall score
- **✅ Good**: 70-84% overall score  
- **⚠️ Needs Improvement**: 50-69% overall score
- **❌ Fail**: Below 50% overall score

### **Section Weights**
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

### **Validation Features**
- **Section Scores**: Individual scores for each resume section with progress bars
- **Critical Issues**: Must-fix problems that prevent validation
- **Recommendations**: Specific suggestions for improvement
- **Role-Specific Adjustments**: Different weights for technical vs non-technical roles

## Project Structure
- `app.py` — Main Streamlit application
- `resume_extraction.py` — Resume parsing and validation integration
- `resume_validator.py` — Resume validation service with checklist
- `test_validation.py` — Test script for validation service
- `requirements.txt` — Python dependencies
- `backend_api.py` — Legacy Flask backend (optional)
- `frontend.html` — Legacy HTML frontend (optional)

## Environment Variables

Create a `.env` file in your project root with the following content:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your actual Gemini API key from Google.

## API Usage

### For Streamlit Cloud Deployment
Add your API key to Streamlit Secrets:
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

## Customizing the Validation Checklist

The validation checklist is hardcoded in `resume_validator.py`. To customize:

1. Edit the `checklist_document` in the `ResumeValidator` class
2. Modify section weights in `section_weights`
3. Update mandatory vs recommended items in `mandatory_items` and `recommended_items`
4. Adjust validation logic in individual `_validate_*` methods

## Cost Estimation

Use the included cost estimation script to calculate API usage costs:
```bash
python estimate_gemini_cost.py
```

## License
MIT 