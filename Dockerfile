FROM python:3.13-alpine

# Install necessary tools
RUN apk add --no-cache git curl build-base

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Clone the main app repository
RUN git clone https://github.com/Piechutowski-IERiGZ/slownik_upraw.git .

# Clone the data repo and move CSV files into expected location
RUN git clone https://github.com/Piechutowski-IERiGZ/slownik_upraw_data.git /tmp/data && \
    mkdir -p /app/slownik_upraw/CSV && \
    mv /tmp/data/*.csv /app/slownik_upraw/CSV && \
    rm -rf /tmp/data

# Install dependencies
RUN uv sync

# Expose port
EXPOSE 80

# Run the app
CMD ["sh", "-c", "uv pip install -e . && cd slownik_upraw && uv run litestar run --host 0.0.0.0 --port 80"]
