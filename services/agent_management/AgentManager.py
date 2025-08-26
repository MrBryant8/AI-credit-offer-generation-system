import time
from Agent_REST_Interface import REST
from datetime import timedelta, datetime, timezone

class AgentManager:
    def __init__(self):
        self.rest=REST()
        self.improve_feedback_prompt = """
        BACKGROUND: You have taken the role of senior AI Engineer. Your area of focus is Agents and specifically the crewAI framework. 
        You devise task descriptions, that are consice, well-thought, direct and agent-friendly. You take into account custom inputs and act accordingly.
        Your description writing skills are unmatched, as well as your sense of proper formating, from which the agents benefit.

        INPUT: {}

        TASK: In your current task you need to review the following list with feedback comments {}. Group comments based on their meaning.
        You need to choose one comment group that is semantically the most common in that list. I repeat choose only ONE. Ignore the others.
        After that refactor the INPUT, so that you take into account that one comment gorup semantic,
        without changing the custom inputs, which are '{more_details_link}', '{client_name}', '{loan_amount}', '{loan_duration}', '{loan_type_description}', '{client_age}', '{client_sex}', '{bank_address}', '{bank_phone_number}'. 
        I repeat, DO NOT change their place in the prompt or their meaning, as they are super important. Go step-by-step.

        OUTPUT: The output format should be a plain text, I repeat NOT a READY email, yet taking into account the feedback comments.
        The output should end with OUTPUT_REFACTORED and the refactored description of an email-writing task with nothing else after that! 
        """
    
    def check_for_feedback(self):
        all_offers=self.rest.get_all_credit_offers()
        moderator_feedback_list = self.get_moderator_feedback(all_offers)
        return moderator_feedback_list

    def remove_moderator_feedback(self, feedback_list):
        for feedback_pair in feedback_list:
            self.rest.remove_moderator_feedback_from_offer(feedback_pair.get("offer_id"))

    def prepare_feedback_only(self, feedback_list):
        feedback_list_filtered = []
        for fb in feedback_list:
            feedback_list_filtered.append(fb.get("feedback"))

        return feedback_list_filtered
    
    def get_agent_config(self):
        current_agent_config = self.rest.get_agent_config()
        return  current_agent_config.get("default_task_description")
    
    def get_improvement_prompt(self, current_description, feedback_list):
        prompt_with_description = self.improve_feedback_prompt.replace('{}', current_description, 1)
        prompt_final = prompt_with_description.replace('{}', f"{feedback_list}", 1)
        return prompt_final
    
    def change_agent_config(self, new_description):
        self.rest.change_agent_config(new_description)

    @staticmethod
    def get_moderator_feedback(offers):
        
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=30)
        feedback_list = []
        
        for offer in offers:
            updated_at = datetime.fromisoformat(offer.get("updated_at"))
            if updated_at >= one_week_ago:  
                moderator_feedback = offer.get("moderator_feedback").strip() if offer.get("moderator_feedback") else ""
                if moderator_feedback and moderator_feedback != f"Feedback {offer.get("id")}":
                    feedback_list.append({
                        'offer_id': offer.get("id"),
                        'feedback': moderator_feedback,
                    })
        
        return feedback_list
            