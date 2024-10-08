# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /app

# install dependencies
RUN pip install --upgrade --no-cache pip
RUN pip install --upgrade pip poetry
COPY pyproject.toml .
COPY . .
RUN poetry config virtualenvs.create false
RUN poetry install
