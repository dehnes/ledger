from rest_framework import serializers
from .models import Account, Transaction, LedgerEntry


class AccountSerializer(serializers.ModelSerializer):
    # We pull in the @property we wrote earlier
    balance = serializers.DecimalField(max_digits=19, decimal_places=4, read_only=True)
    total_balance = serializers.DecimalField(
        max_digits=19, decimal_places=4, read_only=True
    )

    class Meta:
        model = Account
        fields = ["id", "name", "account_type", "parent", "balance", "total_balance"]
        read_only_fields = ["id"]


class LedgerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerEntry
        fields = ["account", "amount"]


class TransactionSerializer(serializers.ModelSerializer):
    entries = LedgerEntrySerializer(many=True)

    class Meta:
        model = Transaction
        fields = ["id", "description", "valuta_date", "entries"]

    def create(self, validated_data):
        """
        Overriding create to use our LedgerService instead of the default
        Model.objects.create() logic.
        """
        from .services import LedgerService

        entries_data = validated_data.pop("entries")
        return LedgerService.create_transaction(
            description=validated_data["description"],
            valuta_date=validated_data["valuta_date"],
            entries=entries_data,
        )
