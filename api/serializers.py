from rest_framework import serializers
from .models import CustomUser, Event, VolunteerApplication, CorporateDonations, ContactMessage

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
        fields = [
            'id', 
            'title', 
            'description', 
            'date', 
            'startTime', 
            'endTime', 
            'location', 
            'is_published', 
            'created_by_username', 
        ]
        # NOTE: 'created_by' and 'created_at' are handled correctly as read-only.
        # The 'ngo' ForeignKey is the main issue. Since 'created_by' and 'ngo' 
        # both link to the NGO user and are set in perform_create, you only need
        # to expose one for reading, or handle them consistently. 
        
        # Given your model has both 'ngo' and 'created_by', let's assume 'created_by' 
        # is sufficient for the API output and ensure it is read-only.

        read_only_fields = ['created_at', 'created_by', 'ngo']
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
        read_only_fields = ['donated_at', 'transaction_id', 'donor']\
        
class ContactMessageSerializer(serializers.ModelSerializer):
    # This acts like validaiton
    name = serializers.CharField(max_length=100, min_length=2)
    message = serializers.CharField(min_length=10) 

    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ['received_at']

    
