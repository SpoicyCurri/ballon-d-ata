from typing import List, Optional
from src.config import ScrapingConfig
from src.web_scraper import WebScraper
from src.table_extractor import TableExtractor
from src.data_cleaner import DataCleaner
from src.utilities.logger import setup_logger
from src.utilities.file_handler import save_dataframe
import pandas as pd

class BallonDorScraper:
    def __init__(self):
        self.config = ScrapingConfig()
        self.logger = setup_logger(__name__)
        self.web_scraper = WebScraper(self.config.USER_AGENT)
        self.table_extractor = TableExtractor(self.config)
        self.data_cleaner = DataCleaner(
            self.config.PATTERNS, 
            self.config.COLUMN_MAPPINGS
        )
        
    def _get_year_config(self, year: int) -> List[tuple]:
        """Get URL and settings for a specific year - returns list of configurations"""
        configurations = []
        
        if 2003 <= year < 2007:
            # Get both table index 0 and 1 for these years
            base_url = self.config.BASE_URL_BALLON.format(year=year)
            configurations.append((base_url, 0, True))
            configurations.append((base_url, 1, True))
        elif 2010 <= year < 2016:
            # Get both table index 0 and 1 for these years  
            base_url = self.config.BASE_URL_FIFA.format(year=year)
            configurations.append((base_url, 0, False))
            configurations.append((base_url, 1, False))
        else:
            # Default case - just table index 0
            base_url = self.config.BASE_URL_BALLON.format(year=year)
            configurations.append((base_url, 0, False))
        
        return configurations

    def generate_url_configurations(self) -> List[tuple]:
        """Generate list of (year, url, table_index, multiple_headers) tuples"""
        configurations = []

        for year in range(self.config.START_YEAR, self.config.END_YEAR + 1):
            if year in self.config.SKIP_YEARS:
                continue
                
            year_configs = self._get_year_config(year)
            for url, table_index, multiple_headers in year_configs:
                configurations.append((year, url, table_index, multiple_headers))
            
        return configurations
    
    def scrape_year(self, year: int, url: str, table_index: int, 
                   multiple_headers: bool) -> Optional[pd.DataFrame]:
        """Scrape data for a single year"""
        try:
            soup = self.web_scraper.fetch_page(url)
            if not soup:
                return None
                
            tables = soup.find_all('table', class_='wikitable')
            if len(tables) <= table_index:
                self.logger.warning(f"Not enough tables for year {year}")
                return None
                
            headers = self.table_extractor.extract_headers(
                tables[table_index], multiple_headers
            )
            rows = self.table_extractor.extract_rows(
                tables[table_index], year, headers, multiple_headers
            )
            
            if not headers or not rows:
                return None
                
            df = pd.DataFrame(rows, columns=headers)
            df["year"] = year
            
            return self.data_cleaner.clean_dataframe(df, year)
            
        except Exception as e:
            self.logger.error(f"Error scraping year {year}: {e}")
            return None

    def _save_results(self, regular_data: pd.DataFrame, multi_header_data: pd.DataFrame):
        if not multi_header_data.empty:
            multi_header_data = self.data_cleaner.clean_multi_year_data(multi_header_data)
            multi_header_data = self.data_cleaner.calculate_percentage(multi_header_data)
            save_dataframe(multi_header_data, self.config.OUTPUT_FILE_MULTI, self.config.OUTPUT_FORMAT)

        if not regular_data.empty:
            regular_data = pd.concat([regular_data, multi_header_data], ignore_index=True)
            regular_data = regular_data.drop(columns=["1st", "2nd", "3rd", "4th", "5th", "votes"])
            regular_data = regular_data.sort_values(by=["year", "rank", "player"], ascending=[False, True, True])
            regular_data = regular_data[["year", "rank", "player", "club", "nationality", "points", "percent", "position"]]
            regular_data = self.data_cleaner.calculate_percentage(regular_data)
            save_dataframe(regular_data, self.config.OUTPUT_FILE_REGULAR, self.config.OUTPUT_FORMAT)
        

    def run(self):
        """Main execution method"""
        configurations = self.generate_url_configurations()
        
        regular_data = pd.DataFrame()
        multi_header_data = pd.DataFrame()
        
        for year, url, table_index, multiple_headers in configurations:
            self.logger.info(f"Scraping data for year {year}")
            
            df = self.scrape_year(year, url, table_index, multiple_headers)
            if df is not None:
                if multiple_headers:
                    multi_header_data = pd.concat([multi_header_data, df], ignore_index=True)
                else:
                    regular_data = pd.concat([regular_data, df], ignore_index=True)
        
        # Process and save data
        self._save_results(regular_data, multi_header_data)

if __name__ == "__main__":
    scraper = BallonDorScraper()
    scraper.run()
