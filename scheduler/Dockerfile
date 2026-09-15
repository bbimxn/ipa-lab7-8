FROM python:3.10-slim
WORKDIR /home/myapp
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /home/myapp/
RUN pip install --progress-bar off --no-cache-dir -r requirements.txt
COPY ./database.py ./producer.py ./scheduler.py /home/myapp/
CMD ["python", "/home/myapp/scheduler.py"]
