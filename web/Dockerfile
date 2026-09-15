FROM python:3.10-slim
WORKDIR /home/myapp
COPY ./templates/* /home/myapp/templates/
COPY ./static/* /home/myapp/static/
COPY requirements.txt /home/myapp/
COPY ./app.py /home/myapp/
RUN pip install --progress-bar off --no-cache-dir -r requirements.txt
CMD ["python", "/home/myapp/app.py"]
EXPOSE 8080
