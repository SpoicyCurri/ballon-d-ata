from typing import List
from bs4 import Tag

class TableExtractor:
    def __init__(self, config):
        self.config = config
        
    def extract_headers(self, table: Tag, multiple_headers: bool = False) -> List[str]:
        if multiple_headers:
            return self._extract_multiple_headers(table)
        return self._extract_single_header(table)
    
    def extract_rows(self, table: Tag, year: int, headers: List[str], 
                    multiple_headers: bool = False) -> List[List[str]]:
        rows = []
        start_index = 1 if not multiple_headers else 2
        for tr in table.find_all('tr')[start_index:]:
            row = []
            for td in tr.find_all(['td', 'th']):
                # Use get_text with separator to preserve line breaks
                text = td.get_text(separator="~~~", strip=True)
                row.append(text)
            # Special handling for 2025 table structure
            if year != 2025:
                if len(headers) > 0 and len(row) < len(headers):
                    row.insert(0, "MISSING_RANK")
        
            if row:  # Only add non-empty rows
                rows.append(row)
    
        return rows
    
    def _extract_multiple_headers(self, table: Tag) -> List[str]:
        header_rows = table.find_all('tr')[:2]
        first_row = header_rows[0]
        second_row = header_rows[1] if len(header_rows) > 1 else None

        # Get all cells from first row with their colspan info
        first_row_cells = []
        for th in first_row.find_all(['th', 'td']):
            colspan = int(th.get('colspan', 1))
            text = th.get_text().strip()
            first_row_cells.append((text, colspan))

        # Get all cells from second row
        second_row_cells = []
        if second_row:
            for th in second_row.find_all(['th', 'td']):
                second_row_cells.append(th.get_text().strip())

        # Build final headers
        headers = []
        second_row_index = 0

        for text, colspan in first_row_cells:
            if colspan == 1:
                # Single column header - use first row text
                headers.append(text)
            else:
                # Multi-column header - use second row texts for sub-columns
                for i in range(colspan):
                    if second_row_index < len(second_row_cells):
                        headers.append(second_row_cells[second_row_index])
                        second_row_index += 1
                    else:
                        headers.append(f"{text}_{i+1}")  # Fallback if second row is missing
        return headers
    
    def _extract_single_header(self, table: Tag) -> List[str]:
        headers = []
        header_row = table.find('tr')
        if header_row:
            for th in header_row.find_all(['th', 'td']):
                headers.append(th.get_text().strip())
        return headers