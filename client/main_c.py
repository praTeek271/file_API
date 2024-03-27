import requests
import secrets
import os
import hashlib

# Server details
server_url = 'http://localhost:5000'
username = 'admin'
password = '72password'

# Function to upload files
def upload_files(username, file_paths):
    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        # File to be uploaded
        files = {'file': open(file_path, 'rb')}
        
        # Additional data: name and token
        data = {'name': f'{username}', 'token': '{0}'.format(secrets.token_urlsafe(16))}
        
        try:
            # Make the request
            response = requests.post(f'{server_url}/upload', files=files, data=data, auth=(username, hashed_password))
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error uploading file {file_path}: {e}")
            continue
        
        # Print response
        try:
            json_response = response.json()
            print(f"Token for {file_path}: [ {json_response['token']} ]")
            print(f"Response status code for {file_path}: {response.status_code}")
            print(f"Download link for {file_path}: {json_response['download_link']}\n")
        except ValueError:
            print(f"Error decoding JSON response for {file_path}")

if __name__ == '__main__':
    username = input("Enter your name: ")
    file_paths = ['file1.txt', 'file2.png']  # Replace with the paths to your files
    upload_files(username, file_paths)
