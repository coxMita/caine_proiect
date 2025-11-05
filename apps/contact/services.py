"""
Contact app services.
Contains business logic for contact operations (write operations).
"""

from .models import ContactMessage


class ContactMessageService:
    """Service for ContactMessage operations"""
    
    @staticmethod
    def create_message(
        *,
        name: str,
        email: str,
        subject: str,
        message: str,
        phone: str = ''
    ) -> ContactMessage:
        """
        Create a new contact message.
        
        Args:
            name: Sender name
            email: Sender email
            subject: Message subject
            message: Message content
            phone: Optional phone number
        
        Returns:
            Created ContactMessage instance
        """
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        return contact_message
    
    @staticmethod
    def mark_as_read(*, message: ContactMessage) -> ContactMessage:
        """
        Mark a message as read.
        
        Args:
            message: ContactMessage instance
        
        Returns:
            Updated ContactMessage instance
        """
        message.is_read = True
        message.save()
        return message
    
    @staticmethod
    def mark_as_responded(*, message: ContactMessage) -> ContactMessage:
        """
        Mark a message as responded.
        
        Args:
            message: ContactMessage instance
        
        Returns:
            Updated ContactMessage instance
        """
        message.is_responded = True
        message.save()
        return message
    
    @staticmethod
    def update_message_status(
        *,
        message: ContactMessage,
        is_read: bool = None,
        is_responded: bool = None
    ) -> ContactMessage:
        """
        Update message status.
        
        Args:
            message: ContactMessage instance
            is_read: Optional read status
            is_responded: Optional responded status
        
        Returns:
            Updated ContactMessage instance
        """
        if is_read is not None:
            message.is_read = is_read
        
        if is_responded is not None:
            message.is_responded = is_responded
        
        message.save()
        return message