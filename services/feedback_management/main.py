from FeedbackManager import FeedbackManager
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



def run_pipeline():

    with open('/run/secrets/gemini_api_key', 'r') as f:
        os.environ["GEMINI_API_KEY"] = f.read().strip()
       
    feedback_manager = FeedbackManager()
    feedback_list_full = feedback_manager.check_for_feedback()
    feedback_list = feedback_manager.prepare_feedback_only(feedback_list_full)
    print(f"List of feedbacks: {feedback_list}")
    active_agent_feedback_count = feedback_manager.get_current_agent_feedback_count()

    if len(feedback_list) < 5 or active_agent_feedback_count != 0:
        print("No need to update the agent task description. Insufficient feedback")
        return

    prompt = feedback_manager.get_feedback_prompt(feedback_list)

    client = genai.Client()
    response = gemini_ask(client, prompt)
    print(f"FULL Response: {response.text}")
    reply = response.text.split("OUTPUT:")[-1]

    if reply:
        print("Valid response taken!")
        feedback_manager.rest.change_agent_feedback(reply)
        # feedback_manager.remove_moderator_feedback(feedback_list=feedback_list_full)
    

run_pipeline()