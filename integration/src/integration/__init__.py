"""Integration package for Gmail client and AI client.

This package provides functionality to integrate the Gmail client with an AI client
for email analysis and spam detection.
"""

from .integration import analyze_emails_for_spam, write_results_to_csv

__all__ = ["analyze_emails_for_spam", "write_results_to_csv"]
