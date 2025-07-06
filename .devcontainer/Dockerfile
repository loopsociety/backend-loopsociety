FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crea el usuario antes de copiar archivos
RUN useradd -m vscode

WORKDIR /workspace

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pymysql

# Da permisos al usuario vscode sobre la carpeta de trabajo
RUN chown -R vscode /workspace

USER vscode


CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]