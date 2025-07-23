import streamlit as st
import json
import os
from resume_extraction import parse_resume

st.set_page_config(page_title="Bulk Resume Parser (Gemini)", layout="wide")
st.title("Bulk Resume Parser (Gemini)")
st.write("Upload multiple PDF resumes, parse them using Gemini, and download the results as JSON.")

uploaded_files = st.file_uploader(
    "Upload PDF resumes (multiple allowed)", type="pdf", accept_multiple_files=True
)

results = []
if uploaded_files:
    st.info(f"Processing {len(uploaded_files)} file(s)...")
    for file in uploaded_files:
        # Save to a temp file
        temp_path = os.path.join("/tmp", file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        result = parse_resume(temp_path)
        result['filename'] = file.name
        results.append(result)
        os.remove(temp_path)

    # Show analytics
    total = len(results)
    success = sum(1 for r in results if not r.get('error'))
    st.markdown(f"**Resumes Uploaded:** {total}  ")
    st.markdown(f"**Successfully Parsed:** {success}")

    # Show results table
    import pandas as pd
    table_data = [
        {
            "File Name": r.get('filename', ''),
            "Status": "Success" if not r.get('error') else "Failed",
            "JSON": json.dumps(r, indent=2) if not r.get('error') else r.get('error')
        }
        for r in results
    ]
    df = pd.DataFrame(table_data)
    st.dataframe(df[["File Name", "Status"]], use_container_width=True)

    # Expandable JSON preview for each file
    for r in results:
        with st.expander(f"{r.get('filename', 'Resume')} - {'Success' if not r.get('error') else 'Failed'}"):
            if r.get('error'):
                st.error(r['error'])
            else:
                st.json(r)

    # Download all as JSON
    st.download_button(
        label="Download All Results as JSON",
        data=json.dumps(results, indent=2),
        file_name="parsed_resumes.json",
        mime="application/json"
    )
else:
    st.info("Please upload one or more PDF resumes to begin.") 