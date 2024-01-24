FROM python:3.12-alpine as builder

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY ./dtb ./dtb
COPY ./settings ./settings
COPY ./manage.py ./manage.py

FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/daphne /usr/local/bin/daphne

ENTRYPOINT ["daphne"]

CMD [ "settings.asgi:application", "-b", "0.0.0.0", "-p", "8000" ]