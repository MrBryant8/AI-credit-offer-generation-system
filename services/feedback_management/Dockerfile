FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /usr/src/services/feedback_management
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Keep container alive
CMD ["sh", "-c", "tail -f /dev/null"]
