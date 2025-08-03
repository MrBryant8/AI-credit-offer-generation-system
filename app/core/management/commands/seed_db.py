from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...models import Client, CreditOffer, Loan  # Replace yourapp with your app name
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seed database with users, clients, loans, and credit offers'

    def handle(self, *args, **options):
        User = get_user_model()

        self.stdout.write("Starting database seeding...")

        # 1. Create 3 users
        users_data = [
            {"first_name": "Alice", "last_name": "Müller", "email": "alice@smartcredit.com", "password": "alicepw"},
            {"first_name": "Bob", "last_name": "Klein", "email": "bob@smartcredit.com", "password": "bobpw"},
            {"first_name": "Carla", "last_name": "Schmidt", "email": "carla@smartcredit.com", "password": "carlapw"},
        ]

        created_users = []
        for udata in users_data:
            user, created = User.objects.get_or_create(
                email=udata["email"],
                defaults={
                    "first_name": udata["first_name"],
                    "last_name": udata["last_name"],
                    "is_active": True,
                }
            )
            if created:
                user.set_password(udata["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.email}"))
            else:
                self.stdout.write(f"User already exists: {user.email}")
            created_users.append(user)

        # 2. Create 5 loan types with descriptions
        loan_types_data = [
            {
                "interest": 0.03,
                "amount_start": 1000,
                "amount_end": 5000,
                "duration": 12,
                "description": "Personal Loan - Small. Ideal for small expenses, this loan offers flexible repayment terms suited for short-term needs."
            },
            {
                "interest": 0.025,
                "amount_start": 5001,
                "amount_end": 15000,
                "duration": 24,
                "description": "Personal Loan - Medium. Perfect for medium-sized purchases or consolidations, providing competitive interest rates and manageable monthly payments."
            },
            {
                "interest": 0.02,
                "amount_start": 15001,
                "amount_end": 50000,
                "duration": 36,
                "description": "Personal Loan - Large. Designed for major expenses such as home improvements or education, with longer terms to ease financial planning."
            },
            {
                "interest": 0.015,
                "amount_start": 50000,
                "amount_end": 150000,
                "duration": 60,
                "description": "Home Loan. Tailored for purchasing or refinancing your home, offering low-interest rates with extended repayment periods."
            },
            {
                "interest": 0.035,
                "amount_start": 500,
                "amount_end": 2500,
                "duration": 6,
                "description": "Short-Term Microloan. A quick financing option for urgent, small-scale needs, ensuring fast approval and minimal paperwork."
            },
        ]

        loans = []
        for ld in loan_types_data:
            loan, created = Loan.objects.get_or_create(
                interest=ld["interest"],
                amount_start=ld["amount_start"],
                amount_end=ld["amount_end"],
                duration=ld["duration"],
                defaults={"description": ld["description"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created loan type: {loan.description}"))
            else:
                self.stdout.write(f"Loan type already exists: {loan.description}")
            loans.append(loan)

        # 3. Create 5 clients
        # For this example, assign some clients to some users, and others user=None
        clients_data = [
            {"user_obj": created_users[0], "age": 30, "is_employed": True, "salary": 3500, "current_debt": 2000, "sex": "female", "risk_score": 50, "propensity_score": 70},
            {"user_obj": created_users[1], "age": 45, "is_employed": True, "salary": 5000, "current_debt": 10000, "sex": "male", "risk_score": 30, "propensity_score": 60},
            {"user_obj": created_users[2], "age": 22, "is_employed": False, "salary": 0, "current_debt": 0, "sex": "non-binary", "risk_score": 75, "propensity_score": 40},
            {"user_obj": None, "age": 50, "is_employed": True, "salary": 7000, "current_debt": 15000, "sex": "male", "risk_score": 20, "propensity_score": 80},
            {"user_obj": None, "age": 29, "is_employed": False, "salary": 0, "current_debt": 500, "sex": "female", "risk_score": 65, "propensity_score": 30},
        ]

        clients = []
        for cd in clients_data:
            client, created = Client.objects.get_or_create(
                user_id=cd["user_obj"]._get_pk_val() if cd["user_obj"] else None,
                age=cd["age"],
                defaults={
                    "is_employed": cd["is_employed"],
                    "salary": cd["salary"],
                    "current_debt": cd["current_debt"],
                    "sex": cd["sex"],
                    "risk_score": cd["risk_score"],
                    "propensity_score": cd["propensity_score"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created client (User: {cd['user_obj'].email if cd['user_obj'] else 'None'}, Age: {cd['age']})"))
            else:
                self.stdout.write(f"Client already exists (User: {cd['user_obj'].email if cd['user_obj'] else 'None'}, Age: {cd['age']})")
            clients.append(client)

        # 4. Create 7 credit offers; ensure one client has multiple offers
        offers_data = [
            {"client": clients[0], "loan": loans[0], "email_content": "Offer 1 email content", "moderator_feedback": "Feedback 1", "is_accepted": True, "is_active": True},
            {"client": clients[0], "loan": loans[1], "email_content": "Offer 2 email content", "moderator_feedback": "Feedback 2", "is_accepted": False, "is_active": True},
            {"client": clients[1], "loan": loans[2], "email_content": "Offer 3 email content", "moderator_feedback": "Feedback 3", "is_accepted": False, "is_active": False},
            {"client": clients[2], "loan": loans[3], "email_content": "Offer 4 email content", "moderator_feedback": "Feedback 4", "is_accepted": True, "is_active": True},
            {"client": clients[3], "loan": loans[4], "email_content": "Offer 5 email content", "moderator_feedback": "Feedback 5", "is_accepted": True, "is_active": False},
            {"client": clients[4], "loan": loans[0], "email_content": "Offer 6 email content", "moderator_feedback": "Feedback 6", "is_accepted": False, "is_active": True},
            {"client": clients[4], "loan": loans[1], "email_content": "Offer 7 email content", "moderator_feedback": "Feedback 7", "is_accepted": True, "is_active": True},
        ]

        for idx, od in enumerate(offers_data, start=1):
            offer,created = CreditOffer.objects.get_or_create(
                email_content=od["email_content"],
                defaults={
                    "client_id": od["client"],
                    "loan_type": od["loan"],
                    "moderator_feedback": od["moderator_feedback"],
                    "is_accepted": od["is_accepted"],
                    "is_active": od["is_active"],
                    "expires_at": timezone.now() + timezone.timedelta(days=30),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Offer #{idx} for Client #{od['client'].id}"))
            else:
                self.stdout.write(
                    f"Offer already exists (User: {od['client'].id}, Loan Type: {od['loan'].description})")

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
