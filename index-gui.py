import os
import openai
import shutil
import time
import sys
import streamlit as st
client = openai.Client()

def create_draft_folder(target_path):
    """
    Creates a 'draft-review' folder inside the given target directory.
    Ensures the path exists before proceeding.
    """
    if not os.path.isdir(target_path):
        st.error("Invalid folder path. Please enter a valid project directory.")
        return None
    
    draft_folder = os.path.join(target_path, "draft-review")
    os.makedirs(draft_folder, exist_ok=True)
    return draft_folder

def copy_files_to_draft(source_path, draft_folder, exclude_folders, allowed_file_extensions):
    """
    Recursively copies allowed files from source_path to draft_folder.
    Skips excluded directories and ensures 'draft-review' itself is not copied.
    """
    file_map = {}  # Store mapping of original → draft file paths

    for root, dirs, files in os.walk(source_path):
        dirs[:] = [d for d in dirs if d not in exclude_folders and os.path.join(root, d) != draft_folder]
        
        for file in files:
            if not file.lower().endswith(tuple(allowed_file_extensions)):
                continue  # Skip files that don't match allowed extensions
            
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(source_file, source_path)
            target_file = os.path.join(draft_folder, relative_path)
            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            if not os.path.exists(target_file):  # Avoid overwriting existing files
                shutil.copy2(source_file, target_file)

            file_map[target_file] = source_file  # Map draft file to original file

    return file_map

def analyze_and_comment_code(file_path):
    """
    Reads the given code file, sends it to OpenAI for analysis, and retrieves inline comments and a summary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, IsADirectoryError):
        st.warning(f"Skipping non-text file: {file_path}")
        return None  
    
    prompt = f"""
    You are an AI code reviewer. Read the following code and:
    1. Generate a short summary explaining the file's purpose in simple terms.
    2. Add meaningful inline comments without replacing the original code.
    3. Ensure comments clarify complex logic while keeping the code readable.
    4. Place the summary as a top-level comment in the file.
    5. Do NOT use triple backticks (```) or Markdown formatting.
    
    Code:
    {content}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content

def process_files_in_draft(draft_folder):
    """
    Iterates through all files in the draft folder, processes each with AI, and saves the modified content.
    """
    files_to_process = []
    for root, _, files in os.walk(draft_folder):
        for file in files:
            files_to_process.append(os.path.join(root, file))
    
    total_files = len(files_to_process)
    
    st.write("Processing files...")
    progress_bar = st.progress(0)
    for i, file_path in enumerate(files_to_process, start=1):
        progress = i / total_files  # Calculate progress ratio
        progress_bar.progress(progress)  # Update progress bar
        st.text(f"Processing file {i}/{total_files}: {file_path}")
        # time.sleep(0.5)  # Simulating processing time

        modified_content = analyze_and_comment_code(file_path)
        if modified_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_content)

    progress_bar.empty()  # Remove the progress bar when done
    st.success("Processing complete! ✅")

def restore_reviewed_files(file_map, reviewed_files):
    """
    Moves reviewed files back to their original locations.
    """
    for draft_file in reviewed_files:
        original_file = file_map.get(draft_file)  # Get the original path
        if original_file:
            shutil.move(draft_file, original_file)  # Move the reviewed file back
        else:
            st.warning(f"Original path for {draft_file} not found!")
    st.success("Reviewed files restored successfully!")

# Streamlit UI
st.title("AI-Powered Code Reviewer")

# User inputs
source_code_path = st.text_input("Enter the project directory to scan:")
exclude_folders = st.multiselect("Select folders to exclude:", ["node_modules", "static", ".next", "draft-review"], default=["node_modules", "static", ".next", "draft-review"])
allowed_file_extensions = st.multiselect("Select file types to process:", [".ts", ".js", ".tsx", ".jsx"], default=[".ts", ".js", ".tsx", ".jsx"])

if st.button("Start Processing", disabled=not source_code_path.strip()):
    if not source_code_path:
        st.error("Please enter a valid project directory.")
    else:
        exclude_folders_set = set(exclude_folders)
        draft_path = create_draft_folder(source_code_path)
        if draft_path:
            st.session_state.file_map = copy_files_to_draft(source_code_path, draft_path, exclude_folders_set, allowed_file_extensions)
            process_files_in_draft(draft_path)



# Offline Review UI
st.subheader("Offline Review & Restore")
draft_folder = os.path.join(source_code_path, "draft-review")

if os.path.exists(draft_folder):
    reviewed_files = []
    for root, _, files in os.walk(draft_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if st.checkbox(f"Reviewed: {file}", key=file_path):
                reviewed_files.append(file_path)

    if st.button("Restore Reviewed Files", disabled=len(reviewed_files) == 0):
        if "file_map" in st.session_state:
            restore_reviewed_files(st.session_state.file_map, reviewed_files)
            st.rerun()  # 🔄 Refresh UI to update file list
        else:
            st.error("File map not found! Please start processing first.")



# Next steps
# 1. Offline Review & Restore     - Done

# 2. Performance Optimization
#     Parallel Processing: Use Python’s concurrent.futures.ThreadPoolExecutor to process multiple files simultaneously.
#     Cache AI Results: Implement a hash-based caching system to store AI responses for unchanged files, reducing redundant API calls.

# 3. Online Deployment
#     Streamlit Cloud: Push your app to GitHub and deploy via Streamlit Cloud.
#     Hugging Face Spaces: Set up a Hugging Face Space using the Streamlit template for wider reach.

# 4. Packaging as a Desktop App
#     PyInstaller: Create a .dmg for macOS using pyinstaller --onefile --windowed.
#     Dependencies Handling: Ensure required packages are bundled correctly.
#     Testing: Run the .dmg file on another Mac to verify installation.

