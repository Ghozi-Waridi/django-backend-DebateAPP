# api_chat/views.py

from email import message
from hmac import trans_36
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import get_groq_response
from .models import DebateSession, ChatMessage, TopicDebate


class TopicDebateListAPIView(APIView):
    def post(self, request, *args, **kwargs):
        topic = request.data.get("topic")

        if not topic:
            return Response(
                {"error": "Topic is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if TopicDebate.objects.filter(topic=topic).exists():
            return Response(
                {"error": "Topic already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        new_topic = TopicDebate.objects.create(topic=topic)

        return Response(
            {
                "id": new_topic.id,
                "topic": new_topic.topic,
                "message": "Topic created successfully",
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, *args, **kwargs):
        topics = TopicDebate.objects.all()
        data = [{"id": topic.id, "topic": topic.topic} for topic in topics]
        return Response(data, status=status.HTTP_200_OK)


class GroqChatAPIView(APIView):
    """
    View untuk menangani logika chat debat.
    Bisa memulai sesi baru atau melanjutkan yang sudah ada.
    """

    def post(self, request, *args, **kwargs):
        print("Coba : ", request.data)
        user_prompt = request.data.get("prompt")
        session_id = request.data.get("sessionId") or request.data.get("session_id")
        topic = request.data.get("topic")
        pihak = request.data.get("pihak")

        if session_id:
            try:
                session = DebateSession.objects.get(id=session_id)
                # Pastikan topic tersedia
                if not topic:
                    topic = session.topic
                
                ChatMessage.objects.create(
                    session=session,
                    role="user",
                    content=user_prompt
                )
            except DebateSession.DoesNotExist:
                return Response(
                    {"error": "Sesi debat tidak ditemukan."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            # Validasi topic saat membuat sesi baru
            if not topic:
                return Response(
                    {"error": "Topic diperlukan untuk sesi baru."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            session = DebateSession.objects.create(topic=topic)
            user_prompt = f"""
        Topik: {topic}
        Posisi: {pihak}

        **Tugas**: Siapkan argumentasi yang kuat dan persuasif dari sudut pandang {pihak} dengan struktur:

        1. **Pernyataan Pembuka** - maks 100 kata
        2. **3 Argumentasi Utama** dengan data pendukung  
        3. **Antisipasi Kontra-Argument** dari pihak lawan
        4. **Pernyataan Penutup** yang impactful

        **Requirements**:
        - Bahasa formal dan profesional
        - Fakta-based dan logis
        - Tone: persuasive dan confident
        - Sertakan contoh konkret jika memungkinkan
        """
            ChatMessage.objects.create(session=session, role="user", content=user_prompt)

        print(f"Session ID: {session.id}, Topic: {session.topic}")
        ai_response_text = get_groq_response(session.id, user_prompt)
        
        return Response(
            {
                "response": ai_response_text, 
                "session_id": str(session.id), 
                "topic": session.topic or topic
            },
            status=status.HTTP_200_OK,
        )


class SessionHistoryAPIView(APIView):
    def get(self, request, session_id=None, *args, **kwargs):
        # Jika session_id diberikan: kembalikan riwayat untuk satu sesi tersebut
        if session_id is not None:
            try:
                session = DebateSession.objects.get(id=session_id)
            except DebateSession.DoesNotExist:
                return Response({"error": "session tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

            messages = ChatMessage.objects.filter(session=session).order_by("created_at")
            history = [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.created_at.isoformat(),
                }
                for m in messages
            ]
            return Response(
                {
                    "session_id": session.id,
                    "topic": session.topic,
                    "history": history,
                },
                status=status.HTTP_200_OK,
            )

        # Tanpa session_id: kembalikan semua sesi dengan history masing-masing
        sessions = DebateSession.objects.all().order_by("created_at")
        messages = ChatMessage.objects.filter(session__in=sessions).order_by("created_at")

        by_session = {s.id: {"session_id": s.id, "topic": s.topic, "history": []} for s in sessions}
        for m in messages:
            by_session[m.session_id]["history"].append(
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.created_at.isoformat(),
                }
            )

        return Response({"sessions": list(by_session.values())}, status=status.HTTP_200_OK)

    # Opsional: tetap sediakan POST untuk ambil history per session jika diinginkan
    def post(self, request, session_id=None, *args, **kwargs):
        if session_id is None:
            return Response({"error": "session_id diperlukan di URL"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            session = DebateSession.objects.get(id=session_id)
        except DebateSession.DoesNotExist:
            return Response({"error": "session tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        messages = ChatMessage.objects.filter(session=session).order_by("created_at")
        history = [
            {
                "role": m.role,
                "content": m.content,
                "timestamp": m.created_at.isoformat(),
            }
            for m in messages
        ]
        return Response(
            {
                "session_id": session.id,
                "topic": session.topic,
                "history": history,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, session_id=None, *args, **kwargs):
        """Menghapus session berdasarkan ID"""
        if session_id is None:
            return Response(
                {"error": "session_id diperlukan di URL"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            session = DebateSession.objects.get(id=session_id)
            session.delete()  # Akan otomatis menghapus ChatMessage terkait karena on_delete=CASCADE
            return Response(
                {"message": "Session berhasil dihapus"},
                status=status.HTTP_200_OK
            )
        except DebateSession.DoesNotExist:
            return Response(
                {"error": "Session tidak ditemukan"},
                status=status.HTTP_404_NOT_FOUND~
            )