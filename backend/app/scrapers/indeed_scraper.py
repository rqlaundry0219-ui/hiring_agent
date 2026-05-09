"""
Indeed Scraper Module
======================
Scrape jobs from Indeed using RSS feeds and HTML parsing.
"""

import feedparser
import re
import hashlib
import logging
from typing import List, Optional
from datetime import datetime

from .base_scraper import BaseScraper, JobPosting

logger = logging.getLogger(__name__)


class IndeedScraper(BaseScraper):
    """Scrape jobs from Indeed using RSS feeds and HTML parsing"""
    
    def __init__(self):
        super().__init__()
        self.source = "indeed"
        self.base_url = "https://www.indeed.com"
        self.rss_base_url = "https://www.indeed.com/rss"
    
    async def fetch_jobs(self, query: str, location: str = "", **kwargs) -> List[JobPosting]:
        """Fetch jobs from Indeed using RSS feed."""
        try:
            rss_url = await self._build_rss_url(query, location)
            self.logger.info(f"Fetching from Indeed RSS: {rss_url}")
            
            feed = feedparser.parse(rss_url)
            jobs = []
            
            for entry in feed.entries:
                job = self._parse_rss_entry(entry)
                if job:
                    jobs.append(job)
            
            self.logger.info(f"Found {len(jobs)} jobs from Indeed")
            return await self.validate_jobs(jobs)
        
        except Exception as e:
            self.logger.error(f"Error fetching Indeed jobs: {str(e)}")
            return []
    
    async def _build_rss_url(self, query: str, location: str) -> str:
        """Build the Indeed RSS feed URL"""
        query_str = "+".join(query.split())
        location_str = location.replace(",", "%2C").replace(" ", "+") if location else ""
        
        rss_url = f"{self.rss_base_url}?q={query_str}"
        if location_str:
            rss_url += f"&l={location_str}"
        
        return rss_url
    
    def _parse_rss_entry(self, entry) -> Optional[JobPosting]:
        """Parse a single RSS entry into JobPosting"""
        try:
            from bs4 import BeautifulSoup
            
            title = entry.get("title", "").strip()
            summary = entry.get("summary", "")
            soup = BeautifulSoup(summary, "html.parser")
            
            lines = [line.strip() for line in soup.get_text().split("\n") if line.strip()]
            
            company = lines[0] if len(lines) > 0 else "Unknown"
            location = lines[1] if len(lines) > 1 else "Unknown"
            description = "\n".join(lines[2:]) if len(lines) > 2 else summary
            
            external_url = entry.get("link", "")
            if not external_url:
                return None
            
            external_id = self._extract_job_id_from_url(external_url)
            published = entry.get("published", "")
            posted_date = self._parse_date(published)
            salary_info = self._extract_salary(description)
            
            return JobPosting(
                title=title,
                company=company,
                location=location,
                description=description,
                external_url=external_url,
                external_id=external_id,
                source=self.source,
                salary_min=salary_info.get("min"),
                salary_max=salary_info.get("max"),
                salary_range=salary_info.get("range"),
                posted_date=posted_date,
                job_type=self._infer_job_type(description),
            )
        
        except Exception as e:
            logger.warning(f"Error parsing Indeed RSS entry: {str(e)}")
            return None
    
    @staticmethod
    def _extract_job_id_from_url(url: str) -> str:
        """Extract job ID from Indeed URL"""
        try:
            if "jk=" in url:
                return url.split("jk=")[1].split("&")[0]
            return hashlib.md5(url.encode()).hexdigest()
        except:
            return hashlib.md5(url.encode()).hexdigest()
    
    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Parse ISO format date from Indeed RSS"""
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except:
            return datetime.utcnow()
    
    @staticmethod
    def _extract_salary(text: str) -> dict:
        """Extract salary information from job description"""
        salary_pattern = r"\$[\d,]+\s*-\s*\$[\d,]+"
        match = re.search(salary_pattern, text)
        
        if match:
            salary_range = match.group()
            parts = salary_range.split("-")
            try:
                salary_min = int(parts[0].replace("$", "").replace(",", ""))
                salary_max = int(parts[1].replace("$", "").replace(",", ""))
                return {
                    "min": salary_min,
                    "max": salary_max,
                    "range": salary_range.strip()
                }
            except:
                return {"range": salary_range.strip()}
        
        return {}
    
    @staticmethod
    def _infer_job_type(description: str) -> str:
        """Infer job type from description"""
        description_lower = description.lower()
        if "full-time" in description_lower or "full time" in description_lower:
            return "full-time"
        elif "part-time" in description_lower or "part time" in description_lower:
            return "part-time"
        elif "contract" in description_lower:
            return "contract"
        elif "hourly" in description_lower:
            return "hourly"
        return "full-time"
