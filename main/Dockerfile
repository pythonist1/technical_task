FROM python:3.8
ADD main.py /main/
ADD collector.py /main/
ADD schemas.py /main/
ADD database.py /main/
ADD index.html /main/
ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt
WORKDIR /main
