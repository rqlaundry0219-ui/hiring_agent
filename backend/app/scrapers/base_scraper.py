"""
Base Scraper Module
===================
Abstract base class and standardized job posting format for all scrapers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import hashlib
import logging

logger = logging.getLogger(__name__)


class JobPosting:
    """Standardized job posting format across all scrapers"""
    
    def __init__(
        self,
        title: str,
        company: str,
        location: str,
        description: str,
        external_url: str,
        external_id: str,
        source: str,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        salary_range: Optional[str] = None,
        job_type: Optional[str] = None,
        experience_level: Optional[str] = None,
        required_skills: Optional[List[str]] = None,
        benefits: Optional[List[str]] = None,
        remote: Optional[bool] = None,
        posted_date: Optional[datetime] = None,
    ):
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.external_url = external_url
        self.external_id = external_id
        self.source = source
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.salary_range = salary_range or self._generate_salary_range()
        self.job_type = job_type
        self.experience_level = experience_level
        self.required_skills = required_skills or []
        self.benefits = benefits or []
        self.remote = remote
        self.posted_date = posted_date or datetime.utcnow()
    
    def _generate_salary_range(self) -> Optional[str]:
        """Generate salary range string from min/max"""
        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,.0f} - ${self.salary_max:,.0f}"
        elif self.salary_min:
            return f"${self.salary_min:,.0f}+"
        elif self.salary_max:
            return f"Up to ${self.salary_max:,.0f}"
        return None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for database storage"""
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "external_url": self.external_url,
            "external_id": self.external_id,
            "source": self.source,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "salary_range": self.salary_range,
            "job_type": self.job_type,
            "experience_level": self.experience_level,
            "required_skills": ",".join(self.required_skills) if self.required_skills else None,
            "benefits": ",".join(self.benefits) if self.benefits else None,
            "remote": self.remote,
            "posted_date": self.posted_date,
        }


class BaseScraper(ABC):
    """Abstract base class for all job scrapers"""
    
    def __init__(self):
        self.source = None
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def fetch_jobs(self, query: str, location: str, **kwargs) -> List[JobPosting]:
        """Fetch jobs from the source."""
        pass
    
    def _generate_external_id(self, url: str) -> str:
        """Generate consistent external ID from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    async def validate_jobs(self, jobs: List[JobPosting]) -> List[JobPosting]:
        """Validate job postings and filter out invalid ones"""
        valid_jobs = []
        for job in jobs:
            if self._is_valid_job(job):
                valid_jobs.append(job)
            else:
                self.logger.warning(f"Invalid job posting: {job.title} at {job.company}")
        return valid_jobs
    
    @staticmethod
    def _is_valid_job(job: JobPosting) -> bool:
        """Check if job posting has required fields"""
        required_fields = ["title", "company", "location", "description", "external_url"]
        return all(getattr(job, field) for field in required_fields)
