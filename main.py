import os
import streamlit as st
from PyPDF2 import PdfReader
import re

# Function to clean text
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]+', '', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with one space
    return text.strip()

# Function to build DFA
def build_dfa(skills):
    dfa = {}
    for skill in skills:
        words = skill.strip().split()  # Handle multi-word skills
        state = dfa
        for word in words:
            for char in word:
                if char not in state:
                    state[char] = {}
                state = state[char]
        state['is_end'] = True  # Mark the end of a skill
    return dfa

# Function to check skills in resume text
def check_skill(dfa, resume_text):
    matches = []
    words = resume_text.split()  # Split the resume text into words
    for i in range(len(words)):
        state = dfa
        matched_skill = []
        for j in range(i, len(words)):
            word = words[j]
            for char in word:
                if char in state:
                    state = state[char]
                else:
                    state = None
                    break
            if state is None:
                break
            matched_skill.append(word)
            if 'is_end' in state:
                matches.append(' '.join(matched_skill))
                break  # Stop at the first match to avoid partial overlap
    return matches

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return clean_text(text)

# Streamlit App
st.title("Resume Skill Matcher")
st.markdown("Upload a resume and enter the required skills to see if they match.")

# Input Section
st.subheader("Enter Required Skills")
required_skills = st.text_area("Enter skills separated by commas (e.g., Python, Java, Machine Learning):").lower().split(',')
required_skills = [skill.strip() for skill in required_skills if skill.strip()]

# Display inputted skills
if required_skills:
    st.write("**Inputted Skills:**")
    st.write(required_skills)

# Upload Resume
st.subheader("Upload Resume")
uploaded_file = st.file_uploader("Upload a PDF resume (max 25MB)", type="pdf")

# Process Resume Button
if st.button("Match Skills"):
    if not required_skills or not uploaded_file:
        st.error("Please provide required skills and upload a resume.")
    else:
        if uploaded_file.size > 25 * 1024 * 1024:
            st.error(f"File {uploaded_file.name} exceeds the 25MB limit.")
        else:
            with st.spinner("Processing resume..."):
                resume_text = extract_text_from_pdf(uploaded_file).lower()
                dfa = build_dfa(required_skills)
                matched_skills = check_skill(dfa, resume_text)
                matched = [skill for skill in required_skills if any(skill in match for match in matched_skills)]
                missing = [skill for skill in required_skills if skill not in matched]

                # Display Results
                st.success("Processing complete!")
                st.subheader("Results")

                # Matched Skills
                st.write("**Matched Skills:**")
                if matched:
                    for skill in matched:
                        st.markdown(f"✅ {skill}")
                else:
                    st.write("No skills matched.")

                # Missing Skills
                st.write("**Missing Skills:**")
                if missing:
                    for skill in missing:
                        st.markdown(f"❌ {skill}")
                else:
                    st.write("All skills matched!")

                # Summary
                st.subheader("Summary")
                st.write(f"**{len(matched)} out of {len(required_skills)} skills matched.**")
                progress = len(matched) / len(required_skills)
                st.progress(progress)

# Footer
st.markdown("---")
st.markdown("**Instructions:** Make sure to enter all required skills separated by commas.")
st.markdown("**Contact:** support@resumematcher.com")