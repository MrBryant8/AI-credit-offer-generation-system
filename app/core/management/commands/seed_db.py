from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...models import Client, CreditOffer, Loan
import random


class Command(BaseCommand):
    help = 'Seed database with users, clients, and loans'

    def handle(self, *args, **options):
        User = get_user_model()

        self.stdout.write("Starting database seeding...")

        users_data = [
            {"first_name": "Alice", "last_name": "Müller", "email": "alice@smartcredit.com", "password": "alicepw", "phone_number": "12341234"},
            {"first_name": "Bob", "last_name": "Klein", "email": "bob@smartcredit.com", "password": "bobpw", "phone_number": "11111111"},
            {"first_name": "Carla", "last_name": "Schmidt", "email": "carla@smartcredit.com", "password": "carlapw", "phone_number": "22222222"},
            {"first_name": "David", "last_name": "Neumann", "email": "david@smartcredit.com", "password": "davidpw", "phone_number": "00000000"},
            {"first_name": "Eva", "last_name": "Fischer", "email": "eva@smartcredit.com", "password": "evapw", "phone_number": "33333333"},
        ]

        created_users = []
        for udata in users_data:
            user, created = User.objects.get_or_create(
                email=udata["email"],
                defaults={
                    "first_name": udata["first_name"],
                    "last_name": udata["last_name"],
                    "is_active": True,
                    "is_moderator": True if udata["email"] == "bob@smartcredit.com" else False,
                    "phone_number": udata["phone_number"]
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
                "interest": 0.06,
                "amount_start": 1000,
                "amount_end": 5000,
                "duration": 12,
                "description": "Personal Loan - Small. Ideal for small expenses, this loan offers flexible repayment terms suited for short-term needs."
            },
            {
                "interest": 0.05,
                "amount_start": 5000,
                "amount_end": 15000,
                "duration": 24,
                "description": "Personal Loan - Medium. Perfect for medium-sized purchases or consolidations, providing competitive interest rates and manageable monthly payments."
            },
            {
                "interest": 0.04,
                "amount_start": 15000,
                "amount_end": 50000,
                "duration": 36,
                "description": "Personal Loan - Large. Designed for major expenses such as home improvements or education, with longer terms to ease financial planning."
            },
            {
                "interest": 0.03,
                "amount_start": 50000,
                "amount_end": 150000,
                "duration": 60,
                "description": "Home Loan. Tailored for purchasing or refinancing your home, offering low-interest rates with extended repayment periods."
            },
            {
                "interest": 0.07,
                "amount_start": 0,
                "amount_end": 1000,
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
        clients_data = [
    {
        "user_obj": created_users[0],
        "identity_number": random.randint(10**9, 10**10 - 1),
        "age": 30,
        "sex": Client.Sex.FEMALE,
        "job": Client.Job.MEDIUM_SKILL,
        "housing": Client.Housing.OWN,
        "saving_account": Client.SavingsAccount.MODERATE,
        "checking_account": Client.CheckingAccount.LITTLE,
        "credit_amount": 3500,
        "duration": 12,
        "purpose": Client.Purpose.RADIO_OR_TV,
    },
    {
        "user_obj": created_users[1],
        "identity_number": random.randint(10**9, 10**10 - 1),
        "age": 45,
        "sex": Client.Sex.MALE,
        "job": Client.Job.HIGH_SKILL,
        "housing": Client.Housing.OWN,
        "saving_account": Client.SavingsAccount.RICH,
        "checking_account": Client.CheckingAccount.MODERATE,
        "credit_amount": 10000,
        "duration": 24,
        "purpose": Client.Purpose.BUSINESS
    },
    {
        "user_obj": created_users[2],
        "identity_number": random.randint(10**9, 10**10 - 1),
        "age": 22,
        "sex": Client.Sex.FEMALE,
        "job": Client.Job.JOBLESS,
        "housing": Client.Housing.RENT,
        "saving_account": Client.SavingsAccount.UNKNOWN,
        "checking_account": Client.CheckingAccount.UNKNOWN,
        "credit_amount": 400,
        "duration": 6,
        "purpose": Client.Purpose.EDUCATION
    },
    {
        "user_obj": created_users[3],
        "identity_number": random.randint(10**9, 10**10 - 1),
        "age": 50,
        "sex": Client.Sex.MALE,
        "job": Client.Job.HIGH_SKILL,
        "housing": Client.Housing.OWN,
        "saving_account": Client.SavingsAccount.QUITE_RICH,
        "checking_account": Client.CheckingAccount.MODERATE,
        "credit_amount": 15000,
        "duration": 36,
        "purpose": Client.Purpose.CAR,
    },
    {
        "user_obj": created_users[4],
        "identity_number": random.randint(10**9, 10**10 - 1),
        "age": 29,
        "sex": Client.Sex.FEMALE,
        "job": Client.Job.LOW_SKILL,
        "housing": Client.Housing.RENT,
        "saving_account": Client.SavingsAccount.LITTLE,
        "checking_account": Client.CheckingAccount.LITTLE,
        "credit_amount": 500,
        "duration": 9,
        "purpose": Client.Purpose.RADIO_OR_TV,
    },
]

        clients = []
        for cd in clients_data:
            client, created = Client.objects.get_or_create(
                user=cd["user_obj"],
                defaults={
                    "age": cd["age"],
                    "identity_number": cd["identity_number"],
                    "sex": cd["sex"],
                    "job": cd["job"],
                    "housing": cd["housing"],
                    "saving_account": cd["saving_account"],
                    "checking_account": cd["checking_account"],
                    "credit_amount": cd["credit_amount"],
                    "duration": cd["duration"],
                    "purpose": cd["purpose"],
                    "risk_score": cd.get("risk_score"),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created client (User: {cd['user_obj'].email if cd['user_obj'] else 'None'}, Age: {cd['age']})"))
            else:
                self.stdout.write(f"Client already exists (User: {cd['user_obj'].email if cd['user_obj'] else 'None'}, Age: {cd['age']})")
            clients.append(client)


        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))


