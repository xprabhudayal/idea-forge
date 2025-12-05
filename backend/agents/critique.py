"""Critique Agent - Stage 2 of the idea validation pipeline."""
import json
from agno.agent import Agent
from agno.models.openai import OpenAIChat


CRITIQUE_SYSTEM_PROMPT = """You are a harsh but fair hackathon judge and idea critic. Your job is to evaluate hackathon ideas with strict criteria.

You evaluate ideas on these dimensions (each 1-10):
1. **Innovation** - How novel and creative is this idea?
2. **Feasibility** - Can this realistically be built in 24-48 hours?
3. **Impact** - Does this solve a real, meaningful problem?
4. **Demo Potential** - Will this wow judges in a 3-minute demo?
5. **Technical Depth** - Is there enough technical challenge to impress?
6. **Market Fit** - Is there actual demand for this solution?

Be HARSH. Most hackathon ideas are mediocre. Only truly exceptional ideas should score above 7.

Scoring Guidelines:
- 1-3: Poor idea, fundamental flaws
- 4-5: Below average, needs major rework
- 6: Average, could work but not a winner
- 7: Good, has potential to place
- 8: Very good, strong contender for top 3
- 9: Excellent, likely winner material
- 10: Exceptional, award-worthy innovation

Always respond with structured JSON:
{
    "scores": {
        "innovation": 1-10,
        "feasibility": 1-10,
        "impact": 1-10,
        "demo_potential": 1-10,
        "technical_depth": 1-10,
        "market_fit": 1-10
    },
    "overall_score": 1-10 (weighted average),
    "verdict": "PASS" or "FAIL",
    "strengths": ["list", "of", "strengths"],
    "weaknesses": ["list", "of", "weaknesses"],
    "improvement_suggestions": ["specific", "actionable", "suggestions"],
    "killer_feature_idea": "One suggestion to make this a winner",
    "reasoning": "Brief explanation of the verdict"
}
"""

CRITIQUE_PROMPT = """Evaluate this hackathon idea with your strict criteria.

Track/Domain: {track}
Problem Statement: {problem_statement}
Threshold Required: {threshold}% (score of {threshold_score}/10 needed to pass)

IDEA TO EVALUATE:
{idea}

Be harsh but constructive. This idea needs to score at least {threshold_score}/10 overall to pass.
If it doesn't meet the threshold, provide specific feedback on how to improve it.

Respond with your evaluation in the specified JSON format.
"""


class CritiqueAgent:
    """Agent responsible for critiquing and scoring hackathon ideas."""
    
    def __init__(self, model_id: str = "gpt-4o"):
        self.agent = Agent(
            name="Hackathon Critique",
            model=OpenAIChat(id=model_id),
            instructions=CRITIQUE_SYSTEM_PROMPT,
            markdown=False,
        )
    
    def evaluate_idea(
        self,
        idea: dict,
        track: str,
        problem_statement: str,
        threshold: int = 7  # 1-9 slider maps to 10-90%, so 7 = 70% = 7/10
    ) -> dict:
        """
        Evaluate an idea against the threshold.
        
        Args:
            idea: The idea dictionary from ResearcherAgent
            track: Hackathon track/domain
            problem_statement: Original problem statement
            threshold: Score threshold (1-9, representing 10-90%)
        
        Returns:
            Evaluation result with scores and verdict
        """
        threshold_score = threshold  # Direct mapping: slider 7 = need 7/10
        threshold_percent = threshold * 10
        
        prompt = CRITIQUE_PROMPT.format(
            track=track,
            problem_statement=problem_statement,
            threshold=threshold_percent,
            threshold_score=threshold_score,
            idea=json.dumps(idea, indent=2)
        )
        
        response = self.agent.run(prompt)
        evaluation = self._parse_evaluation(response.content, threshold_score)
        
        return evaluation
    
    def _parse_evaluation(self, content: str, threshold_score: int) -> dict:
        """Parse the evaluation response."""
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                evaluation = json.loads(json_match.group())
                # Ensure verdict is based on threshold
                if evaluation.get("overall_score", 0) >= threshold_score:
                    evaluation["verdict"] = "PASS"
                else:
                    evaluation["verdict"] = "FAIL"
                return evaluation
        except json.JSONDecodeError:
            pass
        
        # Fallback
        return {
            "scores": {
                "innovation": 0,
                "feasibility": 0,
                "impact": 0,
                "demo_potential": 0,
                "technical_depth": 0,
                "market_fit": 0
            },
            "overall_score": 0,
            "verdict": "FAIL",
            "strengths": [],
            "weaknesses": ["Failed to parse evaluation"],
            "improvement_suggestions": ["Please try again"],
            "killer_feature_idea": "",
            "reasoning": content[:500]
        }
    
    def get_improvement_feedback(self, evaluation: dict) -> str:
        """Extract actionable feedback for the researcher to improve."""
        feedback_parts = []
        
        if evaluation.get("weaknesses"):
            feedback_parts.append(f"Weaknesses to address: {', '.join(evaluation['weaknesses'])}")
        
        if evaluation.get("improvement_suggestions"):
            feedback_parts.append(f"Suggestions: {', '.join(evaluation['improvement_suggestions'])}")
        
        if evaluation.get("killer_feature_idea"):
            feedback_parts.append(f"Killer feature idea: {evaluation['killer_feature_idea']}")
        
        # Identify lowest scoring dimensions
        scores = evaluation.get("scores", {})
        if scores:
            sorted_scores = sorted(scores.items(), key=lambda x: x[1])
            weakest = sorted_scores[:2]
            feedback_parts.append(f"Focus on improving: {', '.join([f'{k} (scored {v})' for k, v in weakest])}")
        
        return " | ".join(feedback_parts)
