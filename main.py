import os
import streamlit as st
from PyPDF2 import PdfReader
import re
from collections import deque, defaultdict

# Function to clean text
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]+', '', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with one space
    return text.strip()

# Function to build Aho-Corasick DFA manually
def build_aho_corasick(skills):
    dfa = defaultdict(dict) # dic is is used to represent states and transitions (Trie)
    output = {} # Stores the final matched patterns
    failure = {} # Reference of required skills in a trie/tree
    
    # Construct trie for each required skills
    for skill in skills:
        state = ""
        for char in skill:
            if char not in dfa[state]: 
                dfa[state][char] = state + char
            state = dfa[state][char]
        output[state] = skill # Final state
    
    # Go to function handles the transitions between states 
    queue = deque()
    for char, next_state in dfa[""].items():
        failure[next_state] = ""
        queue.append(next_state)
    
    # Failure function checks for longest suffix
    while queue:
        current_state = queue.popleft()
        for char, next_state in dfa[current_state].items():
            queue.append(next_state)
            fail_state = failure[current_state]
            while fail_state and char not in dfa[fail_state]:
                fail_state = failure.get(fail_state, "")
            failure[next_state] = dfa.get(fail_state, {}).get(char, "")
            if failure[next_state] in output:
                output[next_state] = output.get(next_state, '') or output[failure[next_state]]
    
    return dfa, failure, output

# Output function to check skills in resume text
def check_skills(dfa, failure, output, resume_text):
    state = ""
    matches = set()
    
    for char in resume_text:
        while state and char not in dfa[state]:
            state = failure.get(state, "")
        state = dfa.get(state, {}).get(char, "")
        if state in output:
            matches.add(output[state])
    
    return list(matches)

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
st.title("Resume Skill Matcher - DFA-based Aho-Corasick")
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
                dfa, failure, output = build_aho_corasick(required_skills)
                matched_skills = check_skills(dfa, failure, output, resume_text)
                missing_skills = [skill for skill in required_skills if skill not in matched_skills]

                # Display Results
                st.success("Processing complete!")
                st.subheader("Results")

                # Matched Skills
                st.write("**Matched Skills:**")
                if matched_skills:
                    for skill in matched_skills:
                        st.markdown(f"✅ {skill}")
                else:
                    st.write("No skills matched.")

                # Missing Skills
                st.write("**Missing Skills:**")
                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(f"❌ {skill}")
                else:
                    st.write("All skills matched!")

                # Summary
                st.subheader("Summary")
                st.write(f"**{len(matched_skills)} out of {len(required_skills)} skills matched.**")
                progress = len(matched_skills) / len(required_skills) if required_skills else 0
                st.progress(progress)

# Footer
st.markdown("---")
st.markdown("**Instructions:** Make sure to enter all required skills separated by commas.")
st.markdown("**Contact:** support@resumematcher.com")
