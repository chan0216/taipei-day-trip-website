FROM python:3.9
WORKDIR /use/src/taipei_oneday
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . . 