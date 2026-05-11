"""
Snagajob Scraper Module
=======================
Scrape jobs from Snagajob.
"""

import logging
from typing import List, Optional
from datetime import datetime

from .base_scraper import BaseScraper, JobPosting

logger = logging.getLogger(__name__)


class SnagajobScraper(BaseScraper):
    """Scrape jobs from Snagajob"""
    
    def __init__(self):
        super().__init__()
        self.source = "snagajob"
        self.base_url = "https://www.snagajob.com"
        self.api_url = "https://api.snagajob.com/jobs/search"
    
    async def fetch_jobs(self, query: str, location: str = "", **kwargs) -> List[JobPosting]:
        """Fetch jobs from Snagajob."""
        try:
            self.logger.info(f"Fetching jobs from Snagajob for query: {query} in {location}")
            
            # Note: Snagajob API integration pending
            # This is a placeholder for future implementation
            
            jobs = []
            self.logger.info(f"Found {len(jobs)} jobs from Snagajob")
            return jobs
        
        except Exception as e:
            self.logger.error(f"Error fetching Snagajob jobs: {str(e)}")
            return []
    
    async def _build_search_url(self, query: str, location: str) -> str:
        """Build the Snagajob search URL"""
        query_str = "+".join(query.split())
        location_str = location.replace(",", "%2C").replace(" ", "+") if location else ""
        
        search_url = f"{self.base_url}/search/jobs/?q={query_str}"
        if location_str:
            search_url += f"&location={location_str}"
        
        return search_url
