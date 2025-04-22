# Use Caddy image with Python for Uvicorn/Litestar
FROM caddy:2.8-alpine

# Install Python, git, and dependencies
RUN apk add --no-cache python3 py3-pip git && \
    python3 -m ensurepip && \
    pip3 install --no-cache-dir uvicorn litestar

# Set working directory
WORKDIR /app

# Clone web app repo
RUN git clone https://github.com/Piechutowski-IERiGZ/slownik_upraw.git app

# Clone data repo and move CSV files to parent CSV folder
RUN git clone https://github.com/Piechutowski-IERiGZ/slownik_upraw_data.git data && \
    mkdir -p /app/CSV && \
    mv /app/data/*.csv /app/CSV/

# Install app dependencies
RUN pip3 install --no-cache-dir -r /app/app/requirements.txt

# Copy Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile

# Expose port
EXPOSE 80

# Run Caddy and Uvicorn (1 worker)
CMD ["sh", "-c", "caddy run --config /etc/caddy/Caddyfile & uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1"]