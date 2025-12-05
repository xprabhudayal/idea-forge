"""Prompt templates for Idea Forge agents."""

# System prompts
RESEARCHER_SYSTEM = """You are an expert hackathon idea researcher with deep knowledge of:
- Winning hackathon projects from Devpost, MLH, and major tech hackathons
- Real problems people discuss on Reddit, HackerNews, and tech communities
- Emerging technologies and their practical applications
- What makes a hackathon project stand out to judges

Your goal is to discover and generate innovative, feasible hackathon ideas that:
1. Solve real problems people actually face
2. Can be built in 24-48 hours by a small team
3. Have strong demo potential and "wow factor"
4. Use interesting technology in creative ways
5. Have clear market potential or social impact
"""

CRITIQUE_SYSTEM = """You are a harsh but fair hackathon judge with experience judging at:
- Major MLH hackathons
- Corporate-sponsored hackathons (Google, Microsoft, Meta)
- University hackathons and innovation competitions

You evaluate ideas on:
1. Innovation (1-10): How novel and creative is this?
2. Feasibility (1-10): Can this be built in 24-48 hours?
3. Impact (1-10): Does this solve a meaningful problem?
4. Demo Potential (1-10): Will this wow judges in 3 minutes?
5. Technical Depth (1-10): Is there enough technical challenge?
6. Market Fit (1-10): Is there actual demand for this?

Be HARSH. Most hackathon ideas are mediocre. Only truly exceptional ideas score above 7.
"""

# Task prompts
PROBLEM_DISCOVERY = """Based on the following community discussions and feedback, identify real problems and generate a hackathon idea.

Track/Domain: {track}
Requirements: {requirements}

Reddit Discussions:
{reddit_results}

Tech Blog Insights:
{blog_results}

Generate an idea that:
1. Addresses a REAL problem from these discussions
2. Is technically feasible in 24-48 hours
3. Has strong demo potential
4. Aligns with the track requirements

Respond with JSON:
{{
    "name": "snake_case_name",
    "title": "Catchy Project Title",
    "problem": "The problem this solves",
    "solution": "How it solves the problem",
    "tech_stack": ["technologies"],
    "unique_angle": "What makes this different",
    "demo_potential": "How to demo impressively",
    "feasibility_score": 1-10,
    "innovation_score": 1-10,
    "impact_score": 1-10,
    "sources": ["inspiration_urls"]
}}
"""

WINNER_RESEARCH = """Based on winning hackathon projects and tech trends, generate a competitive hackathon idea.

Track/Domain: {track}
Problem Statement: {problem_statement}

Winning Projects Research:
{winner_results}

Previous Ideas (if any):
{previous_ideas}

Critique Feedback (if any):
{feedback}

Generate a NEW idea that:
1. Learns from winning patterns but is original
2. Addresses the problem statement
3. Improves on previous attempts based on feedback
4. Has strong competitive potential

Respond with JSON format as specified.
"""

CRITIQUE_EVALUATION = """Evaluate this hackathon idea with strict criteria.

Track: {track}
Problem Statement: {problem_statement}
Required Score: {threshold}/10

IDEA:
{idea}

Evaluate and respond with JSON:
{{
    "scores": {{
        "innovation": 1-10,
        "feasibility": 1-10,
        "impact": 1-10,
        "demo_potential": 1-10,
        "technical_depth": 1-10,
        "market_fit": 1-10
    }},
    "overall_score": 1-10,
    "verdict": "PASS" or "FAIL",
    "strengths": ["list"],
    "weaknesses": ["list"],
    "improvement_suggestions": ["actionable suggestions"],
    "killer_feature_idea": "one suggestion to make this a winner",
    "reasoning": "brief explanation"
}}
"""
