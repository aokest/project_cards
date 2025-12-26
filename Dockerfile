FROM python:3.9-slim

WORKDIR /app

# Copy application files
COPY . .

# Expose port
EXPOSE 18889

# Run server
CMD ["python", "server.py"]
