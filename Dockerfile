FROM python:3.12.7-slim-bookworm

COPY serving-rest-api/app.py app/
COPY serving-rest-api/requirement.txt app/
COPY model.pkl app/

RUN apt update -y \
    && apt clean all \
    && pip install -r /app/requirement.txt

EXPOSE 5000

ENTRYPOINT ["python", "/app/app.py"]