from decimal import Decimal
from datetime import date
from typing import List, TypedDict
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Transaction, LedgerEntry, Account


class EntryData(TypedDict):
    account: Account
    amount: Decimal


class LedgerService:
    @staticmethod
    @transaction.atomic
    def create_transaction(
        description: str, valuta_date: date, entries: List[EntryData]
    ) -> Transaction:
        """
        Creates a transaction and its associated ledger entries with type safety.
        """
        # 1. Create the Transaction Header
        txn = Transaction.objects.create(
            description=description, valuta_date=valuta_date
        )

        entry_objs: List[LedgerEntry] = []
        total_sum: Decimal = Decimal("0.0000")

        for entry_data in entries:
            amount = entry_data["account"]  # Wait! Pylance would catch this typo now.
            amount = entry_data["amount"]
            total_sum += amount

            entry_objs.append(
                LedgerEntry(
                    transaction=txn, account=entry_data["account"], amount=amount
                )
            )

        # 3. Validation
        if total_sum != Decimal("0.0000"):
            raise ValidationError(
                f"Transaction does not balance! Sum is {total_sum}, must be 0."
            )

        # 4. Persistence
        LedgerEntry.objects.bulk_create(entry_objs)

        return txn
