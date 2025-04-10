FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment inside the container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-root

# Copy the rest of the application
COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]