# Consensus API to CSV Exporter

A Python application that calls the Consensus API endpoint and exports demo board tracking data to CSV files.

## Features

- Consensus API client with authentication
- Data processing and transformation
- CSV export capabilities
- Configurable date ranges and paging
- Configuration management via environment variables
- Error handling and logging

## Prerequisites

1. **Python 3.7+**: Download and install from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
   - Verify installation: `python --version`

## Installation

1. Clone or download this repository
2. Open a terminal in the project directory
3. Install dependencies:
   ```bash
   python -m pip install requests pandas python-dotenv
   ```
   Or use the requirements file:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. **Create your environment file**:
   ```bash
   copy .env.example .env
   ```
5. **Configure your API credentials** in the `.env` file:
   - Replace `your_api_key_here` with your actual Consensus API key
   - Replace `your_api_secret_here` with your actual API secret  
   - Replace `your_email@example.com` with your email address
   - Adjust other settings as needed

   ⚠️ **IMPORTANT**: Never commit the `.env` file to version control!

## Running the Application

### Option 1: Command Line
```bash
python main.py
```

### Option 2: VS Code Task
1. Open the project in VS Code
2. Press `Ctrl+Shift+P` to open the command palette
3. Type "Tasks: Run Task" and select it
4. Choose "Run REST API to CSV App"

## Configuration

Update the `.env` file with your Consensus API settings:
- `API_BASE_URL`: The Consensus API endpoint (https://app.goconsensus.com/api/reports/v1.0/trackDemoBoards)
- `API_KEY`: Your API key
- `API_SECRET`: Your API secret
- `API_EMAIL`: Your user email
- `SOURCE_NAME`: Source identifier for the API call
- `START_DATE`: Start date for data retrieval (YYYY-MM-DD format)
- `END_DATE`: End date for data retrieval (YYYY-MM-DD format)
- `PAGE_LIMIT`: Number of records per page (default: 500)
- `PAGE_NUMBER`: Page number to retrieve (default: 1)
- `OUTPUT_DIR`: Directory to save CSV files

## API Details

The application makes **POST** requests to the Consensus API endpoint:
- **URL**: `https://app.goconsensus.com/api/reports/v1.0/trackDemoBoards`
- **Method**: POST
- **Authentication**: API key, secret, and user email in request body
- **Data Format**: JSON request body with auth, paging, and date parameters

## Usage

The application will:
1. Make a POST request to authenticate with the Consensus API using your credentials
2. Request demo board tracking data for the specified date range (01/04/2025 to today)
3. Process the returned data and extract key information
4. Export two CSV files:
   - **Full Data**: Complete processed data with all available fields
   - **Summary**: Focused data with specific columns:
     - Demoboard_ID (senddemoUuid)
     - Demo_IDs (demoUuids)
     - Salesforce_External_AccountId
     - Salesforce_External_OppId
     - View_Time_Seconds
     - Demoboard_View_Date (timeLastView)

## Features

- **Complete Data Retrieval**: Automatically fetches all pages of data from the API
- **Pagination Handling**: No 1000 row limit - retrieves all available data
- **Clean Column Mapping**: Exports only the required columns without unnecessary fields
- **Dual Export**: Both full detailed data and focused summary CSV files

## Output Files

The application generates timestamped CSV files:
- `consensus_full_data_YYYYMMDD_HHMMSS.csv` - Complete data export
- `consensus_summary_YYYYMMDD_HHMMSS.csv` - Summary with mapped columns

## Troubleshooting

### Common Installation Issues:

1. **"pip is not recognized"**:
   Use `python -m pip` instead of `pip`:
   ```bash
   python -m pip install requests pandas python-dotenv
   ```

2. **"ModuleNotFoundError: No module named 'requests'"**:
   Make sure you've installed the dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Python not found**:
   Install Python from [python.org](https://www.python.org/downloads/) and ensure "Add Python to PATH" is checked during installation.

### Running the Application:
- Command line: `python main.py`
- VS Code: Use the "Run REST API to CSV App" task (Ctrl+Shift+P → "Tasks: Run Task")

## Security

🔒 **Important Security Notes:**

- **Never commit API credentials**: The `.env` file is excluded from version control via `.gitignore`
- **Use `.env.example`**: This template file can be safely committed without credentials
- **Environment Variables**: All sensitive data is loaded from environment variables
- **SSL Configuration**: Can be disabled for development but should be enabled in production

### For GitHub Publishing:

1. **Always use `.env.example`** with placeholder values
2. **Verify `.gitignore`** excludes `.env` files
3. **Document credential requirements** in README
4. **Never hardcode credentials** in source code

### Getting API Credentials:

Contact your Consensus administrator to obtain:
- API Key
- API Secret  
- Appropriate user email for API access

## Project Structure

- `main.py` - Main application entry point
- `api_client.py` - REST API client implementation
- `data_processor.py` - Data processing utilities
- `config.py` - Configuration management
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template