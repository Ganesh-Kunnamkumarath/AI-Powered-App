# 🚀 AI-Powered Code Summarizer

AI-Powered Code Summarizer is a tool that analyzes JavaScript/TypeScript code files, provides inline comments, and generates concise summaries using OpenAI's GPT models. It works in three different modes: 
- 🖥️ **CLI Mode**: Runs locally via the command line.
- 🌐 **GUI Mode (Local)**: Provides a Streamlit-based browser interface for local usage.
- ☁️ **Cloud Mode**: Hosted on Streamlit Cloud, allowing users to upload files and compare before/after versions.

## ✨ Features
- 🤖 **Automatic Code Analysis**: Uses OpenAI API to generate concise summaries and inline comments.
- 🔄 **Multi-Mode Usage**: Supports CLI, local GUI, and cloud-based processing.
- 📂 **File Upload Support**: Users can upload `.js`, `.ts`, `.tsx`, and `.jsx` files for review.
- 🆚 **Side-by-Side Comparison**: The cloud version allows users to compare original and modified code.
- 🎯 **Selective File Processing**: Allows choosing specific files while ignoring unnecessary directories.
- 🔙 **Review Restoration (GUI Mode)**: Users can move reviewed files back to their original locations.

## 🛠️ Tech Stack
- 🐍 **Programming Language**: Python 3.12+
- 📚 **Libraries**: OpenAI, Streamlit, OS, Shutil, Time, Sys
- ☁️ **Hosting**: Streamlit Cloud

## 📌 Development Steps Followed
1. 📋 **Define Requirements**: Identify features needed for CLI, GUI, and cloud versions.
2. 🔧 **Set Up Environment**: Install dependencies and configure OpenAI API.
3. 💻 **Develop CLI Version**: Implement core functionality for local processing.
4. 🌍 **Develop GUI Version**: Build a Streamlit-based UI for local browser usage.
5. ☁️ **Develop Cloud Version**: Adapt the GUI for Streamlit Cloud deployment.
6. 🛠️ **Testing & Optimization**: Debug, optimize, and improve performance.
7. 🚀 **Deployment**: Deploy the app on Streamlit Cloud.

## 📥 Installation
### Prerequisites
Ensure you have the following installed:
- 🐍 Python 3.12+
- 📦 Required Python libraries:
  ```sh
  pip install openai streamlit
  ```

## 🚀 Usage

### 1️⃣ Command Line Mode (`index-cli.py`)
Run the CLI tool to process a project directory:
```sh
python index-cli.py
```
- Prompts the user for a project directory.
- Copies relevant files into a `draft-review` folder.
- Analyzes and comments on files using OpenAI.
- Saves the processed files in `draft-review`.


🎥 **Demo:**

<a href="https://www.youtube.com/watch?v=bp1F5jUyRLY" target="_blank">
  <img src="https://img.youtube.com/vi/bp1F5jUyRLY/0.jpg" alt="Demo Video">
</a>




### 2️⃣ GUI Mode (Local) (`index-gui.py`)
Launch the Streamlit-based local GUI:
```sh
streamlit run index-gui.py
```
- Enter a directory path containing JavaScript/TypeScript files.
- Select folders to exclude (e.g., `node_modules`).
- Click "Start Processing" to analyze and comment on code.
- Optionally restore reviewed files to their original location.

🎥 **Demo:** 
<a href="https://www.youtube.com/watch?v=JFW8f8z8HdQ" target="_blank">
  <img src="https://img.youtube.com/vi/JFW8f8z8HdQ/0.jpg" alt="Demo Video">
</a>


### 3️⃣ Cloud Mode (`streamlit_app.py`)
This version is deployed on **Streamlit Cloud**.
- 📂 Upload a single `.js`, `.ts`, `.tsx`, or `.jsx` file.
- 🤖 Click "Process File" to analyze and enhance documentation.
- 🔄 Compare original and modified code side-by-side.
- 📥 Download the modified file for further use.

🌍 **Access the Cloud Version:** [AI-Powered Code Summarizer](https://intelligent-ai-codereviewer-documenter.streamlit.app/)

🎥 **Demo:**
<a href="https://www.youtube.com/watch?v=BPYolx0a-14" target="_blank">
  <img src="https://img.youtube.com/vi/BPYolx0a-14/0.jpg" alt="Demo Video">
</a>



## ⚙️ Configuration
Modify the file extensions or exclusion settings in the respective script files:
- ✅ **Allowed File Extensions**: `.ts`, `.js`, `.tsx`, `.jsx`
- 🚫 **Excluded Folders**: `node_modules`, `static`, `.next`, `draft-review`

## 🚢 Deployment (Streamlit Cloud)
1. 📂 Push the repository to GitHub.
2. 🔗 Sign in to [Streamlit Cloud](https://share.streamlit.io/).
3. 🚀 Deploy the `streamlit_app.py` file by linking your GitHub repository.

## 🛣️ Roadmap
- [ ] ⚡ Implement parallel processing for faster analysis.
- [ ] 🧠 Cache AI responses to avoid redundant API calls.
- [ ] 🖥️ Package as a standalone desktop app.

## 📜 License
MIT License

## 👤 Author
Developed by Ganesh Kunnamkumarath
