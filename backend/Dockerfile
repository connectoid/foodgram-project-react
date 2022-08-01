#FROM python:3.10-slim
#RUN apt update && apt -y install libpq-dev build-essential
#WORKDIR /app
#COPY requirements.txt /app
#RUN pip install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir
#COPY ./ /app
FROM python:3.7-slim
RUN mkdir /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY /foodgram /app
WORKDIR /app
CMD ["python3", "manage.py", "runserver", "0:8000"] 