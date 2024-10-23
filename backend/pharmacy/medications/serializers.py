from rest_framework import serializers
from .models import Medication, Refill

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'description', 'available_quantity']

class RefillSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source='medication.name', read_only=True)  # To display medication name
    user_name = serializers.CharField(source='user.username', read_only=True)  # To display user name
    fulfilled_by = serializers.CharField(source='fulfilled_by.username', read_only=True)  # To display user name
    

    class Meta:
        model = Refill
        fields = ['id', 'medication', 'medication_name', 'quantity', 'status', 'requested_at', 'fulfilled_at', 'user_name', 'fulfilled_by']

    def validate(self, data):
        medication = data.get('medication')
        quantity = data.get('quantity')

        if quantity <= 0 :
            raise serializers.ValidationError(f"Quantity should be greater than or equal 1")
        # Ensure the requested quantity is available
        if medication.available_quantity < quantity:
            raise serializers.ValidationError(f"Not enough stock. Available quantity: {medication.available_quantity}")

        return data
