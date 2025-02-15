FROM python:3-slim

COPY . /vacancy_text

WORKDIR /vacancy_text

ENV PYTHONPATH="/vacancy_text"

RUN pip3 install -r requirements.txt

CMD ["fastapi", "run", "./vacancy_text/main.py"]
