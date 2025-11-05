"""
Accounts app services.
Contains business logic for user operations (write operations).
"""

from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout


class UserService:
    """Service for User model operations"""
    
    @staticmethod
    def create_user(*, username: str, email: str, password: str, **kwargs) -> User:
        """
        Create a new user.
        
        Args:
            username: Username
            email: Email address
            password: Password
            **kwargs: Additional user fields
        
        Returns:
            Created User instance
        """
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        
        return user
    
    @staticmethod
    def update_user(*, user: User, **data) -> User:
        """
        Update a user.
        
        Args:
            user: User instance to update
            **data: Fields to update
        
        Returns:
            Updated User instance
        """
        for key, value in data.items():
            setattr(user, key, value)
        
        user.save()
        return user
    
    @staticmethod
    def login_user(*, request, user: User) -> None:
        """
        Log in a user.
        
        Args:
            request: Django request object
            user: User instance to log in
        """
        auth_login(request, user)
    
    @staticmethod
    def logout_user(*, request) -> None:
        """
        Log out the current user.
        
        Args:
            request: Django request object
        """
        auth_logout(request)