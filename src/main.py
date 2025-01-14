import os
# import re

def build_dfa(skills):
    """
    Build a DFA for a list of skills.
    Each skill corresponds to a sequence of states in the DFA.
    """
    dfa = {}
    for skill in skills:
        state = dfa
        for char in skill:
            if char not in state:
                state[char] = {}
            state = state[char]
        state['is_end'] = True  # Mark the end of a skill
    return dfa

def check_skill(dfa, text):
    """
    Check for the presence of skills in the given text using the DFA.
    """
    matches = []
    missing = []
    for skill in skills:
        state = dfa
        found = True
        for char in skill:
            if char in state:
                state = state[char]
            else:
                found = False
                break
        if found and 'is_end' in state:
            matches.append(skill)
        else:
            missing.append(skill)
    return matches, missing

def extract_text_from_resumes(resume_dir):
    """
    Extract text from resume files stored in a directory.
    Supports plain text files (.txt) and extracts text content for analysis.
    """
    resume_texts = []
    for file in os.listdir(resume_dir):
        if file.endswith('.txt'):
            with open(os.path.join(resume_dir, file), 'r') as f:
                resume_texts.append(f.read())
    return resume_texts

# Input list of required skills
skills = ["Python", "C#", "DFA", "Automation", "String Matching"]
dfa = build_dfa(skills)

# Example directory of resumes (replace with your path)
resume_dir = "C:/Users/alix/Documents/DFA-Based-Approach-for-Skill-Matching-in-Resume-Screening/data/resumes/"
resume_texts = extract_text_from_resumes(resume_dir)

for idx, resume in enumerate(resume_texts, start=1):
    print(f"Processing Resume {idx}:")
    matched, missing = check_skill(dfa, resume)
    print(f"  Matched Skills: {matched}")
    print(f"  Missing Skills: {missing}")
    print("-" * 40)
