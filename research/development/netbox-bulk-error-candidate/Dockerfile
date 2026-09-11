FROM python:3.12-slim-bookworm
ARG NETBOX_REVISION
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN test -n "$NETBOX_REVISION" \
    && git init /upstream \
    && git -C /upstream remote add origin https://github.com/netbox-community/netbox.git \
    && git -C /upstream fetch --depth 1 origin "$NETBOX_REVISION" \
    && git -C /upstream checkout --detach FETCH_HEAD \
    && test "$(git -C /upstream rev-parse HEAD)" = "$NETBOX_REVISION"
RUN python -m pip install --no-cache-dir -r /upstream/requirements.txt
COPY reproduce.py nb_bulk_configuration.py /probe/
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
CMD ["python", "/probe/reproduce.py", "--source", "/upstream", "--output", "/results/observations.json"]
