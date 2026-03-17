from django.db import models
from apps.common.models import Country
from django.conf import settings


class FinancialInstitute(models.Model):
    name = models.CharField(max_length=255)
    bic = models.CharField(max_length=11, unique=True, verbose_name="BIC/SWIFT")
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name="institutes"
    )

    def __str__(self):
        return f"{self.name} ({self.bic})"


class Account(models.Model):
    """The base for all accounts (e.g., 'Groceries', 'Car')"""

    class AccountType(models.TextChoices):
        ASSET = "ASSET", "Asset (Money you have)"
        LIABILITY = "LIABILITY", "Liability (Money you owe)"
        REVENUE = "REVENUE", "Revenue (Income)"
        EXPENSE = "EXPENSE", "Expense (Costs)"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)

    # Hierarchy: Allows an account to have a 'Parent'
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# --- Specialized Account Types ---


class BankAccount(Account):
    """A real SEPA account with IBAN"""

    institute = models.ForeignKey(FinancialInstitute, on_delete=models.PROTECT)
    iban = models.CharField(max_length=34, unique=True)
    account_number = models.CharField(max_length=30, blank=True)


class CreditCard(Account):
    """Credit card metadata"""

    institute = models.ForeignKey(FinancialInstitute, on_delete=models.PROTECT)
    last_four = models.CharField(max_length=4)
    expiry_date = models.DateField(null=True, blank=True)
