import os
import openai
import shutil
import time
import sys
client = openai.Client()

def create_draft_folder(target_path):
    """
    Creates a 'draft-review' folder inside the given target directory.
    Ensures the path exists before proceeding.
    """
    if not os.path.isdir(target_path):
        print("Invalid folder path. Please enter a valid project directory.")
        return None
    
    draft_folder = os.path.join(target_path, "draft-review")
    os.makedirs(draft_folder, exist_ok=True)
    return draft_folder

def copy_files_to_draft(source_path, draft_folder, exclude_folders, allowed_file_extensions):
    """
    Recursively copies allowed files from source_path to draft_folder.
    Skips excluded directories and ensures 'draft-review' itself is not copied.
    """
    for root, dirs, files in os.walk(source_path):
        # Ensure 'draft-review' folder is not copied if it already exists
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

def analyze_and_comment_code(file_path):
    """
    Reads the given code file, sends it to OpenAI for analysis, and retrieves inline comments and a summary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, IsADirectoryError):
        print(f"Skipping non-text file: {file_path}")
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
    
    print("Processing files...")
    for i, file_path in enumerate(files_to_process, start=1):
        sys.stdout.write(f"\rProcessing files: {i}/{total_files}... ")
        sys.stdout.flush()
        print(f"Processing: {file_path}")
        
        modified_content = analyze_and_comment_code(file_path)
        if modified_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_content)
    
    print("\nProcessing complete!")


# Get user input for project directory
source_code_path = input("Enter the project directory to scan: ")
exclude_folders = {"node_modules", "static", ".next"}
allowed_file_extensions = {".jsx"}  # Allowed file types
draft_path = create_draft_folder(source_code_path)

if draft_path:
    copy_files_to_draft(source_code_path, draft_path, exclude_folders, allowed_file_extensions)
    process_files_in_draft(draft_path)
