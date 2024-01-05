# Dockerfile
FROM python:3.8-slim
 
# copy the code and requirements
COPY app.py .
COPY requirements.txt .
# install required python stuff
RUN pip install -r requirements.txt
 
WORKDIR .


ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "app:app", "-n"]