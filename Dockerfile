FROM python:3.8

EXPOSE 8000

COPY . .
WORKDIR /code
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r ../requirements.txt
RUN apt install -y netcat

ENTRYPOINT ["python", "main.py"]
