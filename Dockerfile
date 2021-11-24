FROM python:3.10-slim

#RUN buildDeps='gcc python3-dev' && \
#    apt-get update && \
#    apt-get install --no-install-recommends -y $buildDeps default-libmysqlclient-dev && \
#    pip install --upgrade pip && \
#    pip install mysqlclient && \
#    apt-get purge -y --auto-remove $buildDeps && \
#    rm -rf /var/cache/apt

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
COPY . /app

CMD ["python", "app.py"]
