import os

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

def check_skill(dfa, resume_text):
    """
    Check for the presence of skills in the given text using the DFA.
    """
    matches = []
    words = resume_text.split()
    for word in words:
        state = dfa
        for char in word:
            if char in state:
                state = state[char]
            else:
                state = None
                break
        if state and 'is_end' in state:
            matches.append(word)
    return matches

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

# Define the list of required skills
required_skills = ['Python', 'C#', 'Microsoft', 'HTML', 'JavaScript', 'Computer Science']

# Build the DFA from the required skills
dfa = build_dfa(required_skills)

# Example directory of resumes (replace with your path)
resume_dir = "C:/Users/alix/Documents/DFA-Based-Approach-for-Skill-Matching-in-Resume-Screening/data/resumes/"
resume_texts = extract_text_from_resumes(resume_dir)

for idx, resume in enumerate(resume_texts, start=1):
    print(f"Processing Resume {idx}:")
    matched = check_skill(dfa, resume)
    missing = [skill for skill in required_skills if skill not in matched]
    print(f"  Matched Skills: {matched}")
    print(f"  Missing Skills: {missing}")
    print(f"  Total Matched Skills: {len(matched)}")
    print("-" * 40)