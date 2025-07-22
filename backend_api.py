from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import json
from resume_extraction import parse_resume

app = Flask(__name__)
CORS(app)

@app.route('/upload-resumes', methods=['POST'])
def upload_resumes():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400
    files = request.files.getlist('files')
    results = []
    for file in files:
        if file.filename == '':
            results.append({'error': 'Empty filename'})
            continue
        # Save to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        # Parse resume
        result = parse_resume(tmp_path)
        result['filename'] = file.filename
        results.append(result)
        os.remove(tmp_path)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True) 