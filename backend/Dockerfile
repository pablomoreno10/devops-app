FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml requirements.txt ./

RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

COPY new new

RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

# ---- RUNTIME STAGE ----
FROM python:3.12-slim AS runner

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY new new

EXPOSE 8000

CMD ["uvicorn", "mysite.main:app", "--host", "0.0.0.0", "--port", "8000"]

# multi-stage Docker build to separate the build environment from the runtime image
# smaller, cleaner container
# installing dependencies via pre-built wheels and deleting unnecessary artifacts.