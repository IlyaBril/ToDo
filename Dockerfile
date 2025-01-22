# pull official base image
FROM python

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY requirements.txt /usr/src/requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# copy project

COPY src /usr/src

EXPOSE 5000

#RUN ["uwsgi", "--http", "127.0.0.1", "--port", "5000", "--master", "-p", "4", "-w", "run:app"]

CMD ["uwsgi", "--http", "0.0.0.0:80", "--wsgi-file", "run.py", \
    "--callable", "app", "--stats", "0.0.0.0:81"]