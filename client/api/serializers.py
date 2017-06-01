from django.db import transaction
from django.db.models import F
from rest_framework import fields
from rest_framework import serializers
from .views import Client


class ClientListSerializer(serializers.ModelSerializer):
    fullname = fields.ReadOnlyField()

    read_only_fields = ('fullname')

    class Meta:
        model = Client
        fields = ['id', 'fullname']


class ClientUpdateSerializer(serializers.ModelSerializer):
    """
    The serializer substract the 'amount' from the account of the updated client and distribute it among the other 
    clients whose inns are listed in the 'inns' field.
    """
    inns = fields.CharField(required=True, write_only=True)
    amount = fields.DecimalField(decimal_places=2, max_digits=20, required=True, write_only=True)

    class Meta:
        model = Client
        fields = ['inns', 'amount']

    def validate_amount(self, amount):
        """
        Check that received 'amount' doesn't exceed the current account of the updated client.
        """
        if amount > self.instance.account:
            message = 'Сумма {} превышает текущий баланс клиента {}'.format(amount, self.instance.fullname)
            raise serializers.ValidationError(message)
        return amount

    def validate_inns(self, inns):
        """
        Check that inns exist.
        """
        # Make list of received inns
        inns_list = [inn.strip() for inn in inns.split(',')]
        # Get the list of inns from db
        inns_in_db = Client.objects.values_list('inn', flat=True)
        # Find those received inns that don't match any inn in db
        inns_wrong = set(inns_list).difference(set(inns_in_db))
        if inns_wrong:
            message = 'Данные номера ИНН не найдены: {}'.format(', '.join(inns_wrong))
            raise serializers.ValidationError(message)
        return inns

    def update(self, client_donor, validated_data):
        """
        Substract the 'amount' from the account of client_donor and distribute it among the other 
        clients whose inns are listed in the 'inns' field.
        """
        with transaction.atomic():
            inns = validated_data['inns']
            amount = validated_data['amount']

            # Substract money from client_donor account
            client_donor.account = F('account') - amount
            client_donor.save()

            # Append money to clients_receivers in equal shares
            inns_list = [inn.strip() for inn in inns.split(',')]
            amount_per_client = amount / len(inns_list)
            clients_receivers = Client.objects.filter(inn__in=inns_list)
            clients_receivers.update(account=F('account') + amount_per_client)

            # Make custom response
            client_donor.refresh_from_db()
            self.context['custom_response'] = {'fullname': client_donor.fullname, 'account': client_donor.account}
            return client_donor
