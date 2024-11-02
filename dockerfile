FROM python:3.9-alpine

RUN apk update && apk upgrade
RUN apk add --no-cache tzdata

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD [ "python3", "observe.py" ]