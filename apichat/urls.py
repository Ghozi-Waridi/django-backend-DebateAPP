from django.urls import  path
from .views import GroqChatAPIView, TopicDebateListAPIView

urlpatterns = [
    path('chat/', GroqChatAPIView.as_view(), name='groq_chat'),
    path('topics/', TopicDebateListAPIView.as_view(), name='topic_debate_list'),
]
