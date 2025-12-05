"use client"

import { useState, useCallback } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Slider } from "@/components/ui/slider"
import { Progress } from "@/components/ui/progress"
import { IdeaCard } from "@/components/IdeaCard"
import { Flame, Search, Layers, Loader2, StopCircle, Sparkles } from "lucide-react"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

interface ForgeUpdate {
  iteration: number
  stage: string
  message: string
  idea?: any
  evaluation?: any
}

export function ForgeInterface() {
  const [mode, setMode] = useState<"independent" | "depth">("independent")
  const [track, setTrack] = useState("")
  const [requirements, setRequirements] = useState("")
  const [problemStatement, setProblemStatement] = useState("")
  const [threshold, setThreshold] = useState([7])
  const [maxIterations, setMaxIterations] = useState([10])
  
  const [isLoading, setIsLoading] = useState(false)
  const [currentUpdate, setCurrentUpdate] = useState<ForgeUpdate | null>(null)
  const [finalIdea, setFinalIdea] = useState<any>(null)
  const [finalEvaluation, setFinalEvaluation] = useState<any>(null)
  const [iterationHistory, setIterationHistory] = useState<ForgeUpdate[]>([])

  const runIndependent = useCallback(async () => {
    if (!track) return
    
    setIsLoading(true)
    setFinalIdea(null)
    setFinalEvaluation(null)
    
    try {
      const response = await fetch(`${API_URL}/api/independent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ track, requirements })
      })
      
      if (!response.ok) throw new Error("Failed to generate idea")
      
      const data = await response.json()
      setFinalIdea(data.idea)
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setIsLoading(false)
    }
  }, [track, requirements])

  const runDepth = useCallback(async () => {
    if (!track || !problemStatement) return
    
    setIsLoading(true)
    setFinalIdea(null)
    setFinalEvaluation(null)
    setIterationHistory([])
    setCurrentUpdate(null)
    
    try {
      const response = await fetch(`${API_URL}/api/depth`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          track,
          problem_statement: problemStatement,
          threshold: threshold[0],
          max_iterations: maxIterations[0]
        })
      })
      
      if (!response.ok) throw new Error("Failed to start depth mode")
      
      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      
      while (reader) {
        const { done, value } = await reader.read()
        if (done) break
        
        const text = decoder.decode(value)
        const lines = text.split("\n").filter(line => line.startsWith("data: "))
        
        for (const line of lines) {
          try {
            const data = JSON.parse(line.slice(6)) as ForgeUpdate
            setCurrentUpdate(data)
            setIterationHistory(prev => [...prev, data])
            
            if (data.stage === "complete" || data.stage === "max_iterations") {
              setFinalIdea(data.idea)
              setFinalEvaluation(data.evaluation)
            }
          } catch (e) {
            console.error("Parse error:", e)
          }
        }
      }
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setIsLoading(false)
    }
  }, [track, problemStatement, threshold, maxIterations])

  const stopDepth = useCallback(async () => {
    try {
      await fetch(`${API_URL}/api/depth/stop`, { method: "POST" })
    } catch (error) {
      console.error("Error stopping:", error)
    }
  }, [])

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold flex items-center justify-center gap-3">
            <Flame className="h-10 w-10 text-primary animate-pulse" />
            Idea Forge
          </h1>
          <p className="text-muted-foreground">
            AI-powered hackathon idea generator with iterative refinement
          </p>
        </div>

        {/* Mode Selection */}
        <Tabs value={mode} onValueChange={(v) => setMode(v as any)} className="w-full">
          <TabsList className="grid w-full grid-cols-2 max-w-md mx-auto">
            <TabsTrigger value="independent" className="flex items-center gap-2">
              <Search className="h-4 w-4" /> Independent
            </TabsTrigger>
            <TabsTrigger value="depth" className="flex items-center gap-2">
              <Layers className="h-4 w-4" /> Depth
            </TabsTrigger>
          </TabsList>

          {/* Independent Mode */}
          <TabsContent value="independent">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Search className="h-5 w-5" /> Independent Mode
                </CardTitle>
                <CardDescription>
                  Searches Reddit and tech communities for real problems, then generates a viable hackathon idea
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Track / Domain</label>
                  <input
                    type="text"
                    value={track}
                    onChange={(e) => setTrack(e.target.value)}
                    placeholder="e.g., AI/ML, FinTech, HealthTech, Sustainability"
                    className="w-full mt-1 px-3 py-2 bg-secondary rounded-md border border-border focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Additional Requirements (optional)</label>
                  <textarea
                    value={requirements}
                    onChange={(e) => setRequirements(e.target.value)}
                    placeholder="Any specific requirements, technologies to use, or constraints..."
                    rows={3}
                    className="w-full mt-1 px-3 py-2 bg-secondary rounded-md border border-border focus:outline-none focus:ring-2 focus:ring-primary resize-none"
                  />
                </div>
                <Button 
                  onClick={runIndependent} 
                  disabled={isLoading || !track}
                  className="w-full"
                >
                  {isLoading ? (
                    <><Loader2 className="h-4 w-4 mr-2 animate-spin" /> Searching...</>
                  ) : (
                    <><Sparkles className="h-4 w-4 mr-2" /> Generate Idea</>
                  )}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Depth Mode */}
          <TabsContent value="depth">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Layers className="h-5 w-5" /> Depth Mode
                </CardTitle>
                <CardDescription>
                  Two-stage iterative process: Researcher → Critique. Continues until threshold is met.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Track / Domain</label>
                  <input
                    type="text"
                    value={track}
                    onChange={(e) => setTrack(e.target.value)}
                    placeholder="e.g., AI/ML, FinTech, HealthTech"
                    className="w-full mt-1 px-3 py-2 bg-secondary rounded-md border border-border focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Problem Statement</label>
                  <textarea
                    value={problemStatement}
                    onChange={(e) => setProblemStatement(e.target.value)}
                    placeholder="Describe the problem you want to solve or the hackathon challenge..."
                    rows={3}
                    className="w-full mt-1 px-3 py-2 bg-secondary rounded-md border border-border focus:outline-none focus:ring-2 focus:ring-primary resize-none"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">
                      Quality Threshold: {threshold[0] * 10}%
                    </label>
                    <Slider
                      value={threshold}
                      onValueChange={setThreshold}
                      min={1}
                      max={9}
                      step={1}
                      className="mt-2"
                    />
                    <p className="text-xs text-muted-foreground mt-1">
                      Idea must score ≥{threshold[0]}/10 to pass
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium">
                      Max Iterations: {maxIterations[0]}
                    </label>
                    <Slider
                      value={maxIterations}
                      onValueChange={setMaxIterations}
                      min={1}
                      max={20}
                      step={1}
                      className="mt-2"
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button 
                    onClick={runDepth} 
                    disabled={isLoading || !track || !problemStatement}
                    className="flex-1"
                  >
                    {isLoading ? (
                      <><Loader2 className="h-4 w-4 mr-2 animate-spin" /> Forging...</>
                    ) : (
                      <><Flame className="h-4 w-4 mr-2" /> Start Forge</>
                    )}
                  </Button>
                  {isLoading && (
                    <Button variant="destructive" onClick={stopDepth}>
                      <StopCircle className="h-4 w-4 mr-2" /> Stop
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Progress Display */}
        {isLoading && currentUpdate && (
          <Card className="border-primary/50 animate-pulse-glow">
            <CardContent className="pt-6">
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span>Iteration {currentUpdate.iteration}/{maxIterations[0]}</span>
                  <span className="capitalize">{currentUpdate.stage}</span>
                </div>
                <Progress value={(currentUpdate.iteration / maxIterations[0]) * 100} />
                <p className="text-sm text-muted-foreground">{currentUpdate.message}</p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Results */}
        {finalIdea && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Sparkles className="h-6 w-6 text-primary" />
              {finalEvaluation?.verdict === "PASS" ? "🎉 Winning Idea Found!" : "Best Idea Generated"}
            </h2>
            <IdeaCard idea={finalIdea} evaluation={finalEvaluation} />
          </div>
        )}

        {/* Iteration History */}
        {iterationHistory.length > 1 && (
          <Card>
            <CardHeader>
              <CardTitle>Iteration History</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {iterationHistory.map((update, i) => (
                  <div 
                    key={i} 
                    className={`p-2 rounded text-sm ${
                      update.stage === "complete" ? "bg-green-500/20" :
                      update.stage === "rejected" ? "bg-red-500/10" :
                      "bg-secondary/50"
                    }`}
                  >
                    <span className="font-mono text-xs text-muted-foreground">
                      [{update.iteration}]
                    </span>{" "}
                    {update.message}
                    {update.evaluation && (
                      <span className="ml-2 text-xs">
                        Score: {update.evaluation.overall_score}/10
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
