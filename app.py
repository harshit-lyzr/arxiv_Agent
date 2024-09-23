from fastapi import FastAPI, Query
import feedparser
from typing import List

# Initialize FastAPI app
app = FastAPI()


# Function to get trending arXiv papers
def get_trending_arxiv_papers(category="cs.AI", max_results=5):
    # Base URL for arXiv API with the category and sorting options
    base_url = f"http://export.arxiv.org/api/query?search_query=cat:{category}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

    # Parse the feed
    feed = feedparser.parse(base_url)

    papers = []

    for entry in feed.entries:
        paper = {
            'title': entry.title,
            'authors': ', '.join(author.name for author in entry.authors),
            'summary': entry.summary,
            'link': entry.link,
            'published': entry.published
        }
        papers.append(paper)

    return papers


# FastAPI route to fetch trending arXiv papers
@app.get("/trending_arxiv")
def trending_arxiv(
        category: str = Query("cs.AI", description="Category of arXiv papers (e.g., cs.AI for AI in Computer Science)"),
        max_results: int = Query(5, description="Maximum number of papers to fetch")):
    papers = get_trending_arxiv_papers(category=category, max_results=max_results)
    return {"category": category, "papers": papers}

