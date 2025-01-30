from fastapi import FastAPI, HTTPException
from repository.AgnetRepository import AgentFactory
from models.models import ResponseModel, RequestModel
from datetime import datetime
from repository.AgnetRepository import AgentFactory
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Test API",
    description="A simple API.",
    version="1.0.0"
     )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict access if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
@app.post("/request", response_model=ResponseModel)
async def create_request(request: RequestModel) -> ResponseModel:
    try:
        # Get or create agent instance
        agent = AgentFactory.get_agent(username=request.username)
        

        logging.info(f"This is a debug message {request}")
         


        # Update needs
        needs_update = {
            'competence': request.competence,
            'certainty': request.certainty,
            'affiliation': request.affiliation
        }
        logging.info(f"Before update_needs: {agent.needs}")
        agent.update_needs(needs_update)
        logging.info(f"After update_needs: {agent.needs}")

        # Update emotions
        emotions_update = {
            'arousal': request.arousal,
            'resolution': request.resolution,
            'selection_threshold': request.selection_threshold
        }
        logging.info(f"Before update_emotion: {agent.emotions}")
        agent.update_emotion(emotions_update)
        logging.info(f"After update_emotion: {agent.emotions}")

        # Generate response
        result = await agent.generate_response(request.message)  # Make async if generate_response is async

        # Create response
        response = ResponseModel(
            username=request.username,
            message=result,
            competence=agent.needs['competence'],
            certainty=agent.needs['certainty'],
            affiliation=agent.needs['affiliation'],
            arousal=agent.emotions['arousal'],
            resolution=agent.emotions['resolution'],
            selection_threshold=agent.emotions['selection_threshold'],
        )

        return response

    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid key in agent state: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid value in request: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )