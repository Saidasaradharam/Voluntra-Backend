from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet, basename='profile') 
router.register('events', views.EventViewSet, basename='event')
router.register('applications', views.VolunteerApplicationViewSet, basename='application') 
router.register('donations', views.CorporateDonationsViewSet, basename='donation') 

# FIX: Use the standard Django variable name
urlpatterns = [ 
    path('', include(router.urls))
]