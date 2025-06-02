FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /tests

COPY . . 

RUN pip install -r ./config/requirements.txt

CMD [ "pytest", "test_base_event.py"]