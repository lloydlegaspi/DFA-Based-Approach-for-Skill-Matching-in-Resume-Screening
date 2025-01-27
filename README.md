## DFA-Based-Approach-for-Skill-Matching-in-Resume-Screening
This project automates resume screening using a Deterministic Finite Automata (DFA)-based skill-matching algorithm. This will be run using streamlit as we use python and easy for making this prototype

Any lapses of the app/prototype can be improved as this prototype will only serve as a guide and visualization of the research


## Features
- **File Upload:** Handles file upload (PDF)
- **Skill Matching:** Scans resumes and identifies required skills using DFA.
- **Multi-pattern Detection:** Handles multiple skill patterns efficiently.
- **Output Reports:** Generates a list of matched and missing skills for each resume.


## Limitations of the Prototype
- Simple Matching Logic: The current DFA checks for word-level matches, meaning skills that are not exact word matches (e.g., "Pythonic" or "Microsoft Word") may be overlooked.
- PDF Text extraction may not be accurate as spaces, white spaces and other invisible characters may be detected



## Running the web-app  using streamlit

- cd "C:/Users/alix/Documents/DFA-Based-Approach-for-Skill-Matching-in-Resume-Screening/src/" (where the file directory is located)
  

## Run the Script
   - Navigate to the `src` folder where `main.py` is stored and run:
     
 streamlit run __name of the py. file
     
