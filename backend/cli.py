#!/usr/bin/env python3
"""CLI interface for Idea Forge - run without the web UI."""
import asyncio
import argparse
import json
from dotenv import load_dotenv

load_dotenv()

from agents import IdeaForge
from config import get_model_name


async def run_independent(track: str, requirements: str = ""):
    """Run independent mode from CLI."""
    model_name = get_model_name()
    print(f"\n🔥 Idea Forge - Independent Mode")
    print(f"Model: {model_name}")
    print(f"Track: {track}")
    print(f"Requirements: {requirements or 'None'}")
    print("-" * 50)
    
    forge = IdeaForge()
    result = await forge.run_independent(track, requirements)
    
    print("\n✨ Generated Idea:")
    print(json.dumps(result["idea"], indent=2))
    return result


async def run_depth(
    track: str,
    problem_statement: str,
    threshold: int = 7,
    max_iterations: int = 10
):
    """Run depth mode from CLI."""
    model_name = get_model_name()
    print(f"\n🔥 Idea Forge - Depth Mode")
    print(f"Model: {model_name}")
    print(f"Track: {track}")
    print(f"Problem: {problem_statement}")
    print(f"Threshold: {threshold}/10 ({threshold * 10}%)")
    print(f"Max Iterations: {max_iterations}")
    print("-" * 50)
    
    forge = IdeaForge()
    
    async for update in forge.run_depth(
        track=track,
        problem_statement=problem_statement,
        threshold=threshold,
        max_iterations=max_iterations
    ):
        print(f"\n[Iteration {update.iteration}] {update.stage.upper()}")
        print(f"  {update.message}")
        
        if update.evaluation:
            print(f"  Score: {update.evaluation['overall_score']}/10")
            print(f"  Verdict: {update.evaluation['verdict']}")
        
        if update.stage in ["complete", "max_iterations", "interrupted"]:
            print("\n" + "=" * 50)
            print("FINAL RESULT:")
            print(json.dumps(update.idea, indent=2))
            if update.evaluation:
                print("\nEVALUATION:")
                print(json.dumps(update.evaluation, indent=2))
            break


def main():
    parser = argparse.ArgumentParser(
        description="Idea Forge - AI-powered hackathon idea generator"
    )
    subparsers = parser.add_subparsers(dest="mode", help="Mode to run")
    
    # Independent mode
    ind_parser = subparsers.add_parser("independent", help="Problem discovery mode")
    ind_parser.add_argument("--track", "-t", required=True, help="Hackathon track/domain")
    ind_parser.add_argument("--requirements", "-r", default="", help="Additional requirements")
    
    # Depth mode
    depth_parser = subparsers.add_parser("depth", help="Iterative refinement mode")
    depth_parser.add_argument("--track", "-t", required=True, help="Hackathon track/domain")
    depth_parser.add_argument("--problem", "-p", required=True, help="Problem statement")
    depth_parser.add_argument("--threshold", "-th", type=int, default=7, help="Score threshold (1-9)")
    depth_parser.add_argument("--max-iter", "-m", type=int, default=10, help="Max iterations")
    
    args = parser.parse_args()
    
    if args.mode == "independent":
        asyncio.run(run_independent(args.track, args.requirements))
    elif args.mode == "depth":
        asyncio.run(run_depth(
            args.track,
            args.problem,
            args.threshold,
            args.max_iter
        ))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
