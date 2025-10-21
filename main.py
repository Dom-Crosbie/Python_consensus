#!/usr/bin/env python3
"""
REST API to CSV Exporter
Main application entry point.
"""

import logging
import sys
from datetime import datetime
from api_client import APIClient
from data_processor import DataProcessor
from config import Config

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

def main():
    """Main application function."""
    setup_logging()
    logging.info("Starting REST API to CSV Exporter for Consensus API")
    
    try:
        # Initialize API client
        client = APIClient()
        
        # Set date range for the API call from configuration
        start_date = Config.START_DATE
        end_date = Config.END_DATE
        page_limit = Config.PAGE_LIMIT
        page_number = Config.PAGE_NUMBER
        
        logging.info(f"Fetching data from {start_date} to {end_date}")
        logging.info(f"Using page limit: {page_limit}, page number: {page_number}")
        
        # Fetch data from Consensus API (all pages)
        data = client.get_all_consensus_data(start_date, end_date, page_limit)
        
        if data is None:
            logging.error("Failed to fetch data from Consensus API")
            sys.exit(1)
        
        # Process the data
        processor = DataProcessor()
        df = processor.process_data(data)
        
        if df.empty:
            logging.warning("No data to export")
            sys.exit(0)
        
        # Display data summary
        summary = processor.get_data_summary(df)
        logging.info(f"Full data summary: {summary}")
        
        # Create summary CSV with specific columns
        summary_df = processor.create_summary_csv(df)
        
        # Export both full data and summary
        full_data_filename = f"consensus_full_data_{datetime.now().strftime('%Y%m%d')}.csv"
        summary_filename = f"consensus_summary_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Export full data
        full_success = processor.export_to_csv(df, full_data_filename)
        
        # Export summary
        summary_success = processor.export_to_csv(summary_df, summary_filename)
        
        if full_success and summary_success:
            logging.info("Application completed successfully")
            logging.info(f"Full data exported to: {Config.OUTPUT_DIR}/{full_data_filename}")
            logging.info(f"Summary data exported to: {Config.OUTPUT_DIR}/{summary_filename}")
        else:
            logging.error("Failed to export data")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()