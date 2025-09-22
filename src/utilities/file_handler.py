import pandas as pd
import logging

logger = logging.getLogger(__name__)

def save_dataframe(df: pd.DataFrame, filename: str, format: str = 'csv') -> bool:
    """
    Save DataFrame to file
    
    Args:
        df: pandas DataFrame
        filename: Output filename
        format: File format ('csv', 'json', 'excel')
        
    Returns:
        True if successful, False otherwise
    """
    try:
        filename = filename.format(ext=format.lower())
        if format.lower() == 'csv':
            df.to_csv(filename, index=False)
        elif format.lower() == 'json':
            df.to_json(filename, orient='records', indent=2)
        elif format.lower() in ['excel', 'xlsx']:
            df.to_excel(filename, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Data saved to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return False