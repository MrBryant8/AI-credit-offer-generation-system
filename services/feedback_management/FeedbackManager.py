from Feedback_REST_Interface import REST

class FeedbackManager:

    """
    Feedback Manager Class to manage agent feedback related operations.
    """
    def __init__(self):
        self.rest=REST()
        self.feedback_summary_prompt = """
        BACKGROUND: You have taken the role of senior office assistant. Your area of focus is text analysis and summarization. 
        Your analysis and comprehension is unmatched. You add value to you company by producing text, that is consice, well-thought, direct and easy to understand.

        INPUT: {}

        TASK: In your current task you need to review the list with feedback comments as given in INPUT. 
        Group feedback comments based on their meaning. Write a comprehensive summary for each group and add the number of similar feedbacks per group.
        Go in detail and also write any suggestions for improvement.
        
        OUTPUT: The output format should be plain text,
        The output should start with OUTPUT_REFACTORED: then continue with the summary and suggestions with nothing else after that! 
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
    
    
    def get_feedback_prompt(self, feedback_list):
        prompt_final = self.feedback_summary_prompt.replace('{}', f"{feedback_list}")
        return prompt_final
    
    def get_current_agent_feedback_count(self):
        agent_feedbacks = self.rest.get_agent_feedback_objects()
        active_agent_feedbacks = [feedback for feedback in agent_feedbacks if agent_feedbacks["is_reviewed"] == False]
        return len(active_agent_feedbacks)
    

    @staticmethod
    def get_moderator_feedback(offers):
        
        feedback_list = []
        for offer in offers:
            moderator_feedback = offer.get("moderator_feedback").strip() if offer.get("moderator_feedback") else ""
            if moderator_feedback and moderator_feedback != f"Feedback {offer.get("id")}":
                feedback_list.append({
                    'offer_id': offer.get("id"),
                    'feedback': moderator_feedback,
                })
        
        return feedback_list
            