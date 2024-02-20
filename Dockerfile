FROM python:3.12.1-alpine

WORKDIR /app/

RUN apk add -qU --no-cache postgresql-libs gettext && \
    apk add -q --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev jpeg-dev zlib-dev && \
    pip install --no-cache-dir "poetry==1.7.1" && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root --no-cache --no-interaction && \
    apk --purge del .build-deps

COPY . .

RUN SECRET_KEY=dummy ./manage.py collectstatic --no-input
RUN SECRET_KEY=dummy ./manage.py compilemessages
