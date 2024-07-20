# pull official base image
FROM python:3.10




# set work directory
WORKDIR /app

COPY . /app


RUN python -m venv venv

# Upgrade pip inside the virtual environment
RUN /app/venv/bin/pip install --upgrade pip

RUN /app/venv/bin/pip install -r requirements.txt

# set environment variables

ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:$PATH"


# copy project
COPY . .