const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export interface Idea {
  name: string
  title: string
  problem: string
  solution: string
  tech_stack: string[]
  unique_angle: string
  demo_potential: string
  feasibility_score: number
  innovation_score: number
  impact_score: number
  sources: string[]
}

export interface Evaluation {
  scores: {
    innovation: number
    feasibility: number
    impact: number
    demo_potential: number
    technical_depth: number
    market_fit: number
  }
  overall_score: number
  verdict: "PASS" | "FAIL"
  strengths: string[]
  weaknesses: string[]
  improvement_suggestions: string[]
  killer_feature_idea: string
  reasoning: string
}

export interface ForgeUpdate {
  iteration: number
  stage: "researching" | "evaluating" | "complete" | "rejected" | "interrupted" | "max_iterations"
  message: string
  idea?: Idea
  evaluation?: Evaluation
  error?: string
}

export interface IndependentRequest {
  track: string
  requirements?: string
}

export interface DepthRequest {
  track: string
  problem_statement: string
  threshold: number
  max_iterations: number
}

export interface IdeaResponse {
  success: boolean
  idea: Idea
  mode: string
  evaluation?: Evaluation
}

export interface ForgeStatus {
  status: "idle" | "running" | "stopped" | "not_initialized"
  mode?: string
  iteration?: number
  max_iterations?: number
  ideas_count?: number
  threshold?: number
  final_idea?: Idea
  final_evaluation?: Evaluation
}

export async function runIndependent(request: IndependentRequest): Promise<IdeaResponse> {
  const response = await fetch(`${API_URL}/api/independent`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request)
  })
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }))
    throw new Error(error.detail || "Failed to generate idea")
  }
  
  return response.json()
}

export async function* runDepth(request: DepthRequest): AsyncGenerator<ForgeUpdate> {
  const response = await fetch(`${API_URL}/api/depth`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request)
  })
  
  if (!response.ok) {
    throw new Error("Failed to start depth mode")
  }
  
  const reader = response.body?.getReader()
  if (!reader) throw new Error("No response body")
  
  const decoder = new TextDecoder()
  let buffer = ""
  
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split("\n")
    buffer = lines.pop() || ""
    
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6)) as ForgeUpdate
          yield data
        } catch (e) {
          console.error("Parse error:", e)
        }
      }
    }
  }
}

export async function stopDepth(): Promise<void> {
  await fetch(`${API_URL}/api/depth/stop`, { method: "POST" })
}

export async function getStatus(): Promise<ForgeStatus> {
  const response = await fetch(`${API_URL}/api/status`)
  return response.json()
}
