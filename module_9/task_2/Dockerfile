FROM python:3.10.6-slim

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install -r /app/requirements.txt

COPY app.py static templates ./

ENTRYPOINT ["python", "app.py"]