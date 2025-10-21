"""
Prompts for trajectory evaluation
"""


class EvaluationPrompts:
    """Prompt templates for trajectory evaluation"""
    
    def success_evaluation_prompt(self, task_description: str, query: str,
                                ground_truth: str, trajectory_summary: str,
                                final_observation: str) -> list:
        """Prompt for evaluating trajectory success"""

# - Expected Outcome (Ground Truth API Call or Result): {ground_truth}
        messages = [
            {
            "role": "user",
            "content": f"""You are a strict task evaluation expert. Your goal is to determine whether the following multi-step agent trajectory successfully completed the assigned task.

    # Task Details
    - Task Description: {task_description}
    - Query: {query}
    - Expected Outcome (API Call or Result, Maybe wrong): {ground_truth}
    
    # Execution Summary
    - Trajectory Summary:
    {trajectory_summary}

    - Final Observation: {final_observation}

    # Evaluation Instructions

    Carefully analyze the trajectory to determine if the task was truly completed. Specifically, consider the following aspects:

    1. **API Matching**: Did the agent correctly call the required APIs according to the task requirements?
    2. **Parameter Usage**: Were the parameters used in API calls correct and sufficient?
    3. **Logical Flow**: Was the sequence of steps logical without unreasonable skips?
    4. **Final Result**: Did the final state achieve the expected outcome, reasonably solve the task, obtain all necessary information, and complete the task objectives?
    5. **Failed or Skipped Steps**: Were there any critical errors, skipped steps, or invalid code that prevented the task from being actually executed?

    # Format Your Response Strictly As:

    Success: [true/false]
    Reason: [Concise and specific explanation, referring to the above criteria.]

    Note: Ignore all Connection timeout or No valid action, because it is very likely that it is the former. Do NOT mark the task as successful if the correct API was never called, the parameters were incorrect, or the result was not achieved, even if the intent seemed right.
    """
            }
        ]
        
        return messages

