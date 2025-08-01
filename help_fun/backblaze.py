import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time, string, random

load_dotenv()

class BackblazeB2:
    def __init__(self):
        self.key_id = os.getenv("BACKBLAZE_KEY_ID")
        self.app_key = os.getenv("BACKBLAZE_APP_KEY")
        self.bucket_id = os.getenv("BACKBLAZE_BUCKET_ID")
        self.bucket_name = os.getenv("BACKBLAZE_BUCKET_NAME")

        if not all([self.key_id, self.app_key, self.bucket_id, self.bucket_name]):
            raise ValueError("Missing Backblaze credentials in environment variables.")

        self.auth_data = self._authorize()

    def _authorize(self):
        url = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
        response = requests.get(url, auth=(self.key_id, self.app_key))
        if response.status_code != 200:
            raise ConnectionError(f"Auth failed: {response.text}")
        return response.json()

    def upload_file(self, file_data: bytes, file_name: str, user_id: int = 0):


        epoch = int(time.time())

        characters = ''.join(random.choices(string.ascii_letters, k=6))
        
        api_url = self.auth_data['apiUrl']
        headers = {"Authorization": self.auth_data['authorizationToken']}

        file_name = f"{epoch}_{characters}_{user_id}_{file_name}"

        upload_url_endpoint = f"{api_url}/b2api/v2/b2_get_upload_url"
        payload = {"bucketId": self.bucket_id}
        upload_url_res = requests.post(upload_url_endpoint, headers=headers, json=payload)

        if upload_url_res.status_code != 200:
            raise Exception(f"Failed to get upload URL: {upload_url_res.text}")

        upload_info = upload_url_res.json()
        upload_headers = {
            "Authorization": upload_info['authorizationToken'],
            "X-Bz-File-Name": file_name,
            "Content-Type": "b2/x-auto",
            "X-Bz-Content-Sha1": "do_not_verify"
        }

        upload_res = requests.post(upload_info['uploadUrl'], headers=upload_headers, data=file_data)

        if upload_res.status_code != 200:
            raise Exception(f"Upload failed: {upload_res.text}")

        return {"file_name": file_name, "status": "uploaded"}

    def get_signed_url(self, file_name: str, expiry: int = 120):
        api_url = self.auth_data['apiUrl']
        headers = {"Authorization": self.auth_data['authorizationToken']}

        download_auth_url = f"{api_url}/b2api/v2/b2_get_download_authorization"
        payload = {
            "bucketId": self.bucket_id,
            "fileNamePrefix": file_name,
            "validDurationInSeconds": expiry
        }

        response = requests.post(download_auth_url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Failed to get download auth: {response.text}")

        token = response.json()["authorizationToken"]
        return f"{self.auth_data['downloadUrl']}/file/{self.bucket_name}/{file_name}?Authorization={token}"
    
    def delete_file(self, file_name: str):
        api_url = self.auth_data['apiUrl']
        headers = {"Authorization": self.auth_data['authorizationToken']}

        # Step 1: Get file ID from list_file_versions
        list_versions_url = f"{api_url}/b2api/v2/b2_list_file_versions"
        payload = {
            "bucketId": self.bucket_id,
            "prefix": file_name,
            "maxFileCount": 1
        }

        list_response = requests.post(list_versions_url, headers=headers, json=payload)

        if list_response.status_code != 200:
            raise Exception(f"Failed to get file versions: {list_response.text}")

        files = list_response.json().get("files", [])
        if not files:
            raise FileNotFoundError(f"No file found with name '{file_name}'.")

        file_id = files[0]["fileId"]

        # Step 2: Delete file
        delete_url = f"{api_url}/b2api/v2/b2_delete_file_version"
        delete_payload = {
            "fileName": file_name,
            "fileId": file_id
        }

        delete_response = requests.post(delete_url, headers=headers, json=delete_payload)

        if delete_response.status_code != 200:
            raise Exception(f"Failed to delete file: {delete_response.text}")

        return {"status": "deleted", "file_name": file_name}

    



