from django.urls import path
from .views import GroqChatAPIView, SessionHistoryAPIView
from .views import TopicDebateListAPIView

urlpatterns = [
    path("chat/", GroqChatAPIView.as_view(), name="groq_chat"),
    path("topics/", TopicDebateListAPIView.as_view(), name="topic_debate_list"),
    path("history/<str:session_id>/history/", SessionHistoryAPIView.as_view(), name="session_history"),
]
