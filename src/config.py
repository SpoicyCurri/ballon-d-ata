from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class ScrapingConfig:
    BASE_URL_BALLON: str = "https://en.wikipedia.org/wiki/{year}_Ballon_d%27Or"
    BASE_URL_FIFA: str = "https://en.wikipedia.org/wiki/{year}_FIFA_Ballon_d%27Or"
    
    USER_AGENT: str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    OUTPUT_FILE_MULTI: str = "data/ballon_dor_voting_details.{ext}"
    OUTPUT_FILE_REGULAR: str = "data/ballon_dor_all_years.{ext}"
    OUTPUT_FORMAT: str = "csv"  # Options: 'csv', 'json', 'xlsx'

    # Year ranges and their configurations
    START_YEAR: int = 1956
    END_YEAR: int = 2025
    SKIP_YEARS: List[int] = field(default_factory=lambda: [2020])
    
    # Regex patterns
    PATTERNS: Dict[str, str] = field(default_factory=lambda: {
        'reference_notes': r'~~~\[~~~[0-9a-zA-Z\s]*~~~\]',
        'points_cleanup': r'(\d)\s*\[\d+\]$',
        'rank_ordinal': r'(\d+)[a-zA-Z]{2}$'
    })
    
    # Column mappings
    COLUMN_MAPPINGS: Dict[str, str] = field(default_factory=lambda: {
        "club(s)": "club",
        "national team": "nationality", 
        "votes": "points",
        "name": "player",
    })
    
    # Year ranges for multi-header tables
    MULTI_HEADER_YEARS: List[tuple] = field(default_factory=lambda: [(2003, 2006), (2010, 2015)])