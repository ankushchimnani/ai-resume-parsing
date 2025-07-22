# Resume Gemini Extractor

A tool to parse multiple PDF resumes using Google Gemini API, with a web UI for bulk upload and JSON download.

## Features
- Upload and parse multiple PDF resumes at once
- Download all parsed results as a single JSON file
- Modern, responsive web UI

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
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your Gemini API key:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Get your key from: https://aistudio.google.com/app/apikey

4. **Run the backend API:**
   ```bash
   python backend_api.py
   ```
   - The backend will run on `http://localhost:5000`

5. **Open the frontend:**
   - Open `frontend.html` in your browser.
   - Make sure the backend is running.

## Usage
- Select multiple PDF resumes in the UI.
- Click "Upload & Parse Resumes".
- View results for each file.
- Download all results as a single JSON file.

## Project Structure
- `resume_extraction.py` — Resume parsing logic
- `backend_api.py` — Flask backend for bulk upload
- `frontend.html` — Web UI
- `requirements.txt` — Python dependencies
- `.env.example` — Sample environment file

## License
MIT 