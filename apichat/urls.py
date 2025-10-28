from django.urls import path
from .views import GroqChatAPIView, SessionHistoryAPIView
from .views import TopicDebateListAPIView

urlpatterns = [
    path("chat/", GroqChatAPIView.as_view(), name="groq_chat"),
    path("topics/", TopicDebateListAPIView.as_view(), name="topic_debate_list"),
    # History endpoints: list all sessions or detail by id
    path("history/", SessionHistoryAPIView.as_view(), name="session_history_list"),
    path("history/<int:session_id>/history", SessionHistoryAPIView.as_view(), name="session_history_detail"),
]
