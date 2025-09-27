from djoser.serializers import UserCreateSerializer
from .models import CustomUser

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role')
        
    def validate_role(self, value):

        if value not in ['volunteer', 'ngo', 'corporate']:
             raise serializers.ValidationError("Invalid role.")
        return value