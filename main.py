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
    output = {}  # Stores the final matched patterns
    failure = {} # Reference of required skills in a trie/tree

    # Construct trie for each required skills
    for skill in skills:
        state = ""
        for char in skill:
            if char not in dfa[state]:
                dfa[state][char] = state + char
            state = dfa[state][char]
        output[state] = skill # Final state

     # Go to mechanism that handles the transitions between states 
    queue = deque()
    for char, next_state in dfa[""].items():
        failure[next_state] = ""
        queue.append(next_state)

    # Failure mechanism that checks for longest suffix
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

# Output mechanism to check skills in resume text
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
st.markdown("Upload multiple resumes and enter the required skills to see matches.")

# Input Section
st.subheader("Enter Required Skills")
required_skills = st.text_area("Enter skills separated by commas (e.g., Python, Java, Machine Learning):").lower().split(',')
required_skills = [skill.strip() for skill in required_skills if skill.strip()]

# Display inputted skills
if required_skills:
    st.write("**Inputted Skills:**")
    st.write(required_skills)

# Upload Multiple Resumes
st.subheader("Upload Resumes")
uploaded_files = st.file_uploader("Upload multiple PDF resumes (max 25MB each)", type="pdf", accept_multiple_files=True)

# Process Resume Button
if st.button("Match Skills"):
    if not required_skills or not uploaded_files:
        st.error("Please provide required skills and upload at least one resume.")
    else:
        dfa, failure, output = build_aho_corasick(required_skills)
        results = {}

        for uploaded_file in uploaded_files:
            if uploaded_file.size > 25 * 1024 * 1024:
                st.error(f"File {uploaded_file.name} exceeds the 25MB limit.")
                continue

            with st.spinner(f"Processing {uploaded_file.name}..."):
                resume_text = extract_text_from_pdf(uploaded_file).lower()
                matched_skills = check_skills(dfa, failure, output, resume_text)
                missing_skills = [skill for skill in required_skills if skill not in matched_skills]

                results[uploaded_file.name] = {
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills
                }

        # Display Results
        st.success("Processing complete!")
        st.subheader("Results")

        for resume_name, result in results.items():
            st.write(f"### {resume_name}")
            
            # Matched Skills
            st.write("**Matched Skills:**")
            if result["matched_skills"]:
                for skill in result["matched_skills"]:
                    st.markdown(f"✅ {skill}")
            else:
                st.write("No skills matched.")

            # Missing Skills
            st.write("**Missing Skills:**")
            if result["missing_skills"]:
                for skill in result["missing_skills"]:
                    st.markdown(f"❌ {skill}")
            else:
                st.write("All skills matched!")

            # Summary
            total_skills = len(required_skills)
            matched_count = len(result["matched_skills"])
            progress = matched_count / total_skills if total_skills else 0
            st.write(f"**{matched_count} out of {total_skills} skills matched.**")
            st.progress(progress)

# Footer
st.markdown("---")
st.markdown("**Instructions:** Make sure to enter all required skills separated by commas.")
st.markdown("**Contact:** pahirapcpiamonte@gmail.com")
