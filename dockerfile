FROM python:3.9.9-slim
WORKDIR /code
ADD . /code
RUN python3 -m pip install -r requirements.txt
CMD python3 observe.py
