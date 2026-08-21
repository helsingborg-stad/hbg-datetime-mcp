FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN pip install --no-cache-dir uv \
    && uv sync --frozen

COPY main.py /app/
COPY src /app/src

CMD ["uv", "run", "main.py"]
