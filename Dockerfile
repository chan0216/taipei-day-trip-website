FROM --platform=linux/amd64 python:3.11.4

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn","-w","1","app:app","--bind","0.0.0.0:2000"]

EXPOSE 2000