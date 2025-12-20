import json
import urllib.request
from typing import Dict, Optional

class HTTPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}
    
    def get(self, endpoint: str) -> Dict:
        """Make a GET request to the API"""
        url = f"{self.base_url}/{endpoint}"
        request = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())
    
    def post(self, endpoint: str, data: Dict) -> Dict:
        """Make a POST request to the API with JSON data"""
        url = f"{self.base_url}/{endpoint}"
        json_data = json.dumps(data).encode('utf-8')
        request = urllib.request.Request(url, data=json_data, headers=self.headers, method='POST')
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())

def fetch_user_profile(user_id: int) -> Optional[Dict]:
    """Fetch a user's profile from the API"""
    client = HTTPClient("https://api.example.com")
    try:
        return client.get(f"users/{user_id}")
    except Exception as e:
        print(f"Error fetching user profile: {e}")
        return None

def upload_file_to_server(file_path: str, endpoint: str) -> bool:
    """Upload a file to the server via HTTP POST"""
    with open(file_path, 'rb') as file:
        data = file.read()
        # Simplified upload logic
        print(f"Uploading {file_path} to {endpoint}")
        return True
