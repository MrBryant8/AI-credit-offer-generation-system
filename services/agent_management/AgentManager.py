from services.agent_management.Agent_REST_Interface import REST
from datetime import timedelta
from django.utils import timezone

class AgentManager:
    def __init__(self):
        self.rest=REST()
    
    def check_for_feedback(self):
        all_offers=self.rest.get_all_credit_offers()
        moderator_feedback_list = self.get_moderator_feedback(all_offers)
        return moderator_feedback_list

    def remove_moderator_feedback(self, feedback_list):
        for feedback_pair in feedback_list:
            self.rest.remove_moderator_feedback_from_offer(feedback_pair.get("offer_id"))

    @staticmethod
    def get_moderator_feedback(offers):
        
        one_week_ago = timezone.now() - timedelta(days=7)
        feedback_list = []
        
        for offer in offers:
            if offer.is_active and offer.updated_at >= one_week_ago:  # Assuming updated_at field
                moderator_feedback = offer.moderator_feedback.strip() if offer.moderator_feedback else ""
                if moderator_feedback and moderator_feedback != f"Feedback {offer.id}":
                    feedback_list.append({
                        'offer_id': offer.id,
                        'feedback': moderator_feedback,
                        'date': offer.updated_at
                    })
        
        return feedback_list
            