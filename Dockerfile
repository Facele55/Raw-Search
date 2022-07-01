FROM python:3.9-alpine
# WARNING: DON'T USE FOR PRODUCTION. DOCKER IMAGE IS UNSTABLE AND DOES NOT HAVE SUITABLE SETTINGS.

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# install psycopg2 dependencies
RUN apk update && apk add --no-cache --virtual .build-deps gcc libc-dev libxml2 libxml2-dev && \
    apk add --no-cache libxslt-dev && \
    pip install --no-cache-dir lxml>=3.5.0 && \
    apk del .build-deps


COPY requirements.txt /code/

RUN pip install -U pip
RUN pip install setuptools wheel
RUN pip install -r requirements.txt

COPY . /code/

COPY ./docker-postgresql-multiple-databases/create-multiple-postgresql-databases.sh /docker-entrypoint-initdb.d/


#ENTRYPOINT ["./code/dir/docker-entrypoint.sh"]

RUN chmod +x /docker-entrypoint-initdb.d/create-multiple-postgresql-databases.sh

