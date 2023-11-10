FROM python:3.11

WORKDIR /app

# Python dependencies
RUN pip install poetry
COPY pyproject.toml poetry.lock README.md /app/
COPY . /app
RUN cd /app && poetry config virtualenvs.create false && poetry install
RUN poetry run python project/tools/publish_posts.py
ENTRYPOINT ["poetry", "run", "gunicorn"]
CMD ["project.main:app", "-k", "uvicorn.workers.UvicornWorker", "--forwarded-allow-ips", "*"]