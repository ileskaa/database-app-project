# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.6

FROM python:${PYTHON_VERSION}-slim

LABEL fly_launch_runtime="flask"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

ENV GUNICORN_CMD_ARGS="--bind=[::]:8000 --workers=4"

#  CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
CMD ["gunicorn", "app:app"]
