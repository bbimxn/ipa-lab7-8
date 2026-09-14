FROM python
WORKDIR /home/myapp
ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt /home/myapp/
RUN pip install -r requirements.txt
COPY ./database.py ./producer.py ./scheduler.py /home/myapp/
CMD ["python", "/home/myapp/scheduler.py"]
