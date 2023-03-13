FROM python:3.9

WORKDIR /srv
COPY ./server/requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /srv/requirements.txt
COPY ./server/api.py /srv
COPY ./server/db.py /srv
COPY ./unbabel/calc.py /srv


CMD ["uvicorn", "api:app"]

