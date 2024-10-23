from django.contrib.auth.models import Group

from rest_framework import serializers
from .models import CustomUser, PatientProfile, PharmacistProfile
from accounts.models import Roles
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['medical_history']

class PharmacistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacistProfile
        fields = ['pharmacy_name', 'license_number']

class CustomUserSerializer(serializers.ModelSerializer):
    patient_profile = PatientProfileSerializer(required=False)
    pharmacist_profile = PharmacistProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role', 'patient_profile', 'pharmacist_profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(">>>>>>>>>>>>>>>>>>>> ", validated_data)
        role = validated_data.get('role', None)
        patient_data = validated_data.pop('patient_profile', None)
        pharmacist_data = validated_data.pop('pharmacist_profile', None)
        user = CustomUser(**validated_data)
        user.set_password(validated_data.pop('password'))
        user.save()
        # can use signals here
        if role == Roles.PATIRNT and patient_data:
            # PatientProfile.objects.create(user=user, **patient_data)  # signal Not Fire
            patient_profile = PatientProfile(user=user, **patient_data)
            patient_profile.save()  # This will trigger the post_save signal
            patient_group = Group.objects.get(name='Patients')
            user.groups.add(patient_group)
        elif role == Roles.PHARMACIST and pharmacist_data:
            # PharmacistProfile.objects.create(user=user, **pharmacist_data)
            pharmacist_profile = PharmacistProfile(user=user, **pharmacist_data)
            pharmacist_profile.save()  # This will trigger the post_save signal
            pharmacist_group = Group.objects.get(name='Pharmacists')
            user.groups.add(pharmacist_group)

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom claims to the response (so they appear when the user logs in)
        data['role'] = self.user.role

        return data