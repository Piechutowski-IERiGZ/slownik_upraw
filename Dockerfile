FROM python:3.13-alpine

# Install necessary tools
RUN apk add --no-cache git curl build-base tree

# Install Rust using rustup
# Setting environment variables for Rust paths
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH

# Download and install Rust. -y answers yes to prompts.
# --no-modify-path is important in Docker so it doesn't try to modify shell profiles.
# We add cargo's bin directory to PATH manually via the ENV instruction above.
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Clone the main app repository
RUN git clone https://github.com/Piechutowski-IERiGZ/slownik_upraw.git .

# Clone the data repo and move CSV files directly to /app/CSV
RUN git clone https://github.com/Piechutowski-IERiGZ/slownik_upraw_data.git /tmp/data && \
    mkdir -p /app/CSV && \
    mv /tmp/data/*.csv /app/CSV && \
    rm -rf /tmp/data

# Install dependencies
RUN uv sync

# Expose port
EXPOSE 80

# Run the app
CMD ["sh", "-c", "uv pip install -e . && cd slownik_upraw && uv run litestar run --host 0.0.0.0 --port 80"]
