from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from typing import Dict, List, Optional
import math
import os
from dotenv import load_dotenv

class PsiAgent:
    def __init__(self, google_api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=google_api_key,
            temperature=0.7,
            top_p=1,
            top_k=1,
            max_output_tokens=2048,
        )

        # PSI Theory parameters
        self.needs = {
            'competence': 1.0,
            'certainty': 1.0,
            'affiliation': 1.0
        }

        self.emotions = {
            'arousal': 0.5,
            'resolution': 0.5,
            'selection_threshold': 0.5
        }

        # Modified memory initialization
        self.memory = ConversationBufferMemory(
            input_key="user_input",  # Specify the input key
            output_key="response",   # Specify the output key
            memory_key="chat_history",
            return_messages=True
        )

    def update_needs(self, interaction_result: Dict[str, float]):
        """Update needs based on interaction outcomes"""
        for need, value in interaction_result.items():
            if need in self.needs:
                self.needs[need] = max(0.0, min(1.0, self.needs[need] + value))

    def calculate_emotion(self) -> Dict[str, float]:
        """Calculate emotional state based on needs"""
        avg_need_satisfaction = sum(self.needs.values()) / len(self.needs)

        self.emotions['arousal'] = 1 - avg_need_satisfaction
        self.emotions['resolution'] = max(0.2, avg_need_satisfaction)
        self.emotions['selection_threshold'] = 0.5 + (1 - avg_need_satisfaction) * 0.3

        return self.emotions

    def generate_response(self, user_input: str) -> str:
        emotion_state = self.calculate_emotion()

        template = """
        Current emotional state:
        - Arousal: {arousal}
        - Resolution: {resolution}
        - Selection Threshold: {selection_threshold}

        Based on these emotional parameters and the following needs:
        - Competence: {competence}
        - Certainty: {certainty}
        - Affiliation: {affiliation}

        Previous conversation context:
        {chat_history}

        User: {user_input}
        Assistant:"""

        prompt = PromptTemplate(
            input_variables=["arousal", "resolution", "selection_threshold",
                           "competence", "certainty", "affiliation",
                           "user_input", "chat_history"],
            template=template
        )

        # Create chain without memory first
        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True
        )

        # Generate response using predict method
        response = chain.predict(
            arousal=emotion_state['arousal'],
            resolution=emotion_state['resolution'],
            selection_threshold=emotion_state['selection_threshold'],
            competence=self.needs['competence'],
            certainty=self.needs['certainty'],
            affiliation=self.needs['affiliation'],
            user_input=user_input,
            chat_history=self.memory.load_memory_variables({})["chat_history"]
        )

        # Manually save the conversation to memory
        self.memory.save_context(
            {"user_input": user_input},
            {"response": response}
        )

        # Simulate need changes based on interaction
        self.update_needs({
            'competence': 0.1,
            'certainty': 0.05,
            'affiliation': 0.15
        })

        return response

class PsiMemoryManager:
    def __init__(self):
        self.short_term_memory: List[Dict] = []
        self.long_term_memory: List[Dict] = []
        self.stm_capacity = 5

    def add_to_memory(self, item: Dict):
        self.short_term_memory.append(item)
        if len(self.short_term_memory) > self.stm_capacity:
            self.long_term_memory.append(self.short_term_memory.pop(0))

    def retrieve_relevant_memories(self, context: str) -> List[Dict]:
        relevant_memories = []
        return relevant_memories

def main():

    load_dotenv("../../")

    gemini_key = os.getenv("GEMINI_API_KEY")
    # Get Google API key from environment variable
    google_api_key = "AIzaSyBBQrhM2EQQswSB37Qhvoeq775RqXnEil0"  # Replace with your actual API key

    psi_agent = PsiAgent(gemini_key)

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = psi_agent.generate_response(user_input)
        print(f"Agent: {response}")
        print(f"Emotional State: {psi_agent.emotions}")
        print(f"Needs State: {psi_agent.needs}")

if __name__ == "__main__":
    main()
