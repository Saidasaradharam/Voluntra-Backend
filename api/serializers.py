from rest_framework import serializers
from .models import CustomUser, Event, VolunteerApplication, CorporateDonations

# User/Registration Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['role']   # Role should not be changed via this serializer

# Event Serializers
class EventSerializer(serializers.ModelSerializer):
        
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_at', 'created_by']

# Volunteer Application Serializers
class VolunteerApplicationSerializer(serializers.ModelSerializer):
    volunteer_username = serializers.CharField(source='volunteer.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = VolunteerApplication
        fields = '__all__'
        read_only_fields = ['applied_at', 'status', 'volunteer', 'certificate_issued', 'certificate_url']

# Corporate Donations Serializers
class CorporateDonationsSerializer(serializers.ModelSerializer):
    donor_username = serializers.CharField(source='donor.username', read_only=True)
    ngo_username = serializers.CharField(source='ngo.username', read_only=True)

    class Meta:
        model = CorporateDonations
        fields = '__all__'
        read_only_fields = ['donated_at', 'transaction_id', 'donor']

    
