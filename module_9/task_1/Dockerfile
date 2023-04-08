FROM python:3.10.6-slim

RUN mkdir /app

COPY requirements.txt /app/

RUN python -m pip install -r /app/requirements.txt

COPY app.py /app/

WORKDIR /app

ENTRYPOINT ["python", "app.py"]