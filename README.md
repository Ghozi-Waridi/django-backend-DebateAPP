# Django Debate LLM API

API backend untuk aplikasi debat menggunakan Large Language Model (LLM) dengan integrasi Groq AI. Aplikasi ini memungkinkan pengguna untuk membuat topik debat dan melakukan sesi debat interaktif dengan AI.

## 📋 Daftar Isi

- [Fitur](#fitur)
- [Teknologi](#teknologi)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [API Endpoints](#api-endpoints)
- [Model Database](#model-database)
- [Contoh Penggunaan](#contoh-penggunaan)
- [Error Handling](#error-handling)

## 🚀 Fitur

- ✅ Manajemen topik debat
- ✅ Sesi debat interaktif dengan AI
- ✅ Riwayat percakapan
- ✅ Integrasi dengan Groq AI
- ✅ RESTful API dengan Django REST Framework

## 🛠 Teknologi

- **Backend**: Django 5.2.5
- **API Framework**: Django REST Framework 3.16.1
- **Database**: SQLite (default)
- **AI Provider**: Groq AI
- **Python**: 3.12+

## 📦 Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd backend
```

### 2. Buat Virtual Environment

```bash
python -m venv env
source env/bin/activate  # Untuk macOS/Linux
# atau
env\Scripts\activate     # Untuk Windows
```

### 3. Install Dependencies

```bash
pip install django
pip install djangorestframework
pip install groq
pip install python-dotenv
```

### 4. Konfigurasi Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Jalankan Server

```bash
python manage.py runserver
```

Server akan berjalan di `http://127.0.0.1:8000/`

## ⚙️ Konfigurasi

### Environment Variables

Buat file `.env` di root directory dan tambahkan:

```env
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
SECRET_KEY=your_django_secret_key
```

## 📡 API Endpoints

### Base URL

```
http://127.0.0.1:8000/api/
```

---

## 1. 📝 Topic Management

### GET /api/topics/

Mengambil semua topik debat yang tersedia.

**Request:**

```http
GET /api/topics/
Content-Type: application/json
```

**Response Success (200):**

```json
[
  {
    "id": 1,
    "topic": "Apakah AI akan menggantikan pekerjaan manusia?"
  },
  {
    "id": 2,
    "topic": "Pengaruh media sosial terhadap kesehatan mental remaja"
  }
]
```

### POST /api/topics/

Membuat topik debat baru.

**Request:**

```http
POST /api/topics/
Content-Type: application/json

{
    "topic": "Apakah pendidikan online lebih efektif dari pendidikan tradisional?"
}
```

**Response Success (201):**

```json
{
  "id": 3,
  "topic": "Apakah pendidikan online lebih efektif dari pendidikan tradisional?",
  "message": "Topic created successfully"
}
```

**Response Error (400) - Topic Required:**

```json
{
  "error": "Topic is required"
}
```

**Response Error (400) - Topic Already Exists:**

```json
{
  "error": "Topic already exists"
}
```

---

## 2. 💬 Chat/Debate Session

### POST /api/chat/

Memulai sesi debat baru atau melanjutkan sesi yang sudah ada.

#### Memulai Sesi Baru

**Request:**

```http
POST /api/chat/
Content-Type: application/json

{
    "prompt": "Saya setuju bahwa AI akan membantu manusia, bukan menggantikan mereka",
    "topic": "Apakah AI akan menggantikan pekerjaan manusia?",
    "pihak": "Pro"
}
```

#### Melanjutkan Sesi yang Ada

**Request:**

```http
POST /api/chat/
Content-Type: application/json

{
    "prompt": "Namun, bukankah AI sudah mulai menggantikan pekerjaan di sektor manufaktur?",
    "sessionId": 1
}
```

**Response Success (200):**

```json
{
  "response": "Memang benar bahwa AI telah mengubah sektor manufaktur, namun perlu dibedakan antara 'menggantikan' dan 'mengotomatisasi'. Banyak pekerjaan yang berevolusi menjadi lebih kompleks dan membutuhkan kolaborasi antara manusia dan AI...",
  "session_id": 1
}
```

**Response Error (404) - Session Not Found:**

```json
{
  "error": "Sesi debat tidak ditemukan."
}
```

---

## 🗄️ Model Database

### TopicDebate

```python
class TopicDebate(models.Model):
    topic = models.CharField(max_length=255)
```

### DebateSession

```python
class DebateSession(models.Model):
    topic = models.ForeignKey(TopicDebate, related_name='sessions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

### ChatMessage

```python
class ChatMessage(models.Model):
    session = models.ForeignKey(DebateSession, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10)  # 'user' atau 'assistant'
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 💡 Contoh Penggunaan

### 1. Membuat Topik Baru

```bash
curl -X POST http://127.0.0.1:8000/api/topics/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "Dampak globalisasi terhadap budaya lokal"}'
```

### 2. Melihat Semua Topik

```bash
curl -X GET http://127.0.0.1:8000/api/topics/
```

### 3. Memulai Debat Baru

```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Globalisasi membantu menyebarkan budaya dan menciptakan pemahaman antar bangsa",
    "topic": "Dampak globalisasi terhadap budaya lokal",
    "pihak": "Pro"
  }'
```

### 4. Melanjutkan Debat

```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Tapi bagaimana dengan hilangnya identitas budaya lokal?",
    "sessionId": 1
  }'
```

---

## ⚠️ Error Handling

### Status Codes

| Code | Description                          |
| ---- | ------------------------------------ |
| 200  | OK - Request berhasil                |
| 201  | Created - Resource berhasil dibuat   |
| 400  | Bad Request - Data input tidak valid |
| 404  | Not Found - Resource tidak ditemukan |
| 500  | Internal Server Error - Error server |

### Common Errors

#### 1. Topic Required

```json
{
  "error": "Topic is required"
}
```

#### 2. Topic Already Exists

```json
{
  "error": "Topic already exists"
}
```

#### 3. Session Not Found

```json
{
  "error": "Sesi debat tidak ditemukan."
}
```

---

## 🔧 Development

### Menjalankan dalam Mode Development

```bash
python manage.py runserver 0.0.0.0:8000
```

### Mengakses Django Admin

1. Buat superuser:

```bash
python manage.py createsuperuser
```

2. Akses admin panel di: `http://127.0.0.1:8000/admin/`

### Testing

```bash
python manage.py test
```

---

## 📁 Struktur Proyek

```
backend/
├── manage.py
├── db.sqlite3
├── debat_LLM/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apichat/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── service.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
└── env/
```

---

## 🤝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📞 Contact

- **Developer**: Ghozi Waridi
- **Email**: [your-email@example.com]
- **GitHub**: [@Ghozi-Waridi](https://github.com/Ghozi-Waridi)

---

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Groq AI](https://groq.com/)
