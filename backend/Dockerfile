FROM python:3.13-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    make \
    libssl-dev \
    libcurl4-openssl-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/install/bin:$PATH" \
    PYTHONPATH="/install/lib/python3.13/site-packages" \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    netcat-openbsd \
    wget \
    fontconfig \
    xfonts-base \
    xfonts-75dpi \
    tini \
 && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
 && apt-get install -y ./wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
 && rm wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN addgroup --system appuser && adduser --system --ingroup appuser appuser

WORKDIR /app

COPY --from=builder /install /install
COPY --chown=appuser:appuser . .

RUN chmod +x /app/entrypoints/*

USER appuser

EXPOSE 8000

# tini is used to handle signal forwarding and process reaping like PID 1
ENTRYPOINT ["/usr/bin/tini", "--"]