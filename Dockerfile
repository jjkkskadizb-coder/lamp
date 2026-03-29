FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN chmod +x start.sh

ENV PORT=8080

CMD ["./start.sh"]
