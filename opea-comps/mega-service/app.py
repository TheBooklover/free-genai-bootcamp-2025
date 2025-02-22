from fastapi import HTTPException
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo
)
from comps.cores.mega.constants import ServiceType, ServiceRoleType
from comps import MicroService, ServiceOrchestrator
import os
import json
import aiohttp

os.environ["OTEL_PYTHON_DISABLED"] = "1"  # Disable OpenTelemetry
os.environ["TELEMETRY_ENDPOINT"] = ""

# Explicitly set environment variables
os.environ["LLM_SERVICE_HOST_IP"] = "localhost"
os.environ["LLM_SERVICE_PORT"] = "8008"

# Use the explicit values
EMBEDDING_SERVICE_HOST_IP = os.getenv("EMBEDDING_SERVICE_HOST_IP", "0.0.0.0")
EMBEDDING_SERVICE_PORT = os.getenv("EMBEDDING_SERVICE_PORT", 6000)
LLM_SERVICE_HOST_IP = "localhost"  # Hardcode instead of using os.getenv
LLM_SERVICE_PORT = 8008  # Hardcode instead of using os.getenv
LLM_MODEL = "llama2:1b"  # Updated model specification


class ExampleService:
    def __init__(self, host="0.0.0.0", port=8000):
        print('hello')
        self.host = host
        self.port = port
        self.endpoint = "/v1/example-service"
        self.megaservice = ServiceOrchestrator()

    def add_remote_service(self):
        #embedding = MicroService(
        #    name="embedding",
        #    host=EMBEDDING_SERVICE_HOST_IP,
        #    port=EMBEDDING_SERVICE_PORT,
        #    endpoint="/v1/embeddings",
        #    use_remote_service=True,
        #    service_type=ServiceType.EMBEDDING,
        #)
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            endpoint="/api/generate",
            use_remote_service=True,
            service_type=ServiceType.LLM
        )
        #self.megaservice.add(embedding).add(llm)
        #self.megaservice.flow_to(embedding, llm)
        self.megaservice.add(llm)
    
    def start(self):

        self.service = MicroService(
            self.__class__.__name__,
            service_role=ServiceRoleType.MEGASERVICE,
            host=self.host,
            port=self.port,
            endpoint=self.endpoint,
            input_datatype=ChatCompletionRequest,
            output_datatype=ChatCompletionResponse,
        )

        self.service.add_route(self.endpoint, self.handle_request, methods=["POST"])

        self.service.start()
    async def handle_request(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        try:
            # Validate model first
            if request.model not in ["llama3.2:1b"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid model: {request.model}. Available models: llama3.2:1b"
                )

            # Validate messages format
            if not isinstance(request.messages, list):
                raise HTTPException(
                    status_code=400,
                    detail="Messages must be a list of message objects"
                )
            
            if not request.messages or not isinstance(request.messages[0], dict):
                raise HTTPException(
                    status_code=400,
                    detail="Messages must contain at least one message object"
                )

            if 'content' not in request.messages[0]:
                raise HTTPException(
                    status_code=400,
                    detail="Message must have 'content' field"
                )

            # Format the request exactly like our working direct test
            ollama_request = {
                "model": request.model or "llama3.2:1b",
                "prompt": request.messages[0]['content'] if isinstance(request.messages, list) else request.messages,
                "stream": False
            }
            
            print("Sending request to Ollama:", ollama_request)
            
            # Direct HTTP request instead of using MicroService
            async with aiohttp.ClientSession() as session:
                url = f"http://{LLM_SERVICE_HOST_IP}:{LLM_SERVICE_PORT}/api/generate"
                print("Making direct request to:", url)
                async with session.post(url, json=ollama_request) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Ollama error: {error_text}"
                        )
                    result = await response.json()
                    print("Direct response:", result)
                    # Extract just the response text from Ollama's response
                    content = result.get('response', '')
                    print("Extracted content:", content)  # Add this debug print

            # Create the response
            response = ChatCompletionResponse(
                model=request.model or "example-model",
                choices=[
                    ChatCompletionResponseChoice(
                        index=0,
                        message=ChatMessage(
                            role="assistant",
                            content=content
                        ),
                        finish_reason="stop"
                    )
                ],
                usage=UsageInfo(
                    prompt_tokens=0,
                    completion_tokens=0,
                    total_tokens=0
                )
            )
            
            return response
            
        except Exception as e:
            # Handle any errors
            raise HTTPException(status_code=500, detail=str(e))

example = ExampleService()
example.add_remote_service()
example.start()