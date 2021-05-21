FROM python:3.7-slim

COPY . .
WORKDIR /code
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r ../requirements.txt

ENTRYPOINT ["python", "main.py"]
