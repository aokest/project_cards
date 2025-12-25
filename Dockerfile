FROM python:3.9-slim

WORKDIR /app

# Copy only necessary files
COPY server.py .
COPY index.html .
COPY cardv8.html .
COPY project_timeline.html .
COPY initial_data.json .
COPY project_cards.json .
COPY reparse_v3.py .

# Expose port
EXPOSE 18889

# Run server
CMD ["python", "server.py"]
