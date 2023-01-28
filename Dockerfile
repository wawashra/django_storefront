FROM python:3.9
EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
