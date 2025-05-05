import os
from dotenv import load_dotenv

# Get configuration from environment variables
load_dotenv()

MAX_EMAILS = int(os.getenv("MAX_EMAILS_TO_ANALYZE", "10"))
DEFAULT_OUTPUT_PATH = os.getenv("OUTPUT_CSV_PATH", "spam_analysis_results.csv")