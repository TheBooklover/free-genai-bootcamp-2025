## Running Ollama Third-Party Service

### Choosing a Model
# For macOS:
HOST_IP=$(ipconfig getifaddr en0) NO_PROXY=localhost LLM_ENDPOINT_PORT=8008 LLM_MODEL_ID="llama2" docker compose up

# For Linux:
HOST_IP=$(hostname -I | awk '{print $1}') NO_PROXY=localhost LLM_ENDPOINT_PORT=8008 LLM_MODEL_ID="llama2" docker compose up

### IP Address
Your IP will be automatically detected using the commands above.


### Ollama API

# Pull Llama 3.2 1B model
curl http://localhost:8008/api/pull -d '{
  "model": "llama3.2:1b"
}'

### Test Model

curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Hello, how are you?"
}'



