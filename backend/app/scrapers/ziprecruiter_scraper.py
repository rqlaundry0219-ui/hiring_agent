"""
ZipRecruiter Scraper Module
============================
Scrape jobs from ZipRecruiter.
"""

import logging
from typing import List, Optional
from datetime import datetime

from .base_scraper import BaseScraper, JobPosting

logger = logging.getLogger(__name__)


class ZipRecruiterScraper(BaseScraper):
    """Scrape jobs from ZipRecruiter"""
    
    def __init__(self):
        super().__init__()
        self.source = "ziprecruiter"
        self.base_url = "https://www.ziprecruiter.com"
        self.api_url = "https://api.ziprecruiter.com/jobs/search"
    
    async def fetch_jobs(self, query: str, location: str = "", **kwargs) -> List[JobPosting]:
        """Fetch jobs from ZipRecruiter."""
        try:
            self.logger.info(f"Fetching jobs from ZipRecruiter for query: {query} in {location}")
            
            # Note: ZipRecruiter does not provide a public API for job searching
            # This is a placeholder implementation for future API integration
            # when/if ZipRecruiter provides official API access
            
            jobs = []
            self.logger.info(f"Found {len(jobs)} jobs from ZipRecruiter")
            return jobs
        
        except Exception as e:
            self.logger.error(f"Error fetching ZipRecruiter jobs: {str(e)}")
            return []
    
    async def _build_search_url(self, query: str, location: str) -> str:
        """Build the ZipRecruiter search URL"""
        query_str = "+".join(query.split())
        location_str = location.replace(",", "%2C").replace(" ", "+") if location else ""
        
        search_url = f"{self.base_url}/Jobs/Search?search={query_str}"
        if location_str:
            search_url += f"&location={location_str}"
        
        return search_url
