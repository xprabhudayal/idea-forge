"""Researcher Agent - Stage 1 of the idea generation pipeline."""
import json
from typing import Optional
from agno.agent import Agent

from tools.serper import search_reddit, search_hackathon_winners, search_tech_blogs
from config import get_model_config


RESEARCHER_SYSTEM_PROMPT = """You are an expert hackathon idea researcher. Your job is to discover winning hackathon ideas and real problems people face.

You have access to web search tools to find:
1. Reddit discussions about problems people face
2. Winning hackathon projects from Devpost and other platforms
3. Tech blog posts about innovative solutions

When generating ideas, consider:
- Technical feasibility within 24-48 hours
- Innovation and uniqueness
- Real-world impact and problem-solving
- Demo-ability and wow factor
- Alignment with hackathon track/theme

Always respond with a structured JSON containing:
{
    "name": "short_snake_case_name",
    "title": "Catchy Project Title",
    "problem": "The problem this solves",
    "solution": "How it solves the problem",
    "tech_stack": ["list", "of", "technologies"],
    "unique_angle": "What makes this different",
    "demo_potential": "How to demo this impressively",
    "feasibility_score": 1-10,
    "innovation_score": 1-10,
    "impact_score": 1-10,
    "sources": ["urls", "that", "inspired", "this"]
}
"""

IDEA_GENERATION_PROMPT = """Based on the following search results, generate a compelling hackathon idea.

Track/Domain: {track}
Additional Requirements: {requirements}

Search Results:
{search_results}

Generate a unique, feasible hackathon idea that:
1. Addresses a real problem found in the search results
2. Can be built in 24-48 hours
3. Has strong demo potential
4. Aligns with the track requirements

Respond with the idea in the specified JSON format.
"""

PROBLEM_DISCOVERY_PROMPT = """Based on Reddit discussions and community feedback, identify real problems people face.

Track/Domain: {track}
Additional Requirements: {requirements}

Reddit Discussions:
{reddit_results}

Tech Blog Insights:
{blog_results}

Identify the most pressing problems and generate a hackathon idea that solves one of them.
The idea should be:
1. Solving a REAL problem people actually complain about
2. Technically feasible in a hackathon timeframe
3. Innovative in its approach
4. Demonstrable with a working prototype

Respond with the idea in the specified JSON format.
"""


class ResearcherAgent:
    """Agent responsible for researching and generating hackathon ideas."""
    
    def __init__(self):
        model, model_id = get_model_config()
        self.model_id = model_id
        self.agent = Agent(
            name="Hackathon Researcher",
            model=model,
            instructions=RESEARCHER_SYSTEM_PROMPT,
            markdown=False,
        )
    
    async def search_for_problems(self, track: str, requirements: str = "") -> dict:
        """Search Reddit and blogs for real problems in the given domain."""
        reddit_results = await search_reddit(f"{track} problem frustrating help needed")
        blog_results = await search_tech_blogs(f"{track} challenges solutions")
        
        return {
            "reddit": reddit_results,
            "blogs": blog_results
        }
    
    async def search_for_winners(self, track: str, requirements: str = "") -> dict:
        """Search for winning hackathon projects in the domain."""
        winner_results = await search_hackathon_winners(f"{track} {requirements}")
        blog_results = await search_tech_blogs(f"{track} hackathon project innovative")
        
        return {
            "winners": winner_results,
            "blogs": blog_results
        }
    
    async def generate_idea_independent(self, track: str, requirements: str = "") -> dict:
        """Generate idea based on problem discovery (Independent Mode)."""
        search_results = await self.search_for_problems(track, requirements)
        
        prompt = PROBLEM_DISCOVERY_PROMPT.format(
            track=track,
            requirements=requirements,
            reddit_results=json.dumps(search_results["reddit"], indent=2)[:3000],
            blog_results=json.dumps(search_results["blogs"], indent=2)[:2000]
        )
        
        response = self.agent.run(prompt)
        return self._parse_idea_response(response.content)
    
    async def generate_idea_depth(
        self, 
        track: str, 
        problem_statement: str,
        previous_ideas: list = None,
        feedback: str = None
    ) -> dict:
        """Generate idea based on winning projects research (Depth Mode)."""
        search_results = await self.search_for_winners(track, problem_statement)
        
        prev_ideas_str = ""
        if previous_ideas:
            prev_ideas_str = f"\n\nPrevious ideas that didn't meet threshold:\n{json.dumps(previous_ideas, indent=2)}"
            if feedback:
                prev_ideas_str += f"\n\nCritique feedback: {feedback}"
        
        prompt = IDEA_GENERATION_PROMPT.format(
            track=track,
            requirements=problem_statement + prev_ideas_str,
            search_results=json.dumps(search_results, indent=2)[:4000]
        )
        
        response = self.agent.run(prompt)
        return self._parse_idea_response(response.content)
    
    def _parse_idea_response(self, content: str) -> dict:
        """Parse the JSON response from the agent."""
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        
        # Fallback structure if parsing fails
        return {
            "name": "parsing_error",
            "title": "Error Parsing Response",
            "problem": content[:500],
            "solution": "Please try again",
            "tech_stack": [],
            "unique_angle": "",
            "demo_potential": "",
            "feasibility_score": 0,
            "innovation_score": 0,
            "impact_score": 0,
            "sources": []
        }
