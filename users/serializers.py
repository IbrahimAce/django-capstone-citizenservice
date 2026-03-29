from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration (POST /api/auth/register/).

    What is a serializer?
    It converts Python objects (like a User) to/from JSON.
    It also validates incoming data before saving to the database.

    This serializer:
    1. Accepts username, email, password, password2, role, phone_number, national_id
    2. Validates that password and password2 match
    3. Hashes the password using set_password() before saving
    """

    password = serializers.CharField(
        write_only=True,       # password is accepted as input but never returned in responses
        required=True,
        validators=[validate_password]  # Django's built-in password strength checks
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'role', 'phone_number', 'national_id'
        ]
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, attrs):
        """Called automatically by DRF. Raises an error if passwords don't match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """
        Called when serializer.save() is called in the view.
        We must hash the password — never store plain text passwords.
        """
        validated_data.pop('password2')           # Remove the confirmation field
        password = validated_data.pop('password') # Extract plain text password
        user = User(**validated_data)             # Build User object (not saved yet)
        user.set_password(password)               # Hash the password
        user.save()                               # Now save to database
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating a user's own profile.
    Used by GET /api/auth/profile/ and PATCH /api/auth/profile/
    """

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role',
            'phone_number', 'national_id', 'date_joined'
        ]
        # These fields cannot be changed through the profile endpoint
        read_only_fields = ['id', 'username', 'role', 'date_joined']
