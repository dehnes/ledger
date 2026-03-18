from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from apps.ledger.models import Account, FinancialInstitute, BankAccount
from apps.ledger.services import LedgerService

User = get_user_model()


class Command(BaseCommand):
    help = "Performs a smoke test on the ledger system"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Ledger Smoke Test..."))

        # 1. Setup - Get or Create a User
        user, _ = User.objects.get_or_create(
            email="admin@ledger.local",  # Use email as the identifier
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        # 2. Setup - Create a Bank
        bank, _ = FinancialInstitute.objects.get_or_create(
            name="Global Bank",
            bic="GLOBDEFFXXX",
            country_id=1,  # Assuming Germany/ID 1 exists from our migration
        )

        # 3. Setup - Create Accounts
        # We use update_or_create to make the script re-runnable
        salary_acc, _ = Account.objects.update_or_create(
            name="Salary Income",
            user=user,
            defaults={"account_type": Account.AccountType.REVENUE},
        )

        checking_acc, _ = BankAccount.objects.update_or_create(
            name="Main Checking",
            user=user,
            defaults={
                "account_type": Account.AccountType.ASSET,
                "institute": bank,
                "iban": "DE1234567890",
            },
        )

        # 4. Action - Use the Service to Record Salary
        self.stdout.write("Recording a Salary Transaction...")

        LedgerService.create_transaction(
            description="March Salary",
            valuta_date=now().date(),
            entries=[
                {
                    "account": salary_acc,
                    "amount": Decimal("-3000.00"),
                },  # Revenue is negative in DEB
                {
                    "account": checking_acc,
                    "amount": Decimal("3000.00"),
                },  # Asset increases
            ],
        )

        # 5. Verification
        # We refresh from DB to see the new balances
        self.stdout.write(f"Checking Balance: {checking_acc.balance}")

        if checking_acc.balance == Decimal("3000.00"):
            self.stdout.write(self.style.SUCCESS("✅ Test Passed: Balance is correct!"))
        else:
            self.stdout.write(
                self.style.ERROR(f"❌ Test Failed: Balance is {checking_acc.balance}")
            )
