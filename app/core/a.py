import os
import requests

def generate_email(prompt):
    # Get the model API URL injected by Docker Model Runner
    model_url = os.getenv("LLM_URL")
    model_name = os.getenv("LLM_NAME")
    print(model_url)
    if not model_url:
        raise EnvironmentError("AI_MODEL_URL environment variable not set")

    # Construct the request payload
    payload = {
        "model": f"{model_name}",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }
    print(model_url, model_name)
    # Call the LLM's generate endpoint
    response1 = requests.get(f"{model_url}/engines/llama.cpp/v1/models")
    print(response1.text)
    response = requests.post(f"{model_url}/chat/completions", json=payload).json()
    print(response)

    if response.status_code == 200:
        result = response.json()
        return result.get("text", "")
    else:
        raise RuntimeError(f"Model API error: {response.status_code} {response.text}")

# Example usage
if __name__ == "__main__":
    prompt_text = "Write a professional email to a client informing about a project delay."
    email_body = generate_email(prompt_text)
    print("Generated Email:\n", email_body)
