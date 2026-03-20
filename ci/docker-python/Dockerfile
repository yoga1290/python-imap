FROM python:3.13-alpine

WORKDIR /usr/app
COPY utils ./utils
COPY entrypoint.py .
COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt

ENTRYPOINT [ "python", "entrypoint.py" ]