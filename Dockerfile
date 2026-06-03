FROM python:3.14-slim as resume_build

ENV POETRY_VERSION="2.4.1" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/app" \
    VENV_PATH="/app/.venv"

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN python -m pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR $PYSETUP_PATH

COPY app.py gunicorn.conf.py poetry.lock poetry.toml pyproject.toml ./

COPY data/ ./data/
COPY resume_app/ ./resume_app/
COPY schemas/ ./schemas/

RUN poetry install --no-root --no-directory --no-plugins --without=dev && \
    rm -f poetry.lock pyproject.toml poetry.toml

FROM python:3.14-slim as resume_app
LABEL org.opencontainer.image.authors="Patrick St. Jean, stjeanp@pat-st-jean.com"

ENV PATH="/app:/app/.venv/bin:${PATH}" \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN addgroup --gid 1001 resume && adduser --disabled-password --uid 1001 --gid 1001 --shell /bin/bash --comment "Resume App Account" resume

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y curl libglib2.0-0 libpango-1.0-0 libpangoft2-1.0-0 && \
    apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /app

RUN chown resume:resume /app
COPY --from=resume_build --chown=resume:resume /app/ ./

USER resume

EXPOSE 2112

HEALTHCHECK CMD curl -f http://localhost:2112/ || exit 1

ENTRYPOINT ["gunicorn", "app:app"]
