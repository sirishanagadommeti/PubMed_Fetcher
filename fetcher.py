import requests
from typing import List, Optional
from .utils import is_non_academic
from pydantic import BaseModel

class Paper(BaseModel):
    pubmed_id: str
    title: str
    publication_date: str
    non_academic_authors: List[str]
    company_affiliations: List[str]
    corresponding_email: Optional[str]

def fetch_pubmed_ids(query: str) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 100
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_paper_details(pmid: str) -> Optional[Paper]:
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    response = requests.get(efetch_url, params=params)
    if response.status_code != 200:
        return None

    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.content)
    article = root.find(".//PubmedArticle")
    if article is None:
        return None

    title = article.findtext(".//ArticleTitle", default="")
    date = article.findtext(".//PubDate/Year", default="Unknown")

    authors = article.findall(".//Author")
    non_academic_authors = []
    company_affiliations = []
    corresponding_email = None

    for author in authors:
        affiliation = author.findtext(".//AffiliationInfo/Affiliation")
        name_parts = [
            author.findtext("ForeName", ""),
            author.findtext("LastName", "")
        ]
        full_name = " ".join(name_parts).strip()

        if affiliation and is_non_academic(affiliation):
            non_academic_authors.append(full_name)
            company_affiliations.append(affiliation)

        if affiliation and "@" in affiliation and corresponding_email is None:
            import re
            match = re.search(r"[\w\.-]+@[\w\.-]+", affiliation)
            if match:
                corresponding_email = match.group()

    if not non_academic_authors:
        return None

    return Paper(
        pubmed_id=pmid,
        title=title,
        publication_date=date,
        non_academic_authors=non_academic_authors,
        company_affiliations=company_affiliations,
        corresponding_email=corresponding_email
    )