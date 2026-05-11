"""
Scraper module exports
=====================
Centralized exports for all job scrapers and related classes.
"""

from .base_scraper import BaseScraper, JobPosting
from .indeed_scraper import IndeedScraper
from .ziprecruiter_scraper import ZipRecruiterScraper
from .snagajob_scraper import SnagajobScraper
from .glassdoor_scraper import GlassdoorScraper

__all__ = [
    "BaseScraper",
    "JobPosting",
    "IndeedScraper",
    "ZipRecruiterScraper",
    "SnagajobScraper",
    "GlassdoorScraper",
]
