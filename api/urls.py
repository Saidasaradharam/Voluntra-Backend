from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from api import views as api_views 


router = DefaultRouter()
router.register('profile', views.UserProfileViewSet, basename='profile') 
router.register('events', views.EventViewSet, basename='event')
router.register('applications', views.VolunteerApplicationViewSet, basename='application') 
router.register('donations', views.CorporateDonationsViewSet, basename='donation') 

# FIX: Use the standard Django variable name
urlpatterns = [ 
    path('', include(router.urls)),
    path('auth/check_user/', api_views.check_user_exists),
    path('auth/', include('djoser.urls')), # /users/ and /users/me/
    path('auth/', include('djoser.urls.jwt')) # /jwt/create/, /jwt/refresh/, /jwt/verify/
]