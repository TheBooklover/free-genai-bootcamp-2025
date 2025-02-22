import requests
import json

def test_chat():
    url = "http://localhost:8000/v1/example-service"
    
    payload = {
        "model": "llama2",
        "messages": "Tell me a short joke about programming"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Status Code:", response.status_code)
        print("Response:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print("Error:", e)

# Added new test cases for Llama model integration
def test_chat_llama():
    url = "http://localhost:8000/v1/example-service"
    
    payload = {
        "model": "llama2",
        "messages": "Tell me a short joke about programming"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Status Code:", response.status_code)
        print("Response:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_chat() 