FROM python:3-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /usr/src/services/client_management
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "-c", "print('Run me with: docker run --rm <image> python main.py')"]