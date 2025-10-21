import requests
import logging
from typing import Dict, List, Optional
from config import Config

class APIClient:
    """REST API client for making HTTP requests."""
    
    def __init__(self):
        self.base_url = Config.API_BASE_URL
        self.api_key = Config.API_KEY
        self.api_secret = Config.API_SECRET
        self.api_email = Config.API_EMAIL
        self.source_name = Config.SOURCE_NAME
        self.session = requests.Session()
        
        # Set up default headers for POST requests
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'REST-API-CSV-Exporter/1.0'
        })
        
        # Configure SSL verification (set to False if having certificate issues)
        # In production, you should resolve certificate issues rather than disable verification
        self.session.verify = Config.VERIFY_SSL
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[List[Dict]]:
        """
        Make a GET request to the specified endpoint.
        
        Args:
            endpoint: The API endpoint (relative to base URL)
            params: Optional query parameters
            
        Returns:
            JSON response data or None if request failed
        """
        try:
            url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            logging.info(f"Making GET request to: {url}")
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logging.info(f"Successfully retrieved {len(data) if isinstance(data, list) else 1} records")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            return None
        except ValueError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            return None
    
    def get_consensus_data(self, start_date: str, end_date: str, limit: int = 500, page: int = 1) -> Optional[List[Dict]]:
        """
        Make a POST request to the Consensus API with authentication.
        
        Args:
            start_date: Start date for the data query
            end_date: End date for the data query
            limit: Number of records per page (default: 500)
            page: Page number to retrieve (default: 1)
            
        Returns:
            JSON response data or None if request failed
        """
        try:
            # Construct the request body as specified
            request_body = {
                "auth": {
                    "api_key": self.api_key,
                    "api_secret": self.api_secret,
                    "user_email": self.api_email,
                    "source_name": self.source_name
                },
                "paging": {
                    "limit": limit,
                    "page": page,
                    "sortBy": "creationDate",
                    "order": "ASC"
                },
                "start_date": start_date,
                "end_date": end_date
            }
            
            logging.info(f"Making POST request to Consensus API for date range: {start_date} to {end_date}")
            logging.info(f"Requesting page {page} with limit {limit}")
            
            response = self.session.post(self.base_url, json=request_body)
            response.raise_for_status()
            
            data = response.json()
            logging.info(f"Successfully retrieved data from Consensus API")
            
            # Handle the nested response structure
            if isinstance(data, dict) and 'data' in data and 'items' in data['data']:
                items = data['data']['items']
                logging.info(f"Extracted {len(items)} items from API response")
                
                # Check pagination info from the actual API response structure
                if 'paging' in data['data']:
                    paging = data['data']['paging']
                    current_page = paging.get('page', page)
                    count_items = paging.get('countItems', len(items))
                    next_page = paging.get('nextPage', 0)
                    limit = paging.get('limit', 500)
                    
                    logging.info(f"Pagination info: Page {current_page}, Items on page: {count_items}, Next page: {next_page}")
                    
                    if next_page > 0:
                        logging.info(f"More data available on page {next_page}")
                    else:
                        logging.info("No more pages available")
                
                return items
            else:
                logging.warning(f"Unexpected API response structure")
                return data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Consensus API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response status: {e.response.status_code}")
                logging.error(f"Response body: {e.response.text}")
            return None
        except ValueError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            return None
    
    def get_all_consensus_data(self, start_date: str, end_date: str, limit: int = 500) -> Optional[List[Dict]]:
        """
        Fetch all pages of Consensus API data using the API's pagination structure.
        
        Args:
            start_date: Start date for the data query
            end_date: End date for the data query
            limit: Number of records per page (default: 500)
            
        Returns:
            Combined list of all items from all pages, or None if failed
        """
        all_items = []
        page = 1
        
        try:
            while True:
                # Get current page
                response_data = self.get_consensus_data_with_pagination(start_date, end_date, limit, page)
                
                if response_data is None:
                    logging.error(f"Failed to fetch page {page}")
                    break
                
                items = response_data.get('items', [])
                paging = response_data.get('paging', {})
                
                if not items:  # Empty list means no more data
                    logging.info(f"No more data on page {page}")
                    break
                
                all_items.extend(items)
                count_items = paging.get('countItems', len(items))
                next_page = paging.get('nextPage', 0)
                
                logging.info(f"Fetched page {page} with {count_items} items. Total so far: {len(all_items)}")
                
                # Check if there's a next page
                if next_page is None or next_page == 0:
                    logging.info(f"Reached last page. No more pages available.")
                    break
                
                page = next_page
                
                # Safety check to prevent infinite loops
                if page > 100:  # Adjust this limit as needed
                    logging.warning(f"Reached maximum page limit (100). Stopping.")
                    break
            
            logging.info(f"Fetched total of {len(all_items)} items from {page} pages")
            return all_items
            
        except Exception as e:
            logging.error(f"Error fetching all consensus data: {e}")
            return all_items if all_items else None
    
    def get_consensus_data_with_pagination(self, start_date: str, end_date: str, limit: int = 500, page: int = 1) -> Optional[Dict]:
        """
        Get consensus data with full pagination information.
        
        Returns:
            Dictionary containing 'items' and 'paging' information, or None if failed
        """
        try:
            # Construct the request body as specified
            request_body = {
                "auth": {
                    "api_key": self.api_key,
                    "api_secret": self.api_secret,
                    "user_email": self.api_email,
                    "source_name": self.source_name
                },
                "paging": {
                    "limit": limit,
                    "page": page,
                    "sortBy": "creationDate",
                    "order": "ASC"
                },
                "start_date": start_date,
                "end_date": end_date
            }
            
            logging.info(f"Making POST request to Consensus API for date range: {start_date} to {end_date}")
            logging.info(f"Requesting page {page} with limit {limit}")
            
            response = self.session.post(self.base_url, json=request_body)
            response.raise_for_status()
            
            data = response.json()
            
            # Return the full data structure including pagination info
            if isinstance(data, dict) and 'data' in data:
                return data['data']
            else:
                logging.warning(f"Unexpected API response structure")
                return None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Consensus API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response status: {e.response.status_code}")
                logging.error(f"Response body: {e.response.text}")
            return None
        except ValueError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            return None