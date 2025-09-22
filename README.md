# ⚽ Balon D'App 🏆

A web scraping tool that collected all the Balon d'Or nominations data into a single time series dataset, including the full history from 1956 to 2025. Also an animated racing bar chart of total nominations of players during their active periods.

## 🚀 Setup

### 1. 📦 Install UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 🔧 Initialize the Project

Clone the repository and set up the Python environment:

```bash
# Clone the repository
git clone git@github.com:SpoicyCurri/balon-dapp.git
cd balon-dapp

# Create a virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

### 3. ▶️ Running the Application

```bash
# Run the main scraping application
uv run main.py

# Generate bar chart race visualization
uv run visuals/bar_chart_races.py
```

## ✨ Features

### 🕷️ Web Scraping Tool

The web scraping component (`main.py`) is designed to collect Ballon d'Or voting data from Wikipedia across multiple years (1956-2024). It includes:

**Key Components:**
- **🌐 WebScraper**: Handles HTTP requests with proper user-agent headers and error handling
- **📊 TableExtractor**: Parses HTML tables from Wikipedia pages, handling different table structures across years
- **🧹 DataCleaner**: Normalizes and cleans the extracted data, handling inconsistencies in player names and voting formats
- **📅 Year-specific Logic**: Adapts to different Wikipedia page structures for different time periods:
  - 2003-2006: Ballon d'Or with multiple voting tables
  - 2010-2015: FIFA Ballon d'Or era with different table formats
  - Other years: Standard Ballon d'Or format

**Output:** 
- `data/ballon_dor_all_years.csv`: Complete dataset of all Ballon d'Or nominations and voting data
- `data/ballon_dor_voting_details.csv`: Detailed voting information of the years between 2003 and 2006, where additional data was published

### 📊 Bar Chart Race Visualization

The bar chart race tool (`visuals/bar_chart_races.py`) creates an animated visualization showing the cumulative Ballon d'Or nominations for top players over time.

**Features:**
- **⏱️ Animated Timeline**: Shows progression from 1956 to 2024
- **🏆 Top 10 Players**: Displays the most nominated players at each point in time
- **📈 Cumulative Counting**: Tracks total nominations rather than just annual winners
- **👤 Player Disambiguation**: Handles players with same names (e.g. Luis Suárez)
- **🌐 Interactive HTML Output**: Generates a standalone HTML file with the animated chart

**Technical Details:**
- Uses `raceplotly` library for smooth animated transitions
- Output saved as `visuals/outputs/bar_chart_race_output.html`
