"""FastAPI backend for Idea Forge."""
import asyncio
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json

load_dotenv()

from agents import IdeaForge, ForgeUpdate

# Global forge instance
forge: Optional[IdeaForge] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global forge
    forge = IdeaForge()
    yield
    forge = None


app = FastAPI(
    title="Idea Forge API",
    description="AI-powered hackathon idea generator and validator",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IndependentRequest(BaseModel):
    track: str = Field(..., description="Hackathon track/domain")
    requirements: str = Field("", description="Additional requirements")


class DepthRequest(BaseModel):
    track: str = Field(..., description="Hackathon track/domain")
    problem_statement: str = Field(..., description="Problem statement to solve")
    threshold: int = Field(7, ge=1, le=9, description="Score threshold (1-9)")
    max_iterations: int = Field(10, ge=1, le=20, description="Max iterations")


class IdeaResponse(BaseModel):
    success: bool
    idea: dict
    mode: str
    evaluation: Optional[dict] = None


@app.get("/")
async def root():
    return {"message": "Idea Forge API", "status": "running"}


@app.get("/api/status")
async def get_status():
    """Get current forge status."""
    if not forge:
        return {"status": "not_initialized"}
    return forge.get_status()


@app.post("/api/independent")
async def run_independent(request: IndependentRequest) -> IdeaResponse:
    """
    Run Independent Mode - generates idea from problem discovery.
    Searches Reddit and tech communities for real problems.
    """
    if not forge:
        raise HTTPException(status_code=500, detail="Forge not initialized")
    
    if forge.state and forge.state.is_running:
        raise HTTPException(status_code=409, detail="Another process is running")
    
    try:
        result = await forge.run_independent(
            track=request.track,
            requirements=request.requirements
        )
        return IdeaResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/depth")
async def run_depth(request: DepthRequest):
    """
    Run Depth Mode - iterative idea generation with critique.
    Returns Server-Sent Events stream of updates.
    """
    if not forge:
        raise HTTPException(status_code=500, detail="Forge not initialized")
    
    if forge.state and forge.state.is_running:
        raise HTTPException(status_code=409, detail="Another process is running")
    
    async def event_generator():
        try:
            async for update in forge.run_depth(
                track=request.track,
                problem_statement=request.problem_statement,
                threshold=request.threshold,
                max_iterations=request.max_iterations
            ):
                data = {
                    "iteration": update.iteration,
                    "stage": update.stage,
                    "message": update.message,
                    "idea": update.idea,
                    "evaluation": update.evaluation
                }
                yield f"data: {json.dumps(data)}\n\n"
                await asyncio.sleep(0.1)
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/api/depth/stop")
async def stop_depth():
    """Stop the current depth mode process."""
    if not forge:
        raise HTTPException(status_code=500, detail="Forge not initialized")
    
    forge.interrupt()
    return {"message": "Interrupt signal sent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
