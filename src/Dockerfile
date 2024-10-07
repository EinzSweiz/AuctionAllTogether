FROM python:3.11-slim

WORKDIR /app

# Copy only the requirements first to leverage Docker cache
COPY requirements.txt .
RUN python3 -m venv /opt/venv && \
    pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make scripts executable
RUN chmod +x /app/migrate.sh /app/entrypoint.sh

CMD [ "/app/entrypoint.sh" ]
