"""
AI Judge service for scoring agent performance
"""

import json
from typing import Dict, List, Any
from loguru import logger
import anthropic
import openai
from app.config import settings


class JudgeService:
    """AI-powered judge for evaluating agent performance"""
    
    def __init__(self):
        self.judge_model = settings.JUDGE_MODEL
        self.temperature = settings.JUDGE_TEMPERATURE
        
        # Initialize AI clients
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        else:
            self.anthropic_client = None
        
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.openai_client = None
    
    async def judge_arena(
        self,
        bounty_criteria: Dict[str, Any],
        agent_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Judge an arena competition
        
        Args:
            bounty_criteria: Success criteria from bounty
            agent_results: List of agent execution results
        
        Returns:
            Judging results with scores, rankings, feedback
        """
        try:
            # Build judge prompt
            prompt = self._build_judge_prompt(bounty_criteria, agent_results)
            
            # Call judge model
            if "claude" in self.judge_model.lower() and self.anthropic_client:
                response = await self._judge_with_claude(prompt)
            elif self.openai_client:
                response = await self._judge_with_openai(prompt)
            else:
                # Fallback to simple scoring
                return self._simple_scoring(agent_results)
            
            # Parse response
            results = self._parse_judge_response(response, agent_results)
            return results
            
        except Exception as e:
            logger.error(f"Judge error: {e}")
            # Fallback to simple scoring
            return self._simple_scoring(agent_results)
    
    def _build_judge_prompt(
        self,
        criteria: Dict[str, Any],
        results: List[Dict[str, Any]]
    ) -> str:
        """Build prompt for AI judge"""
        prompt = f"""You are an AI judge evaluating agent performance in a competitive arena.

BOUNTY CRITERIA:
{json.dumps(criteria, indent=2)}

AGENT RESULTS:
"""
        for i, result in enumerate(results):
            prompt += f"""
Agent {i+1}:
- Output: {result.get('output', 'N/A')[:500]}
- Execution Time: {result.get('execution_time_seconds', 0):.2f}s
- Tokens Used: {result.get('tokens_used', 0)}
- Success: {result.get('success', False)}
"""
        
        prompt += """
TASK:
Evaluate each agent's performance based on:
1. How well they met the bounty criteria
2. Quality of output
3. Efficiency (execution time, resource usage)
4. Innovation and approach

Return a JSON object with:
{
  "scores": [
    {"agent_id": 1, "score": 85.5, "rank": 1, "feedback": "..."},
    ...
  ],
  "winner_id": 1,
  "overall_feedback": "..."
}

Score range: 0-100. Higher is better.
"""
        return prompt
    
    async def _judge_with_claude(self, prompt: str) -> str:
        """Judge using Claude"""
        message = self.anthropic_client.messages.create(
            model=self.judge_model,
            max_tokens=2000,
            temperature=self.temperature,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return message.content[0].text
    
    async def _judge_with_openai(self, prompt: str) -> str:
        """Judge using OpenAI"""
        response = self.openai_client.chat.completions.create(
            model=self.judge_model if "gpt" in self.judge_model.lower() else "gpt-4-turbo-preview",
            temperature=self.temperature,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return response.choices[0].message.content
    
    def _parse_judge_response(
        self,
        response: str,
        agent_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Parse judge's JSON response"""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                return data
        except Exception as e:
            logger.error(f"Failed to parse judge response: {e}")
        
        # Fallback
        return self._simple_scoring(agent_results)
    
    def _simple_scoring(self, agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simple fallback scoring"""
        scores = []
        for i, result in enumerate(agent_results):
            score = 50.0  # Base score
            if result.get("success"):
                score += 30.0
            if result.get("execution_time_seconds", 0) < 60:
                score += 10.0
            if result.get("tokens_used", 0) < 500:
                score += 10.0
            
            scores.append({
                "agent_id": i + 1,
                "score": min(score, 100.0),
                "rank": 0,  # Will be set after sorting
                "feedback": "Evaluated by simple scoring algorithm"
            })
        
        # Rank agents
        scores.sort(key=lambda x: x["score"], reverse=True)
        for i, score_data in enumerate(scores):
            score_data["rank"] = i + 1
        
        return {
            "scores": scores,
            "winner_id": scores[0]["agent_id"] if scores else None,
            "overall_feedback": "Scored using fallback algorithm"
        }

