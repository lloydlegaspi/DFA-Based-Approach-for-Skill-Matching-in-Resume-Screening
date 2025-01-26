import os
import streamlit as st
from PyPDF2 import PdfReader
import re

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]+', '', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with one space
    return text.strip()

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

def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return clean_text(text)

st.title("DFA-Based Skill Matching in Resume Screening")

# Input required skills
required_skills = st.text_area("Enter required skills (comma-separated):").lower().split(',')
required_skills = [skill.strip() for skill in required_skills if skill.strip()]

# Display the list of inputted skills
st.write("Inputted Skills:")
st.write(required_skills)

# Upload PDF files
uploaded_files = st.file_uploader("Upload up to 3 PDF resumes (max 25MB each)", type="pdf", accept_multiple_files=True)

if st.button("Process Resumes"):
    if not required_skills or not uploaded_files:
        st.error("Please provide required skills and upload resumes.")
    else:
        dfa = build_dfa(required_skills)
        for idx, uploaded_file in enumerate(uploaded_files, start=1):
            if uploaded_file.size > 25 * 1024 * 1024:
                st.error(f"File {uploaded_file.name} exceeds the 25MB limit.")
                continue
            resume_text = extract_text_from_pdf(uploaded_file).lower()
            st.write(f"Extracted Text from Resume {idx}:")
            st.write(resume_text)  # Debugging statement to check extracted text
            matched = check_skill(dfa, resume_text)
            matched = [skill for skill in required_skills if any(skill in match for match in matched)]
            missing = [skill for skill in required_skills if skill not in matched]
            st.write(f"Processing Resume {idx}:")
            st.write(f"Total Matched Skills: {len(matched)}")
            st.write("Matched Skills:")
            st.write(matched)
            st.write("Missing Skills:")
            st.write(missing)
            st.write("-" * 40)