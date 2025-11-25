import uuid
from django.db import models
from .usuario import MockUser

class ChatInteraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        MockUser,
        on_delete=models.CASCADE,
        related_name='interactions',
        db_index=True
    )
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.identifier} - {self.created_at}"