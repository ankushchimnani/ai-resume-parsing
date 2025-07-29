import streamlit as st
import json
import os
from resume_extraction import parse_resume, get_validation_checklist

st.set_page_config(page_title="Bulk Resume Parser & Validator (Gemini)", layout="wide")
st.title("Bulk Resume Parser & Validator (Gemini)")
st.write("Upload multiple PDF resumes, parse them using Gemini, validate against checklist, and download the results as JSON.")

# Add a sidebar for validation checklist
with st.sidebar:
    st.header("Validation Checklist")
    if st.button("View Checklist"):
        checklist = get_validation_checklist()
        st.text_area("Resume Validation Checklist", checklist, height=400, disabled=True)

uploaded_files = st.file_uploader(
    "Upload PDF resumes (multiple allowed)", type="pdf", accept_multiple_files=True
)

results = []
if uploaded_files:
    st.info(f"Processing {len(uploaded_files)} file(s)...")
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, file in enumerate(uploaded_files):
        status_text.text(f"Processing {file.name}...")
        
        # Save to a temp file
        temp_path = os.path.join("/tmp", file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        
        result = parse_resume(temp_path)
        result['filename'] = file.name
        results.append(result)
        os.remove(temp_path)
        
        # Update progress
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    status_text.text("Processing complete!")
    progress_bar.empty()
    status_text.empty()

    # Show analytics
    total = len(results)
    success = sum(1 for r in results if not r.get('error'))
    validation_passed = sum(1 for r in results if not r.get('error') and r.get('validation', {}).get('passed', False))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Resumes Uploaded", total)
    with col2:
        st.metric("Successfully Parsed", success)
    with col3:
        st.metric("Validation Passed", validation_passed)

    # Show results table with validation scores
    import pandas as pd
    table_data = []
    for r in results:
        if r.get('error'):
            table_data.append({
                "File Name": r.get('filename', ''),
                "Status": "Failed",
                "Validation Score": "N/A",
                "Validation Passed": "N/A",
                "Critical Issues": "N/A"
            })
        else:
            validation = r.get('validation', {})
            score = validation.get('overall_score', 0)
            passed = validation.get('passed', False)
            critical_issues = len(validation.get('critical_issues', []))
            
            # Get validation status with emoji
            status = validation.get("status", "Unknown")
            status_emoji = {
                "Excellent": "🏆",
                "Good": "✅",
                "Needs Improvement": "⚠️",
                "Fail": "❌"
            }.get(status, "❓")
            
            table_data.append({
                "File Name": r.get('filename', ''),
                "Status": "Success",
                "Validation Score": f"{score:.1f}%",
                "Validation Status": f"{status_emoji} {status}",
                "Critical Issues": critical_issues
            })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)

    # Expandable detailed view for each file
    for r in results:
        filename = r.get('filename', 'Resume')
        has_error = bool(r.get('error'))
        status = "Failed" if has_error else "Success"
        
        with st.expander(f"{filename} - {status}"):
            if has_error:
                st.error(r['error'])
            else:
                # Create tabs for different views
                tab1, tab2, tab3, tab4 = st.tabs(["Parsed Data", "Validation Results", "Raw Text", "Raw JSON"])
                
                with tab1:
                    st.subheader("Parsed Resume Data")
                    parsed_data = r.get('parsed_data', {})
                    
                    # Display personal details
                    if 'personal_details' in parsed_data:
                        st.write("**Personal Details:**")
                        personal = parsed_data['personal_details']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Name:** {personal.get('name', 'N/A')}")
                            st.write(f"**Email:** {personal.get('email', 'N/A')}")
                        with col2:
                            st.write(f"**Phone:** {personal.get('phone', 'N/A')}")
                            st.write(f"**Location:** {personal.get('location', 'N/A')}")
                    
                    # Display professional presence
                    if 'professional_presence' in parsed_data:
                        st.write("**Professional Presence:**")
                        presence = parsed_data['professional_presence']
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            linkedin = presence.get('linkedin_url', 'N/A')
                            if linkedin != 'N/A':
                                st.write(f"**LinkedIn:** [{linkedin}]({linkedin})")
                            else:
                                st.write(f"**LinkedIn:** {linkedin}")
                        with col2:
                            github = presence.get('github_url', 'N/A')
                            if github != 'N/A':
                                st.write(f"**GitHub:** [{github}]({github})")
                            else:
                                st.write(f"**GitHub:** {github}")
                        with col3:
                            portfolio = presence.get('portfolio_url', 'N/A')
                            if portfolio != 'N/A':
                                st.write(f"**Portfolio:** [{portfolio}]({portfolio})")
                            else:
                                st.write(f"**Portfolio:** {portfolio}")
                    
                    # Display summary
                    if 'summary' in parsed_data:
                        st.write("**Summary:**")
                        st.write(parsed_data['summary'])
                    
                    # Display skills
                    if 'skills' in parsed_data:
                        st.write("**Skills:**")
                        skills = parsed_data['skills']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Technical Skills:**")
                            for skill in skills.get('technical', []):
                                st.write(f"• {skill}")
                        with col2:
                            st.write("**Soft Skills:**")
                            for skill in skills.get('soft', []):
                                st.write(f"• {skill}")
                
                with tab2:
                    st.subheader("Validation Results")
                    validation = r.get('validation', {})
                    
                    # Overall score
                    score = validation.get('overall_score', 0)
                    passed = validation.get('passed', False)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Overall Score", f"{score:.1f}%")
                    with col2:
                        # Get validation status with emoji
                        status = validation.get("status", "Unknown")
                        status_emoji = {
                            "Excellent": "🏆",
                            "Good": "✅",
                            "Needs Improvement": "⚠️",
                            "Fail": "❌"
                        }.get(status, "❓")
                        st.metric("Validation Status", f"{status_emoji} {status}")
                    
                    # Section scores
                    st.write("**Section Scores:**")
                    sections = validation.get('sections', {})
                    for section_name, section_data in sections.items():
                        section_score = section_data.get('score', 0)
                        weight = section_data.get('weight', 0)
                        issues = section_data.get('issues', [])
                        
                        # Create a progress bar for each section
                        st.write(f"**{section_name.replace('_', ' ').title()}** ({weight}% weight)")
                        st.progress(section_score / 100)
                        st.write(f"Score: {section_score:.1f}%")
                        
                        if issues:
                            st.write("**Issues:**")
                            for issue in issues:
                                st.write(f"• {issue}")
                        st.divider()
                    
                    # Critical issues
                    critical_issues = validation.get('critical_issues', [])
                    if critical_issues:
                        st.error("**Critical Issues:**")
                        for issue in critical_issues:
                            st.write(f"• {issue}")
                    
                    # Recommendations
                    recommendations = validation.get('recommendations', [])
                    if recommendations:
                        st.info("**Recommendations:**")
                        for rec in recommendations:
                            st.write(f"• {rec}")
                
                with tab3:
                    st.subheader("Raw Text Content")
                    raw_text = parsed_data.get('raw_text_content', 'No raw text content available')
                    st.text_area("Complete Resume Text", raw_text, height=400, disabled=True)
                    st.info("This is the complete text extracted from the resume. Use this to verify that no content was missed during parsing.")
                
                with tab4:
                    st.subheader("Raw JSON Data")
                    st.json(r)

    # Download all as JSON
    st.download_button(
        label="Download All Results as JSON",
        data=json.dumps(results, indent=2),
        file_name="parsed_and_validated_resumes.json",
        mime="application/json"
    )
else:
    st.info("Please upload one or more PDF resumes to begin.") 