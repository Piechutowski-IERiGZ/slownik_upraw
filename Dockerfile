FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

RUN git clone https://github.com/Piechutowski-IERiGZ/slownik_upraw.git .

RUN git clone https://github.com/Piechutowski-IERiGZ/slownik_upraw_data.git /tmp/data && \
    mkdir -p /app/CSV && \
    mv /tmp/data/*.csv /app/CSV && \
    rm -rf /tmp/data

RUN uv sync

EXPOSE 80

CMD ["sh", "-c", "uv pip install -e . && cd slownik_upraw && uv run litestar run --host 0.0.0.0 --port 80"]