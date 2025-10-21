import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the REST API to CSV application."""
    
    # API Configuration
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://app.goconsensus.com/api/reports/v1.0/trackDemoBoards')
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    API_EMAIL = os.getenv('API_EMAIL')
    SOURCE_NAME = os.getenv('SOURCE_NAME', 'pythonapp')
    
    # SSL Configuration
    VERIFY_SSL = os.getenv('VERIFY_SSL', 'true').lower() == 'true'
    
    # Date Range Configuration
    START_DATE = os.getenv('START_DATE', '2025-04-01')
    END_DATE = os.getenv('END_DATE', '2025-10-21')
    
    # Paging Configuration
    PAGE_LIMIT = int(os.getenv('PAGE_LIMIT', '500'))
    PAGE_NUMBER = int(os.getenv('PAGE_NUMBER', '1'))
    
    # Output Configuration
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
    OUTPUT_FILENAME = os.getenv('OUTPUT_FILENAME', 'api_data.csv')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_output_path(cls):
        """Get the full output file path."""
        return os.path.join(cls.OUTPUT_DIR, cls.OUTPUT_FILENAME)
    
    @classmethod
    def ensure_output_dir(cls):
        """Ensure the output directory exists."""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)