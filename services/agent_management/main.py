from AgentManager import AgentManager


def run_pipeline():
    am = AgentManager()
    feedback_list = am.check_for_feedback()
    am.remove_moderator_feedback(feedback_list=feedback_list)

    #TODO: send feedbacks to LLM somehow and return its suggested agent-config, when done, send a request to update the agent-config



run_pipeline()