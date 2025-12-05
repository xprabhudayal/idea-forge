"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Lightbulb, Wrench, Zap, Target, ExternalLink } from "lucide-react"

interface Idea {
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
  sources?: string[]
}

interface Evaluation {
  scores: {
    innovation: number
    feasibility: number
    impact: number
    demo_potential: number
    technical_depth: number
    market_fit: number
  }
  overall_score: number
  verdict: string
  strengths: string[]
  weaknesses: string[]
  improvement_suggestions: string[]
  killer_feature_idea: string
  reasoning: string
}

interface IdeaCardProps {
  idea: Idea
  evaluation?: Evaluation
}

function ScoreBadge({ score, label }: { score: number; label: string }) {
  const color = score >= 8 ? "text-green-400" : score >= 6 ? "text-yellow-400" : "text-red-400"
  return (
    <div className="flex flex-col items-center">
      <span className={`text-2xl font-bold ${color}`}>{score}</span>
      <span className="text-xs text-muted-foreground">{label}</span>
    </div>
  )
}

export function IdeaCard({ idea, evaluation }: IdeaCardProps) {
  return (
    <Card className="border-primary/20 bg-gradient-to-br from-card to-card/50">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-xl flex items-center gap-2">
              <Lightbulb className="h-5 w-5 text-primary" />
              {idea.title}
            </CardTitle>
            <CardDescription className="mt-1 font-mono text-xs">{idea.name}</CardDescription>
          </div>
          {evaluation && (
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              evaluation.verdict === "PASS" 
                ? "bg-green-500/20 text-green-400" 
                : "bg-red-500/20 text-red-400"
            }`}>
              {evaluation.verdict} ({evaluation.overall_score}/10)
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h4 className="text-sm font-medium flex items-center gap-2 mb-1">
            <Target className="h-4 w-4 text-red-400" /> Problem
          </h4>
          <p className="text-sm text-muted-foreground">{idea.problem}</p>
        </div>
        
        <div>
          <h4 className="text-sm font-medium flex items-center gap-2 mb-1">
            <Zap className="h-4 w-4 text-yellow-400" /> Solution
          </h4>
          <p className="text-sm text-muted-foreground">{idea.solution}</p>
        </div>
        
        <div>
          <h4 className="text-sm font-medium flex items-center gap-2 mb-1">
            <Wrench className="h-4 w-4 text-blue-400" /> Tech Stack
          </h4>
          <div className="flex flex-wrap gap-1">
            {idea.tech_stack.map((tech, i) => (
              <span key={i} className="px-2 py-0.5 bg-secondary rounded text-xs">{tech}</span>
            ))}
          </div>
        </div>
        
        {idea.unique_angle && (
          <div className="p-3 bg-primary/10 rounded-lg">
            <h4 className="text-sm font-medium mb-1">✨ Unique Angle</h4>
            <p className="text-sm text-muted-foreground">{idea.unique_angle}</p>
          </div>
        )}
        
        {idea.demo_potential && (
          <div className="p-3 bg-secondary/50 rounded-lg">
            <h4 className="text-sm font-medium mb-1">🎬 Demo Potential</h4>
            <p className="text-sm text-muted-foreground">{idea.demo_potential}</p>
          </div>
        )}
        
        <div className="flex justify-around pt-2 border-t border-border">
          <ScoreBadge score={idea.feasibility_score} label="Feasibility" />
          <ScoreBadge score={idea.innovation_score} label="Innovation" />
          <ScoreBadge score={idea.impact_score} label="Impact" />
        </div>
        
        {evaluation && (
          <div className="pt-4 border-t border-border space-y-3">
            <h4 className="font-medium">Critique Evaluation</h4>
            <div className="grid grid-cols-3 gap-2 text-center">
              {Object.entries(evaluation.scores).map(([key, value]) => (
                <div key={key} className="p-2 bg-secondary/30 rounded">
                  <div className="text-lg font-bold">{value}</div>
                  <div className="text-xs text-muted-foreground capitalize">{key.replace('_', ' ')}</div>
                </div>
              ))}
            </div>
            
            {evaluation.strengths.length > 0 && (
              <div>
                <h5 className="text-sm font-medium text-green-400 mb-1">Strengths</h5>
                <ul className="text-xs text-muted-foreground space-y-1">
                  {evaluation.strengths.map((s, i) => <li key={i}>• {s}</li>)}
                </ul>
              </div>
            )}
            
            {evaluation.weaknesses.length > 0 && (
              <div>
                <h5 className="text-sm font-medium text-red-400 mb-1">Weaknesses</h5>
                <ul className="text-xs text-muted-foreground space-y-1">
                  {evaluation.weaknesses.map((w, i) => <li key={i}>• {w}</li>)}
                </ul>
              </div>
            )}
            
            {evaluation.killer_feature_idea && (
              <div className="p-2 bg-primary/20 rounded">
                <h5 className="text-sm font-medium mb-1">💡 Killer Feature Suggestion</h5>
                <p className="text-xs text-muted-foreground">{evaluation.killer_feature_idea}</p>
              </div>
            )}
          </div>
        )}
        
        {idea.sources && idea.sources.length > 0 && (
          <div className="pt-2 border-t border-border">
            <h4 className="text-xs font-medium text-muted-foreground mb-1 flex items-center gap-1">
              <ExternalLink className="h-3 w-3" /> Sources
            </h4>
            <div className="flex flex-wrap gap-1">
              {idea.sources.slice(0, 3).map((url, i) => (
                <a 
                  key={i} 
                  href={url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-xs text-primary hover:underline truncate max-w-[150px]"
                >
                  {new URL(url).hostname}
                </a>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
