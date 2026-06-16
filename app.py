import streamlit as st
import os
import random
import time
import json

# --- 1. CONFIGURATION ---
UPLOAD_DIR = "uploads"
DB_FILE = "database.json"

# Ensure our upload folder and database exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

# --- 2. MULTI-USER DATABASE FUNCTIONS ---
def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

def generate_unique_code(db):
    """Generates the 12-digit mixed fraction: XXXXXX XXX/XXX"""
    while True:
        whole = random.randint(100000, 999999) # 6 digits
        num = random.randint(100, 999)         # 3 digits
        den = random.randint(100, 999)         # 3 digits
        code = f"{whole} {num}/{den}"
        
        if code not in db:
            return code

# --- 3. STREAMLIT USER INTERFACE ---
st.set_page_config(page_title="SP - Global File Share", page_icon="🌐", layout="centered")

st.title("🌐 SP - Global File Share")
st.markdown("Securely transfer files using a unique 12-digit mixed fraction code.")

# Create two tabs for Sender and Receiver
tab_upload, tab_download = st.tabs(["📤 Sender (Upload)", "📥 Receiver (Download)"])

# --- SENDER ENGINE ---
with tab_upload:
    st.subheader("Upload a File to Generate Code")
    uploaded_file = st.file_uploader("Choose any file to share", label_visibility="collapsed")
    
    if st.button("Upload & Generate SP Code", use_container_width=True, type="primary"):
        if uploaded_file is not None:
            # Create a safe, unique filename to prevent multi-user overwriting
            safe_name = f"{int(time.time())}_{uploaded_file.name}"
            save_path = os.path.join(UPLOAD_DIR, safe_name)
            
            # Save the file to the disk
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Generate code and update the global database
            db = load_db()
            unique_code = generate_unique_code(db)
            db[unique_code] = {
                "original_name": uploaded_file.name, 
                "path": save_path
            }
            save_db(db)
            
            # Display Success
            st.success("File Uploaded Successfully!")
            st.write("Share this exact code with the receiver:")
            st.info(f"**{unique_code}**")
        else:
            st.error("Please select a file first.")

# --- RECEIVER ENGINE ---
with tab_download:
    st.subheader("Retrieve a Shared File")
    user_code = st.text_input("Enter the 12-digit SP Code (e.g., 123456 789/123)")
    
    if st.button("Retrieve File", use_container_width=True):
        db = load_db()
        user_code = user_code.strip()
        
        if user_code in db:
            file_info = db[user_code]
            file_path = file_info["path"]
            
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                
                st.success(f"File Found: {file_info['original_name']}")
                
                # Streamlit's built-in secure download button
                st.download_button(
                    label="📥 Click here to Download",
                    data=file_bytes,
                    file_name=file_info['original_name'],
                    use_container_width=True,
                    type="primary"
                )
            else:
                st.error("Error: The file exists in the database but is missing from the server.")
        else:
            st.error("Invalid or Expired SP Code. Please check the fraction formatting.")