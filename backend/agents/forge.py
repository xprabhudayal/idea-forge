"""IdeaForge - Main orchestrator for the two-stage idea generation system."""
import asyncio
from typing import Optional, Callable, AsyncGenerator
from dataclasses import dataclass, field
from enum import Enum

from .researcher import ResearcherAgent
from .critique import CritiqueAgent


class ForgeMode(Enum):
    INDEPENDENT = "independent"
    DEPTH = "depth"


@dataclass
class ForgeState:
    """State tracking for the forge process."""
    mode: ForgeMode
    track: str
    problem_statement: str = ""
    threshold: int = 7
    max_iterations: int = 10
    current_iteration: int = 0
    ideas_generated: list = field(default_factory=list)
    evaluations: list = field(default_factory=list)
    is_running: bool = False
    is_interrupted: bool = False
    final_idea: Optional[dict] = None
    final_evaluation: Optional[dict] = None


@dataclass
class ForgeUpdate:
    """Update message from the forge process."""
    iteration: int
    stage: str  # "researching", "evaluating", "complete", "interrupted"
    idea: Optional[dict] = None
    evaluation: Optional[dict] = None
    message: str = ""


class IdeaForge:
    """
    Main orchestrator that implements the two-stage idea generation pipeline.
    
    Independent Mode:
        - Searches Reddit for problems
        - Generates a single idea based on real user pain points
    
    Depth Mode:
        - Stage 1: Researcher searches for winning ideas
        - Stage 2: Critique evaluates and scores
        - Iterates until threshold met or interrupted
    """
    
    def __init__(self, model_id: str = "gpt-4o"):
        self.researcher = ResearcherAgent(model_id)
        self.critique = CritiqueAgent(model_id)
        self.state: Optional[ForgeState] = None
    
    async def run_independent(
        self,
        track: str,
        requirements: str = ""
    ) -> dict:
        """
        Run Independent Mode - single idea generation from problem discovery.
        
        Args:
            track: Hackathon track/domain
            requirements: Additional requirements
        
        Returns:
            Generated idea dictionary
        """
        self.state = ForgeState(
            mode=ForgeMode.INDEPENDENT,
            track=track,
            problem_statement=requirements,
            is_running=True
        )
        
        try:
            idea = await self.researcher.generate_idea_independent(track, requirements)
            self.state.final_idea = idea
            self.state.ideas_generated.append(idea)
            return {
                "success": True,
                "idea": idea,
                "mode": "independent"
            }
        finally:
            self.state.is_running = False
    
    async def run_depth(
        self,
        track: str,
        problem_statement: str,
        threshold: int = 7,
        max_iterations: int = 10,
        on_update: Optional[Callable[[ForgeUpdate], None]] = None
    ) -> AsyncGenerator[ForgeUpdate, None]:
        """
        Run Depth Mode - iterative idea generation with critique validation.
        
        Args:
            track: Hackathon track/domain
            problem_statement: The problem statement to solve
            threshold: Score threshold (1-9, maps to 10-90%)
            max_iterations: Maximum iterations before stopping
            on_update: Optional callback for updates
        
        Yields:
            ForgeUpdate objects with progress information
        """
        self.state = ForgeState(
            mode=ForgeMode.DEPTH,
            track=track,
            problem_statement=problem_statement,
            threshold=threshold,
            max_iterations=max_iterations,
            is_running=True
        )
        
        feedback = None
        
        try:
            for iteration in range(1, max_iterations + 1):
                if self.state.is_interrupted:
                    yield ForgeUpdate(
                        iteration=iteration,
                        stage="interrupted",
                        message="Process interrupted by user"
                    )
                    break
                
                self.state.current_iteration = iteration
                
                # Stage 1: Research
                yield ForgeUpdate(
                    iteration=iteration,
                    stage="researching",
                    message=f"Iteration {iteration}: Searching for winning ideas..."
                )
                
                idea = await self.researcher.generate_idea_depth(
                    track=track,
                    problem_statement=problem_statement,
                    previous_ideas=self.state.ideas_generated[-3:] if self.state.ideas_generated else None,
                    feedback=feedback
                )
                self.state.ideas_generated.append(idea)
                
                yield ForgeUpdate(
                    iteration=iteration,
                    stage="evaluating",
                    idea=idea,
                    message=f"Iteration {iteration}: Evaluating idea..."
                )
                
                # Stage 2: Critique
                evaluation = self.critique.evaluate_idea(
                    idea=idea,
                    track=track,
                    problem_statement=problem_statement,
                    threshold=threshold
                )
                self.state.evaluations.append(evaluation)
                
                if evaluation["verdict"] == "PASS":
                    self.state.final_idea = idea
                    self.state.final_evaluation = evaluation
                    yield ForgeUpdate(
                        iteration=iteration,
                        stage="complete",
                        idea=idea,
                        evaluation=evaluation,
                        message=f"🎉 Found winning idea! Score: {evaluation['overall_score']}/10"
                    )
                    break
                else:
                    feedback = self.critique.get_improvement_feedback(evaluation)
                    yield ForgeUpdate(
                        iteration=iteration,
                        stage="rejected",
                        idea=idea,
                        evaluation=evaluation,
                        message=f"Iteration {iteration}: Score {evaluation['overall_score']}/10 - Below threshold {threshold}/10. Trying again..."
                    )
            else:
                # Max iterations reached
                best_idx = max(range(len(self.state.evaluations)), 
                              key=lambda i: self.state.evaluations[i].get("overall_score", 0))
                self.state.final_idea = self.state.ideas_generated[best_idx]
                self.state.final_evaluation = self.state.evaluations[best_idx]
                
                yield ForgeUpdate(
                    iteration=max_iterations,
                    stage="max_iterations",
                    idea=self.state.final_idea,
                    evaluation=self.state.final_evaluation,
                    message=f"Max iterations reached. Best idea scored {self.state.final_evaluation['overall_score']}/10"
                )
        
        finally:
            self.state.is_running = False
    
    def interrupt(self):
        """Interrupt the current depth mode process."""
        if self.state and self.state.is_running:
            self.state.is_interrupted = True
    
    def get_status(self) -> dict:
        """Get current forge status."""
        if not self.state:
            return {"status": "idle"}
        
        return {
            "status": "running" if self.state.is_running else "stopped",
            "mode": self.state.mode.value,
            "iteration": self.state.current_iteration,
            "max_iterations": self.state.max_iterations,
            "ideas_count": len(self.state.ideas_generated),
            "threshold": self.state.threshold,
            "final_idea": self.state.final_idea,
            "final_evaluation": self.state.final_evaluation
        }
