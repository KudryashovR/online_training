FROM python:3.12

WORKDIR /app

RUN apt-get update &&\
    apt-get install -y curl &&\
    curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml /app/

RUN poetry install --no-dev

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000