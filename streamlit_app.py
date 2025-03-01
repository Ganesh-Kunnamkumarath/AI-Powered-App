import streamlit as st
import openai
import os
import time
client = openai.Client()

# Function to analyze code and add comments using OpenAI
def analyze_and_comment_code(file_content):
    """
    Sends the file content to OpenAI to generate a summary and add inline comments.
    """
    prompt = f"""
    You are an AI code reviewer. Read the following code and:
    1. Generate a short summary explaining the file's purpose in simple terms.
    2. Add meaningful inline comments without replacing the original code.
    3. Ensure comments clarify complex logic while keeping the code readable.
    4. Place the summary as a top-level comment in the file.
    5. Do NOT use triple backticks (```) or Markdown formatting.
    
    Code:
    {file_content}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )

        # st.write(response)
        return response.choices[0].message.content

    except Exception as e:
        st.error(f"OpenAI API Error: {str(e)}")  # Show exact error in Streamlit
        return f"Error processing file: {str(e)}"

# Main function to run the Streamlit app
def main():
    st.set_page_config(layout="wide")  # Set the layout to full width
    st.title("AI Code Reviewer for React & Next.js")
    st.write("Upload a .js, .ts, .tsx, or .jsx file to analyze and enhance documentation.")

    uploaded_file = st.file_uploader("Upload a file", type=["js", "ts", "tsx", "jsx"])

    # Move buttons to the top
    col_top1, col_top2 = st.columns([0.7, 0.3])
    with col_top1:
        process_clicked = st.button("Process File", type="primary")
    with col_top2:
        download_placeholder = st.empty()
    
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        
        col1, col2 = st.columns(2)  # Create two equal columns for side-by-side comparison
        with col1:
            st.subheader("Original Code")
            st.code(file_content, language="javascript")
        
        if process_clicked:
            loader_placeholder = st.empty()
            loader_placeholder.markdown(
                """
                <div id="loader" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                background: rgba(0,0,0,0.3); display: flex; align-items: center; 
                justify-content: center; color: white; font-size: 24px; z-index: 9999;">
                🧠 🔄 Processing... Please wait.
                </div>
                """,
                unsafe_allow_html=True
            )
            
            start_time = time.time()
            modified_content = analyze_and_comment_code(file_content)
            elapsed_time = time.time() - start_time
            
            if elapsed_time > 25:
                modified_content = "Processing took too long. Please try again later."
            elif "Error processing file" in modified_content:
                modified_content = "An error occurred while processing the file. Please check the input and try again."
            
            time.sleep(1)  # Simulate processing time
            loader_placeholder.empty()  # Hide loader after processing
            
            with col2:
                st.subheader("Modified Code")
                st.code(modified_content, language="javascript")
            
            # Provide a download button for the modified file
            download_placeholder.download_button(
                label="✅ Download Modified File",
                data=modified_content,
                file_name=f"modified_{uploaded_file.name}",
                mime="text/plain"
            )
    else:
        if process_clicked:
            st.error("Please upload a valid file before processing.")

if __name__ == "__main__":
    main()
