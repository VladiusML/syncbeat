FROM python:3.10

RUN mkdir /syncbeats

WORKDIR /syncbeats

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . . 

CMD ["gunicorn", "syncbeats.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]