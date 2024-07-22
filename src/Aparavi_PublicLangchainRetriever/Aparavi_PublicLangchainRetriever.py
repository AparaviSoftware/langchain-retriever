import requests
import logging

class SemanticSearchRetriever:
    """A class to handle semantic search retrievals from the APARAVI platform."""

    def __init__(self, user_id: str, password: str, server_url: str, port: int):
        
        """Initializes the object and obtains a token from the login to the APARAVI platform."""
        self.server_url = server_url
        self.port       = port
        self.login_url  = f"http://{self.server_url}:{str(self.port)}/server/api/v3/login"
        self.headers    = {"Content-Type": "application/json"}
        self.login_data = {"userId": user_id, "password": password}
        self.logger     = logging.getLogger(__name__)
        self.auth_token = self.login()

    def login(self) -> str:
        """Posts the login request and gets back status including token if successful."""
        
        # post request and return a status code
        response = requests.post(self.login_url, json=self.login_data, headers=self.headers)
        
        if response.status_code == 200:
            
            # check response for token
            json_response = response.json()
            token         = json_response.get("data", {}).get("token")
            
            if token:
                self.logger.info("Token extracted successfully: %s", token)
                return token
            else:
                self.logger.error("Token not found in the response.")
                raise ValueError("Token not found in the response.")
        
        else:
            self.logger.error("Login failed with status code: %s", response.status_code)
            self.logger.error("Response: %s", response.text)
            raise ConnectionError("Login failed")

    def search(self, query: str, store_path: str, limit: int) -> dict:
        """Conducts a semantic search."""
        
        search_url     = f"http://{self.server_url}:{self.port}/server/api/v3/database/vectorSearch"
        search_params  = {"search": query, "storePath": store_path, "limit": limit}
        search_headers = {"Authorization": self.auth_token}
        response       = requests.get(search_url, params=search_params, headers=search_headers)
        
        return response.json()