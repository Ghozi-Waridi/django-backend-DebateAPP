# api_chat/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import get_groq_response
from .models import DebateSession, ChatMessage

class GroqChatAPIView(APIView):
    """
    View untuk menangani logika chat debat.
    Bisa memulai sesi baru atau melanjutkan yang sudah ada.
    """
    def post(self, request, *args, **kwargs):
        user_prompt = request.data.get('prompt')
        session_id = request.data.get('session_id') 

        if not user_prompt:
            return Response(
                {"error": "Field 'prompt' tidak boleh kosong."},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        if session_id:

            try:
                session = DebateSession.objects.get(id=session_id)
            except DebateSession.DoesNotExist:
                return Response({"error": "Sesi debat tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)
        else:

            topic = f"Debat dimulai dengan: {user_prompt[:50]}..."
            session = DebateSession.objects.create(topic=topic)

        ChatMessage.objects.create(
            session=session,
            role='user',
            content=user_prompt
        )

        ai_response_text = get_groq_response(session.id, user_prompt)
        return Response(
            {
                "response": ai_response_text,
                "session_id": session.id 
            },
            status=status.HTTP_200_OK
        )
