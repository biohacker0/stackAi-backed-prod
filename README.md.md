# StackAI Backend Production

FastAPI server application for StackAI backend services.

## Quick Start

### Prerequisites

- Python 3.7+
- Git

### Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/biohacker0/stackAi-backed-prod.git
cd stackAi-backed-prod
```

2. **Activate virtual environment**

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Start the server**

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

The server will be available at `http://localhost:8080`

## Project Structure

```
├── .venv/              # Virtual environment
├── auth.py             # Authentication module
├── connections.py      # Database/API connections
├── knowledge_base.py   # Knowledge base functionality
├── main.py             # FastAPI application entry point
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
└── .env               # Environment variables
```

## Environment Setup

Create a `.env` file in the root directory with the following variables:

```env
SUPABASE_URL=
SUPABASE_ANON_KEY=
BACKEND_URL=
CONNECTION_ID=
CORS_ORIGINS=
AUTH_EMAIL=
AUTH_PASSWORD=
```

## Development

To run in development mode with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## Docker

### Build and run with Docker

1. **Build the image**

```bash
docker build -t stackai-backend .
```

2. **Run the container**

```bash
docker run -p 8080:8080 --env-file .env stackai-backend
```

### Using Docker Compose

Create a `docker-compose.yml`:

```yaml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "8080:8080"
    env_file:
      - .env
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

## Deployment

This project includes a `Procfile` for deployment on platforms like Heroku.
