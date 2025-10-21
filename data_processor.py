import pandas as pd
import logging
from typing import List, Dict, Optional
from datetime import datetime
from config import Config

class DataProcessor:
    """Data processing utilities for transforming Consensus API data."""
    
    @staticmethod
    def process_data(data: List[Dict]) -> pd.DataFrame:
        """
        Process raw Consensus API data into a pandas DataFrame with specific columns.
        
        Args:
            data: List of dictionaries from API response
            
        Returns:
            Processed pandas DataFrame with mapped columns
        """
        try:
            if not data:
                logging.warning("No data to process")
                return pd.DataFrame()
            
            # Extract and flatten the data according to requirements
            processed_records = []
            
            for record in data:
                # Extract basic demoboard information
                demoboard_info = {
                    'senddemoUuid': record.get('senddemoUuid', ''),
                    'demoboardName': record.get('demoboardName', ''),
                    'organization': record.get('organization', ''),
                    'viewTime': record.get('viewTime', 0),
                    'timeLastView': record.get('timeLastView', ''),
                }
                
                # Extract external opportunity data
                ext_opp = record.get('externalOpportunity', {})
                demoboard_info.update({
                    'externalAccountId': ext_opp.get('externalAccountId', ''),
                    'externalOpportunityId': ext_opp.get('externalOpportunityId', ''),
                    'externalAccountName': ext_opp.get('externalAccountName', ''),
                    'externalOpportunityName': ext_opp.get('externalOpportunityName', '')
                })
                
                # Extract demo UUIDs and create separate rows for each
                demo_uuids = record.get('demoUuids', [])
                if demo_uuids:
                    # Create a row for each demoUuid
                    for i, demo_uuid in enumerate(demo_uuids):
                        demo_record = demoboard_info.copy()
                        if i == 0:
                            # First row keeps the senddemoUuid
                            demo_record['demoUuids'] = demo_uuid
                        else:
                            # Subsequent rows have empty senddemoUuid
                            demo_record['senddemoUuid'] = ''
                            demo_record['demoUuids'] = demo_uuid
                        processed_records.append(demo_record)
                else:
                    # If no demoUuids, use the main demoUuid if available
                    demoboard_info['demoUuids'] = record.get('demoUuid', '')
                    processed_records.append(demoboard_info.copy())
            
            # Convert to DataFrame
            df = pd.DataFrame(processed_records)
            
            # Clean and format the data
            df = DataProcessor._clean_consensus_data(df)
            
            logging.info(f"Processed {len(df)} rows and {len(df.columns)} columns from Consensus API")
            return df
            
        except Exception as e:
            logging.error(f"Error processing Consensus API data: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def _clean_consensus_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the Consensus DataFrame by handling data formatting.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Convert string representations of None/null to empty strings
        df = df.replace(['null', 'None', None], '')
        
        # Strip whitespace from string columns and replace 'nan' with empty strings
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace('nan', '')
        
        # Convert numeric columns
        numeric_columns = ['viewTime']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    @staticmethod
    def create_summary_csv(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a summary CSV with the specific columns requested.
        
        Args:
            df: Full processed DataFrame
            
        Returns:
            Summary DataFrame with specific columns
        """
        try:
            if df.empty:
                return pd.DataFrame()
            
            # Create summary with requested columns
            summary_columns = [
                'senddemoUuid',
                'demoUuids',
                'externalAccountId',
                'externalOpportunityId',
                'viewTime',
                'timeLastView'
            ]
            
            # Select only the columns that exist in the DataFrame
            available_columns = [col for col in summary_columns if col in df.columns]
            
            if not available_columns:
                logging.warning("None of the requested summary columns are available")
                return df
            
            summary_df = df[available_columns].copy()
            
            # Don't remove duplicates since we want separate rows for each demoUuid
            # summary_df = summary_df.drop_duplicates(subset=['senddemoUuid'], keep='first')
            
            # Rename columns to match requirements
            column_mapping = {
                'senddemoUuid': 'Demoboard_ID',
                'demoUuids': 'Demo_IDs',
                'externalAccountId': 'Salesforce_External_AccountId',
                'externalOpportunityId': 'Salesforce_External_OppId',
                'viewTime': 'View_Time_Seconds',
                'timeLastView': 'Demoboard_View_Date'
            }
            
            summary_df = summary_df.rename(columns=column_mapping)
            
            logging.info(f"Created summary with {len(summary_df)} unique demoboards")
            return summary_df
            
        except Exception as e:
            logging.error(f"Error creating summary CSV: {e}")
            return df
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: Optional[str] = None) -> bool:
        """
        Export DataFrame to CSV file.
        
        Args:
            df: DataFrame to export
            filename: Optional custom filename
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            Config.ensure_output_dir()
            
            if filename:
                output_path = f"{Config.OUTPUT_DIR}/{filename}"
            else:
                output_path = Config.get_output_path()
            
            df.to_csv(output_path, index=False, encoding='utf-8')
            logging.info(f"Data exported successfully to: {output_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error exporting to CSV: {e}")
            return False
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict:
        """
        Get a summary of the DataFrame.
        
        Args:
            df: DataFrame to summarize
            
        Returns:
            Dictionary containing summary information
        """
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'null_counts': df.isnull().sum().to_dict()
        }