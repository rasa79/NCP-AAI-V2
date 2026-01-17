"""
Coordinator Agent - Orchestrates research workflow and task decomposition.
"""

import logging
from typing import List, Dict, Any
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)


class CoordinatorAgent:
    """
    Coordinator agent responsible for:
    - Decomposing research questions into sub-tasks
    - Assigning tasks to specialized agents
    - Monitoring workflow progress
    - Coordinating agent interactions
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo-instruct"):
        """Initialize coordinator agent."""
        self.name = "Coordinator"
        self.llm = None  # TODO: Initialize LLM
        self.task_queue = []
        self.completed_tasks = []
        
        logger.info(f"{self.name} agent initialized")
    
    def decompose_question(self, research_question: str) -> List[Dict[str, Any]]:
        """
        Decompose research question into sub-tasks.
        
        Args:
            research_question: Main research question
        
        Returns:
            List of sub-task dictionaries with task details
        
        TODO: Implement question decomposition
        Hints:
        - Use LLM to break down the question
        - Create 3-5 sub-questions
        - Assign priority to each sub-task
        - Determine which agent should handle each task
        """
        logger.info(f"Decomposing question: {research_question}")
        
        # YOUR CODE HERE
        # Decompose the question into sub-tasks
        
        sub_tasks = []  # REPLACE THIS
        
        self.task_queue.extend(sub_tasks)
        return sub_tasks
    
    def assign_task(self, task: Dict[str, Any]) -> str:
        """
        Assign task to appropriate agent.
        
        Args:
            task: Task dictionary
        
        Returns:
            Name of agent to handle the task
        
        TODO: Implement task assignment logic
        Hints:
        - Analyze task type
        - Match to agent capabilities
        - Consider agent availability
        """
        # YOUR CODE HERE
        
        return "Searcher"  # REPLACE THIS
    
    def monitor_progress(self) -> Dict[str, Any]:
        """
        Monitor workflow progress.
        
        Returns:
            Progress statistics
        """
        return {
            "total_tasks": len(self.task_queue) + len(self.completed_tasks),
            "pending_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "progress_percentage": len(self.completed_tasks) / (len(self.task_queue) + len(self.completed_tasks)) * 100 if (len(self.task_queue) + len(self.completed_tasks)) > 0 else 0
        }
    
    def mark_task_complete(self, task_id: str):
        """Mark task as completed."""
        # Find and move task from queue to completed
        for task in self.task_queue:
            if task.get("id") == task_id:
                self.task_queue.remove(task)
                self.completed_tasks.append(task)
                break
