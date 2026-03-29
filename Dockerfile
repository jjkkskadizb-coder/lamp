dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY oil_lamp.py .
EXPOSE 8000
CMD ["python3", "oil_lamp.py"]
