from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Extends the default Django User to include a 'role' field for
    role-based access control.
    """
    ROLE_CHOICES = [
        ('ngo', 'NGO'),
        ('volunteer', 'Volunteer'),
        ('corporate', 'Corporate'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='volunteer',
        help_text="Role of the user in the system")

    # By default 'username', 'email', 'first_name', 'last_name' fields will be present.

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def is_ngo(self):
        return self.role == 'ngo'
    
    def is_volunteer(self):
        return self.role == 'volunteer'
    
    def is_corporate(self):
        return self.role == 'corporate'
    

class Event(models.Model):
    """
    Represents an event created by an NGO.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    location = models.CharField(max_length=255)
    ngo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'ngo'})
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='managed_events',
        limit_choices_to={'role': 'ngo'})
    
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class VolunteerApplication(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='applications')
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'volunteer'})
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    certificate_issued = models.BooleanField(default=False)
    certificate_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.volunteer.username} - {self.event.title} ({self.status})"
    
    class Meta:
        unique_together = ('event', 'volunteer')  # Prevent duplicate applications
        verbose_name_plural = "Volunteer Applications"

class CorporateDonations(models.Model):
    """
    Represents donations made by corporate users or volunteers to NGOs.
    """
    donor = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True, 
            blank=True,
            related_name='donations_made',
            # Optionally limit to corporate/volunteer roles for clearer tracking
            limit_choices_to=models.Q(role='corporate') | models.Q(role='volunteer')
        )
    ngo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_donations', limit_choices_to={'role': 'ngo'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)


    def __str__(self):
        return f"{self.corporate.username} donated {self.amount} to {self.ngo.username}"
    
