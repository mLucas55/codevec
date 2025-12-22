"""HTTP client for making API requests"""
import requests
import json
from typing import Optional, Dict, Any

class HTTPClient:
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.timeout = timeout
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.session = requests.Session()
    
    def set_auth_token(self, token):
        """Set authorization token for all requests"""
        self.default_headers['Authorization'] = f'Bearer {token}'
    
    def get(self, endpoint, params=None, headers=None):
        """Send GET request to API endpoint"""
        url = f"{self.base_url}/{endpoint}"
        request_headers = {**self.default_headers, **(headers or {})}
        
        try:
            response = self.session.get(
                url,
                params=params,
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def post(self, endpoint, data=None, headers=None):
        """Send POST request with JSON data"""
        url = f"{self.base_url}/{endpoint}"
        request_headers = {**self.default_headers, **(headers or {})}
        
        try:
            response = self.session.post(
                url,
                json=data,
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def put(self, endpoint, data=None, headers=None):
        """Send PUT request to update resource"""
        url = f"{self.base_url}/{endpoint}"
        request_headers = {**self.default_headers, **(headers or {})}
        
        try:
            response = self.session.put(
                url,
                json=data,
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def delete(self, endpoint, headers=None):
        """Send DELETE request to remove resource"""
        url = f"{self.base_url}/{endpoint}"
        request_headers = {**self.default_headers, **(headers or {})}
        
        try:
            response = self.session.delete(
                url,
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json() if response.text else {'success': True}
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def upload_file(self, endpoint, file_path, field_name='file'):
        """Upload a file to the API"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            with open(file_path, 'rb') as f:
                files = {field_name: f}
                response = self.session.post(
                    url,
                    files=files,
                    headers={'Authorization': self.default_headers.get('Authorization', '')},
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def retry_request(self, method, endpoint, max_retries=3, **kwargs):
        """Retry failed requests with exponential backoff"""
        import time
        
        for attempt in range(max_retries):
            result = getattr(self, method)(endpoint, **kwargs)
            
            if 'error' not in result:
                return result
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
        
        return result
