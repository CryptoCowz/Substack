#!/usr/bin/env python3
"""
Syncs generated Substack markdown and preview HTML files 
from GitHub Actions to a dated subfolder in Google Drive.
"""

import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PARENT_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID", "1_odUdVmseKHloV1tHxJfRTtJWebfOdML")
SERVICE_ACCOUNT_FILE = "gdrive_credentials.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

def upload_files():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"[!] Warning: {SERVICE_ACCOUNT_FILE} not found. Skipping Google Drive sync.")
        return

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive_service = build("drive", "v3", credentials=creds)

    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_title = f"{date_str}_Substack_Pasture_Drafts"

    # Search if dated folder exists
    query = f"name = '{folder_title}' and '{PARENT_FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    res = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = res.get("files", [])

    if files:
        target_folder_id = files[0]["id"]
        print(f"[*] Found existing dated folder: {folder_title} ({target_folder_id})")
    else:
        folder_metadata = {
            "name": folder_title,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [PARENT_FOLDER_ID]
        }
        f_obj = drive_service.files().create(body=folder_metadata, fields="id").execute()
        target_folder_id = f_obj.get("id")
        print(f"[+] Created new dated folder: {folder_title} ({target_folder_id})")

    # Upload files from output/substack
    files_to_upload = []
    source_dir = "output/substack"
    if os.path.exists(source_dir):
        for root, _, fs in os.walk(source_dir):
            for f in fs:
                files_to_upload.append(os.path.join(root, f))

    print(f"[*] Uploading {len(files_to_upload)} files to Google Drive...")

    for file_path in files_to_upload:
        file_name = os.path.basename(file_path)
        if file_name.endswith(".html"):
            mime_type = "text/html"
        elif file_name.endswith(".json"):
            mime_type = "application/json"
        else:
            mime_type = "text/markdown"

        file_metadata = {
            "name": file_name,
            "parents": [target_folder_id]
        }
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        try:
            drive_service.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()
            print(f"[✓] Uploaded: {file_name}")
        except Exception as e:
            print(f"[!] Error uploading {file_name}: {e}")

if __name__ == "__main__":
    upload_files()
