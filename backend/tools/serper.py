"""Serper API tool for web search."""
import os
import httpx
from typing import Optional

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


async def search_web(
    query: str,
    num_results: int = 10,
    search_type: str = "search"
) -> dict:
    """
    Search the web using Serper API.
    
    Args:
        query: Search query string
        num_results: Number of results to return
        search_type: Type of search (search, news, images)
    
    Returns:
        Search results as dictionary
    """
    if not SERPER_API_KEY:
        raise ValueError("SERPER_API_KEY environment variable not set")
    
    url = f"https://google.serper.dev/{search_type}"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": num_results
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()


async def search_reddit(query: str, num_results: int = 10) -> dict:
    """Search Reddit specifically for problems and discussions."""
    reddit_query = f"site:reddit.com {query}"
    return await search_web(reddit_query, num_results)


async def search_hackathon_winners(query: str, num_results: int = 10) -> dict:
    """Search for hackathon winning projects."""
    winner_query = f"{query} hackathon winner project devpost"
    return await search_web(winner_query, num_results)


async def search_tech_blogs(query: str, num_results: int = 10) -> dict:
    """Search tech blogs and social media for ideas."""
    blog_query = f"{query} (site:medium.com OR site:dev.to OR site:hackernoon.com OR site:twitter.com)"
    return await search_web(blog_query, num_results)
