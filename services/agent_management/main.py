from AgentManager import AgentManager
from google import genai
from google.genai import types
import os

def gemini_ask(client: genai.Client, question, model="gemini-2.0-flash-lite"):

    return client.models.generate_content(
        model=model, 
        contents=question, 
        config=types.GenerateContentConfig(
            temperature=0.1
        )
    )

os.environ["GEMINI_API_KEY"] = ''

def run_pipeline():
    am = AgentManager()
    feedback_list_full = am.check_for_feedback()
    feedback_list = am.prepare_feedback_only(feedback_list_full)
    print(f"List of feedbacks: {feedback_list}")

    if len(feedback_list) < 1:
        print("No need to update the agent task description")
        return

    current_description = am.get_agent_config()
    prompt = am.get_improvement_prompt(current_description, feedback_list)

    client = genai.Client()
    response = gemini_ask(client, prompt)
    print(f"FULL Response: {response.text}")
    reply = response.text.split("OUTPUT_REFACTORED:")[-1]

    if reply:
        print("Valid response taken!")
        am.change_agent_config(reply)
        # am.remove_moderator_feedback(feedback_list=feedback_list_full)
    

run_pipeline()