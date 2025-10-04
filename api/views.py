from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import CustomUser, Event, VolunteerApplication, CorporateDonations, ContactMessage
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import AllowAny 
from rest_framework import generics
from .serializers import (
    UserSerializer, 
    EventSerializer, 
    VolunteerApplicationSerializer, 
    CorporateDonationsSerializer,
    ContactMessageSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def check_user_exists(request):
    """
    Checks if a user with the given username exists in the database.
    """
    username = request.data.get('username')
    
    if not username:
        return Response({"detail": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the user exists
    user_exists = CustomUser.objects.filter(username__iexact=username).exists()
    
    return Response({
        "username": username,
        "exists": user_exists
    }, status=status.HTTP_200_OK)

class IsNgo(permissions.BasePermission):
    """
    Custom permission to only allow NGOs to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_ngo

class IsVolunteer(permissions.BasePermission):
    """
    Custom permission to only allow Volunteers to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_volunteer
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing user profiles.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow superusers (admin) to see all, but normal users only their own ID
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(pk=self.request.user.pk)
    
    def perform_update(self, serializer):
        # Prevents role from being changed via this API unless by an admin
        if 'role' in serializer.validated_data and not self.request.user.is_superuser:
            del serializer.validated_data['role']
        
        serializer.save()

class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing events. Only NGOs can create, update, or delete events.
    Volunteers and Corporates can view published events.
    """
    queryset = Event.objects.filter(is_published=True).order_by('-date')
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsNgo]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Automatically set the event creator to the logged-in NGO user
        serializer.save(created_by=self.request.user)

class VolunteerApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = VolunteerApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_ngo():
            # NGOs can see applications for their events
            return VolunteerApplication.objects.filter(event__created_by=user).order_by('-applied_at')
        elif user.is_volunteer():
            # Volunteers can see their own applications
            return VolunteerApplication.objects.filter(volunteer=user).order_by('-applied_at')
        else:
            return VolunteerApplication.objects.none()
        
    def get_permissions(self):
        if self.action == 'create':
            # Only volunteers can submit an application
            self.permission_classes = [IsVolunteer]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsNgo]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        # Automatically set the volunteer to the logged-in user
        serializer.save(volunteer=self.request.user)

class CorporateDonationsViewSet(viewsets.ModelViewSet):
    serializer_class = CorporateDonationsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_ngo():
            # NGOs can see donations made to them
            return CorporateDonations.objects.filter(ngo=user).order_by('-donated_at')
        elif user.is_corporate() or user.is_volunteer():
            # Corporates and Volunteers can see their own donations
            return CorporateDonations.objects.filter(donor=user).order_by('-donated_at')
        else:
            return CorporateDonations.objects.none()

    def perform_create(self, serializer):
        # Automatically set the donor to the logged-in user
        serializer.save(donor=self.request.user)

class ContactMessageView(generics.CreateAPIView):
    """
    Handles POST requests for the public Contact Us form submission.
    """
    queryset = ContactMessage.objects.all() # Define queryset
    serializer_class = ContactMessageSerializer # Define serializer
    permission_classes = [AllowAny]