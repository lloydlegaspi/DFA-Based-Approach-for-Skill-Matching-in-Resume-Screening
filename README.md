## DFA-Based-Approach-for-Skill-Matching-in-Resume-Screening
This project automates resume screening using a Deterministic Finite Automata (DFA)-based skill-matching algorithm. It helps recruiters process large volumes of resumes efficiently by detecting and matching candidate skills with job requirements.

Since this is only a prototype, limited features of the said project will be implemented like string matching, this requires input skills that will be the basis for the matching of the skills that are in resumes.txt

## Features
- **Skill Matching:** Scans resumes and identifies required skills using DFA.
- **Multi-pattern Detection:** Handles multiple skill patterns efficiently.
- **Output Reports:** Generates a list of matched and missing skills for each resume.


## Limitations of the Prototype
- Simple Matching Logic: The current DFA checks for word-level matches, meaning skills that are not exact word matches (e.g., "Pythonic" or "Microsoft Word") may be overlooked.
- No Case Sensitivity Handling: The matching process assumes the case matches exactly (e.g., "python" will not match "Python").
- Single-word Skills: Multi-word skills like "Computer Science" are treated as separate strings and need precise matching.


## Prerequisites using Python
- Python 3.8 or higher.
- Python Interpreter

## Installation
1. Clone this repository:
   ```bash
   git clone <repo_url>
   
2.  cd DFA-Based-Approach-for-Skill-Matching-in-Resume-Screening
  
3. pip install -r requirements.txt
   - use this only if we will implement PDF or GUI features of the prototype
  
   

## Run the Script
   - Navigate to the `src` folder where `main.py` is stored and run:
     ```bash
     python main.py
     
