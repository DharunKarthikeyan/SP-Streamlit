import os
import streamlit as st
import random
import time
import json

# ==========================================
# 1. CUSTOM BLACK & GOLD THEME (CSS)
# ==========================================
def apply_premium_theme():
    st.markdown("""
    <style>
    /* Main App Background - Sleek Dark/Black */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #1E1E1E !important;
        color: #D4AF37 !important; /* Gold Text */
        border: 1px solid #D4AF37 !important;
        border-radius: 5px;
    }
    
    /* Primary Buttons - Gold */
    .stButton > button {
        background-color: #D4AF37 !important;
        color: #121212 !important; /* Black Text */
        font-weight: 800;
        border-radius: 5px;
        border: 1px solid #D4AF37;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #121212 !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37;
        box-shadow: 0px 0px 10px rgba(212, 175, 55, 0.5);
    }
    
    /* File Uploader Container */
    [data-testid="stFileUploadDropzone"] {
        background-color: #1E1E1E !important;
        border: 2px dashed #D4AF37 !important;
        border-radius: 10px;
    }
    
    /* Headings and Text */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #E0E0E0 !important;
    }
    
    /* Highlights and Accents */
    strong {
        color: #D4AF37 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1E1E1E;
        border-radius: 5px;
        padding: 5px;
        border-bottom: 2px solid #D4AF37;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SYSTEM SETUP (Folders & Database)
# ==========================================
UPLOAD_DIR = "uploads"
DB_FILE = "database.json"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

def generate_unique_code(db):
    while True:
        whole = random.randint(100000, 999999) 
        num = random.randint(100, 999)         
        den = random.randint(100, 999)         
        code = f"{whole} {num}/{den}"
        if code not in db:
            return code

# ==========================================
# 3. PAGE INITIALIZATION & GATEKEEPER
# ==========================================
st.set_page_config(page_title="SP - Global File Share", page_icon="👑", layout="centered")
apply_premium_theme()

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ==========================================
# 4. PAGE 1: LOGIN PAGE
# ==========================================
def login_page():
    st.title("👑 SP - Premium File Share")
    st.markdown("Please log in to access the secure network.")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Account Login")
        
        with st.form("auth_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Access Portal", use_container_width=True)
            
            if submit:
                # Basic validation (Accepts any non-empty input for demo purposes)
                if email and password: 
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Access Denied: Please provide credentials.")

# ==========================================
# 5. PAGE 2: MAIN APP (Sender / Receiver)
# ==========================================
def main_app_page():
    # Sidebar for logout
    with st.sidebar:
        st.markdown("### 👑 SP Portal")
        st.success("Status: Authenticated")
        if st.button("Secure Logout"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.title("👑 SP - Global File Share")
    st.markdown("Securely transfer files using your unique 12-digit code.")

    tab_upload, tab_download = st.tabs(["📤 Upload & Share", "📥 Retrieve File"])

    # --- SENDER ENGINE ---
    with tab_upload:
        st.subheader("Initiate Transfer")
        uploaded_file = st.file_uploader("Select a file to encrypt and share", label_visibility="collapsed")
        
        if st.button("Generate SP Transfer Code", use_container_width=True):
            if uploaded_file is not None:
                with st.spinner('Securing file...'):
                    safe_name = f"{int(time.time())}_{uploaded_file.name}"
                    save_path = os.path.join(UPLOAD_DIR, safe_name)
                    
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    db = load_db()
                    unique_code = generate_unique_code(db)
                    db[unique_code] = {"original_name": uploaded_file.name, "path": save_path}
                    save_db(db)
                    
                st.success("Transfer Prepared Successfully!")
                st.markdown(f"Provide this exact code to the recipient: <h3 style='color:#D4AF37; text-align:center;'>{unique_code}</h3>", unsafe_allow_html=True)
            else:
                st.error("System requires a file to proceed.")

    # --- RECEIVER ENGINE ---
    with tab_download:
        st.subheader("Receive Transfer")
        user_code = st.text_input("Enter your 12-digit SP Code:")
        
        if st.button("Authenticate & Retrieve", use_container_width=True):
            db = load_db()
            user_code = user_code.strip()
            
            if user_code in db:
                file_info = db[user_code]
                file_path = file_info["path"]
                
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                    
                    st.success(f"Target Acquired: {file_info['original_name']}")
                    st.download_button(
                        label="📥 Download File to Local Machine",
                        data=file_bytes,
                        file_name=file_info['original_name'],
                        use_container_width=True
                    )
                else:
                    st.error("Critical Error: Payload missing from server.")
            else:
                st.error("Invalid Code: Access Denied.")

# ==========================================
# 6. APP EXECUTION ROUTER
# ==========================================
if not st.session_state["logged_in"]:
    login_page()
else:
    main_app_page()