# Ekantipur Scraper 📰

A Playwright-based Python scraper for [ekantipur.com](https://ekantipur.com) that extracts the latest **entertainment news** and the **cartoon of the day**.

## ✨ Features
- Skips the advertisement overlay automatically.
- Extracts top 5 entertainment articles:
  - Title (headline)
  - Image URL (thumbnail)
  - Category (e.g., "मनोरञ्जन")
  - Author name (in Nepali, if available)
- Extracts cartoon of the day:
  - Title
  - Image URL
  - Author (fallback to `"Unknown"` if missing)
- Cleans titles by removing trailing `MINS READ`.
- Saves results in `output.json` with UTF‑8 encoding.

## 📂 Project Structure
ekantipur-scraper/
│
├── scraper.py        # Main Playwright script
├── prompt.txt        # Log of all prompts and selector changes
├── output.json       # Generated JSON output
├── README.md         # Project documentation
└── .gitignore        # Ignore venv, cache, logs


## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Playwright installed

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/ekantipur-scraper.git
cd ekantipur-scraper

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install playwright
playwright install
