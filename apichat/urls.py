from django.urls import  path
from .views import GroqChatAPIView

urlpatterns = [
    path('chat/', GroqChatAPIView.as_view(), name='groq_chat'),
    ]
