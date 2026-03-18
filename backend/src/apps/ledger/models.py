from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from apps.common.models import Country
from django.conf import settings
import uuid
from django.db.models import Sum


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
    # Many-to-Many relationship to our new People app
    owners = models.ManyToManyField("people.Person", related_name="accounts")
    created_at = models.DateTimeField(auto_now_add=True)
    # The 'created_by' keeps track of the system user who manages this
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="managed_accounts",
    )

    @property
    def balance(self) -> Decimal:
        """Calculate the sum of all entries for this account."""
        result = self.entries.aggregate(total=Sum("amount"))["total"]
        return result or Decimal("0.0000")

    @property
    def total_balance(self) -> Decimal:
        """
        Calculates the balance of this account PLUS all its descendants.
        """
        # 1. Get the balance of this specific account
        current_balance = self.balance  # Uses the property we wrote earlier

        # 2. Add balances of all children recursively
        # We use .all() on the 'children' related_name we defined
        for child in self.children.all():
            current_balance += child.total_balance

        return current_balance

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


class Transaction(models.Model):
    """The 'Header' of a financial event (e.g., 'Grocery Shopping')"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=255)
    valuta_date = models.DateField(
        help_text="The date the transaction effectively happens"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.valuta_date} - {self.description}"

    def clean(self):
        """Ensure the transaction balances to zero."""
        if self.pk:  # Only check if the transaction has entries saved
            total = sum(entry.amount for entry in self.entries.all())
            if total != 0:
                raise ValidationError(
                    f"Transaction does not balance! Current sum: {total}"
                )


class LedgerEntry(models.Model):
    """The 'Legs' of a transaction. Every transaction must have at least two."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="entries"
    )
    account = models.ForeignKey(
        "Account", on_delete=models.PROTECT, related_name="entries"
    )

    # Use Decimal for money. Never use Float!
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        help_text="Positive for Credit, Negative for Debit",
    )

    def __str__(self):
        return f"{self.account.name}: {self.amount}"
