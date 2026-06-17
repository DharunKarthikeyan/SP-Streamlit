# 👑 SFS - secure file sharing

A sleek, secure, and lightweight web-based file-sharing portal built with Python and Streamlit. This application acts as a secure digital dropbox, allowing users to upload files and share them across a network using uniquely generated cryptographic fraction codes.

## 🗝️ The "Keys" Mechanism
This application uses a unique key generation system to secure and retrieve files instead of standard URLs. 
* **Key Generation:** When a user uploads a file, the system generates a highly unique, 12-digit mixed-fraction code (e.g., `123456 789/123`).
* **Key Storage:** The key is stored in a local `database.json` ledger, mapping the fraction code to the physical file path on the server.
* **Key Retrieval:** The recipient must enter the exact 12-digit fraction key to authenticate and unlock the download sequence.

## ✨ Key Features
* **Secure Authentication Gatekeeper:** Users must authenticate via the login portal before accessing the upload or download engines.
* **Premium Custom UI:** Features a custom CSS-injected "Black & Gold" luxury theme, overriding standard framework visuals for a premium user experience.
* **File Collision Prevention:** Automatically appends Unix timestamps to incoming files, ensuring users never accidentally overwrite data with duplicate filenames.
* **Lightweight Data Ledger:** Operates without the overhead of a heavy SQL database. It relies entirely on a localized JSON dictionary system for rapid file mapping.

## 🛠️ Technical Stack
* **Frontend & Web Server:** Streamlit
* **Backend Logic:** Python 3.x
* **Data Persistence:** JSON (Local File System)
