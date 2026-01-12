from django.db import models
from django.conf import settings


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('system', 'system'),
        ('user', 'user'),
        ('assistant', 'assistant'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    conversation = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        who = self.user.username if self.user else 'anon'
        return f"{self.created_at.isoformat()} {who} {self.role}: {self.content[:40]}"
