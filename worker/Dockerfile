FROM python:3.10-slim
WORKDIR /home/myapp
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /home/myapp/
RUN pip install --progress-bar off --no-cache-dir -r requirements.txt
COPY ./worker.py /home/myapp/
CMD ["python", "/home/myapp/worker.py"]
