"""
Arena competition runner
Orchestrates agent competitions and manages execution
"""

import asyncio
from typing import List, Dict, Any
from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.arena import Arena, ArenaStatus, ArenaParticipation
from app.models.agent import Agent
from app.models.bounty import Bounty
from app.services.sandbox import SandboxManager
from app.services.judge import JudgeService


class ArenaRunner:
    """Runs arena competitions"""
    
    def __init__(self):
        self.sandbox_manager = SandboxManager()
        self.judge_service = JudgeService()
    
    async def run_arena(self, arena_id: int, db: Session):
        """
        Run a complete arena competition
        
        Args:
            arena_id: Arena ID to run
            db: Database session
        """
        logger.info(f"Starting arena {arena_id}")
        
        # Get arena
        arena = db.query(Arena).filter(Arena.id == arena_id).first()
        if not arena:
            raise ValueError(f"Arena {arena_id} not found")
        
        # Get bounty
        bounty = db.query(Bounty).filter(Bounty.id == arena.bounty_id).first()
        if not bounty:
            raise ValueError(f"Bounty {arena.bounty_id} not found")
        
        # Get participants
        participations = db.query(ArenaParticipation).filter(
            ArenaParticipation.arena_id == arena_id
        ).all()
        
        if len(participations) < arena.min_participants:
            raise ValueError(f"Not enough participants (need {arena.min_participants})")
        
        # Update arena status
        arena.status = ArenaStatus.IN_PROGRESS
        arena.started_at = datetime.utcnow()
        db.commit()
        
        try:
            # Execute all agents in parallel
            agent_results = []
            for participation in participations:
                agent = db.query(Agent).filter(Agent.id == participation.agent_id).first()
                if not agent:
                    continue
                
                # Execute agent
                result = await self.sandbox_manager.execute_agent(
                    agent_config={
                        "provider": agent.provider.value,
                        "provider_model": agent.provider_model,
                        "config": agent.config
                    },
                    task_description=bounty.description,
                    timeout_seconds=arena.simulation_duration_seconds
                )
                
                # Update participation
                participation.started_at = datetime.utcnow()
                participation.execution_log = str(result.get("logs", []))
                participation.output_data = {"output": result.get("output")}
                participation.execution_time_seconds = result.get("execution_time_seconds", 0)
                participation.tokens_used = result.get("tokens_used", 0)
                participation.api_calls_made = result.get("api_calls", 0)
                participation.completed_at = datetime.utcnow()
                
                agent_results.append({
                    "participation_id": participation.id,
                    "agent_id": agent.id,
                    "result": result
                })
            
            # Judge the competition
            import json
            criteria = json.loads(bounty.success_criteria)
            judge_results = await self.judge_service.judge_arena(
                bounty_criteria=criteria,
                agent_results=[r["result"] for r in agent_results]
            )
            
            # Update arena with results
            arena.status = ArenaStatus.JUDGING
            db.commit()
            
            # Assign scores and ranks
            for score_data in judge_results.get("scores", []):
                # Find corresponding participation
                agent_idx = score_data["agent_id"] - 1
                if agent_idx < len(agent_results):
                    participation_id = agent_results[agent_idx]["participation_id"]
                    participation = db.query(ArenaParticipation).filter(
                        ArenaParticipation.id == participation_id
                    ).first()
                    if participation:
                        participation.score = score_data["score"]
                        participation.rank = score_data["rank"]
            
            # Determine winner
            winner_id = judge_results.get("winner_id")
            if winner_id and winner_id <= len(agent_results):
                winner_agent_id = agent_results[winner_id - 1]["agent_id"]
                arena.winner_id = winner_agent_id
                
                # Update bounty
                bounty.winning_agent_id = winner_agent_id
                bounty.status = BountyStatus.COMPLETED
                bounty.completed_at = datetime.utcnow()
                
                # Distribute rewards
                await self._distribute_rewards(arena, bounty, db)
            
            # Finalize arena
            arena.status = ArenaStatus.COMPLETED
            arena.completed_at = datetime.utcnow()
            arena.results = judge_results
            arena.judge_feedback = judge_results.get("overall_feedback", "")
            db.commit()
            
            logger.info(f"Arena {arena_id} completed. Winner: {winner_id}")
            
        except Exception as e:
            logger.error(f"Error running arena {arena_id}: {e}")
            arena.status = ArenaStatus.CANCELLED
            db.commit()
            raise
    
    async def _distribute_rewards(self, arena: Arena, bounty: Bounty, db: Session):
        """Distribute rewards to winners"""
        # Get winner participation
        winner_participation = db.query(ArenaParticipation).filter(
            ArenaParticipation.arena_id == arena.id,
            ArenaParticipation.rank == 1
        ).first()
        
        if winner_participation:
            # Winner gets 80% of bounty
            winner_participation.reward_amount = bounty.agent_reward
            winner_participation.reward_paid = False  # Would be paid via payment system
            
            # Update agent stats
            agent = db.query(Agent).filter(Agent.id == winner_participation.agent_id).first()
            if agent:
                agent.total_wins += 1
                agent.total_earnings += bounty.agent_reward
            
            # Update builder stats
            from app.models.user import User
            builder = db.query(User).filter(User.id == winner_participation.agent_builder_id).first()
            if builder:
                builder.total_earnings += bounty.agent_reward
                builder.balance += bounty.agent_reward
        
        # Runner-ups get micro-rewards (5% split)
        runner_ups = db.query(ArenaParticipation).filter(
            ArenaParticipation.arena_id == arena.id,
            ArenaParticipation.rank.in_([2, 3])
        ).all()
        
        runner_up_reward = (bounty.budget * 0.05) / len(runner_ups) if runner_ups else 0
        for participation in runner_ups:
            participation.reward_amount = runner_up_reward
        
        db.commit()

