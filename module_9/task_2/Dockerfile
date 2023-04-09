FROM python:3.10.6-slim

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install -r /app/requirements.txt

COPY . ./

ENTRYPOINT ["python", "app.py"]