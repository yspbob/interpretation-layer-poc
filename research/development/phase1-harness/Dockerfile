FROM python:3.12-slim-bookworm@sha256:782412e85d0f0984994c290652577d4018aff08145c85b262bb63dc0c7522254
COPY worker.py /app/worker.py
USER 65534:65534
ENTRYPOINT ["python", "-I", "-B", "/app/worker.py"]
