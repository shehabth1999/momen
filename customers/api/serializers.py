from rest_framework import serializers
from customers.models import Customer, Record, Address, MainValue, Notes
from django.utils.translation import gettext_lazy as _
from accounts.models import BaseUser


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    address_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Customer
        fields = '__all__'        

    def create(self, validated_data):
        address_id = validated_data.pop('address_id')
        try:
            address = Address.objects.get(id = address_id)
        except Address.DoesNotExist:
            serializers.ValidationError(_('Address does not exist'))

        # Associate the address with the validated data
        validated_data['address'] = address
        customer = Customer.objects.create(**validated_data)    

        return customer

class CustomerSmallSerializer(serializers.ModelSerializer):
    address = serializers.StringRelatedField()
    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'amount', 'collect_day']

class CustomeMinimumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']



class RecordSerializer(serializers.ModelSerializer):
    customer = CustomeMinimumSerializer(read_only=True)
    customer_id = serializers.IntegerField(write_only=True)
    collector = serializers.StringRelatedField(read_only=True)
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Record
        fields = '__all__'

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        try:
            customer = Customer.objects.get(id = customer_id)
            validated_data['customer'] = customer
        except Customer.DoesNotExist:
            serializers.ValidationError(_('Customer does not exist'))

        # get collector from request.user
        collector = BaseUser.objects.get(id = self.context['request'].user.id)    
        validated_data['collector'] = collector
        
        main_value = MainValue.objects.all().first().amount
        
        is_refund = validated_data.get('is_refund', False)

        if is_refund:
            validated_data['amount'] = -main_value
        else:
            validated_data['amount'] = main_value

        new_val = customer.amount - validated_data['amount']

        if new_val < 0:
            raise serializers.ValidationError(_('This Customer Already Paid'))
        
        customer.amount = new_val
        customer.save()

        return Record.objects.create(**validated_data)    
    



class NotesSerializer(serializers.ModelSerializer):
    customer = CustomeMinimumSerializer(read_only=True)
    customer_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Notes
        fields = '__all__'

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        try:
            customer = Customer.objects.get(id = customer_id)
            validated_data['customer'] = customer
        except Customer.DoesNotExist:
            serializers.ValidationError(_('Customer does not exist'))

        return Notes.objects.create(**validated_data)