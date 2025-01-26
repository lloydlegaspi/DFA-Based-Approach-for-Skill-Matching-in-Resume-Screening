## DFA-Based-Approach-for-Skill-Matching-in-Resume-Screening
This project automates resume screening using a Deterministic Finite Automata (DFA)-based skill-matching algorithm. 


## Features
- **File Upload:** Handles file upload (PDF)
- **Skill Matching:** Scans resumes and identifies required skills using DFA.
- **Multi-pattern Detection:** Handles multiple skill patterns efficiently.
- **Output Reports:** Generates a list of matched and missing skills for each resume.


## Limitations of the Prototype
- Simple Matching Logic: The current DFA checks for word-level matches, meaning skills that are not exact word matches (e.g., "Pythonic" or "Microsoft Word") may be overlooked.
- No Case Sensitivity Handling: The matching process assumes the case matches exactly (e.g., "python" will not match "Python").
- PDF Text extraction may not be accurate as spaces, white spaces and other invisible characters may be detected



## Running the web-app  using streamlit

- cd "C:/Users/alix/Documents/DFA-Based-Approach-for-Skill-Matching-in-Resume-Screening/src/" (where the file directory is located)
  

## Run the Script
   - Navigate to the `src` folder where `main.py` is stored and run:
     
 streamlit run __name of the py. file
     
