from agent.LangchainGemini import PsiAgent
from dotenv import load_dotenv
from typing import Dict
import os
from pathlib import Path




class AgentFactory:
    _instances: Dict[str, PsiAgent] = {}  # Type hint for the instances dictionary

    current_dir = Path(__file__).parent
    # Go up two directory levels to reach the root where .env is located
    root_dir = current_dir.parent.parent
    # Load the .env file from the root directory
    load_dotenv(root_dir / '.env')

    default_gemini_key = os.getenv("GEMINI_API_KEY")

    

    @classmethod
    def get_agent(cls, username: str, key: str = None) -> PsiAgent:  # Added return type hint
        """
        Factory method to get or create an instance of PsiAgent.
        
        Args:
            username (str): The unique identifier for the agent (e.g., username).
            key (str): The API key to use for the PsiAgent. Defaults to the key from the environment.

        Returns:
            PsiAgent: An instance of PsiAgent associated with the username.
        """
        if not username:
            raise ValueError("Username must be provided")

        # Default to the environment key if no custom key is provided
        if key is None:
            key = cls.default_gemini_key  # Fixed to use cls.default_gemini_key

        # Check if an instance for the given username already exists
        if username not in cls._instances:
            # Create and store a new instance if it doesn't exist
            cls._instances[username] = PsiAgent(key)

        return cls._instances[username]
