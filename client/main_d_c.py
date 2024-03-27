import requests

# Server details
server_url = 'http://localhost:5000'
token = '5466578965'  # Replace with the special token

# Function to download file
def download_file():
    # Make the request to download the file
    response = requests.get(f'{server_url}/download', params={'token': token})

    # Check if the request was successful
    if response.status_code == 200:
        # Save the file
        with open('downloaded_file.txt', 'wb') as f:
            f.write(response.content)
        print('File downloaded successfully')
    else:
        print('Error downloading file')

if __name__ == '__main__':
    download_file()
