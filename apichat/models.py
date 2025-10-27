# api_chat/models.py



from django.db import models
# import uuid

class TopicDebate(models.Model):
    topic = models.CharField(max_length=255)

    def __str__(self):
        return self.topic


class DebateSession(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"Session {self.id} - {self.topic[:50]}"


class ChatMessage(models.Model):

    session = models.ForeignKey(
        DebateSession, related_name="messages", on_delete=models.CASCADE
    )
    role = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
