FROM python:3.8

WORKDIR /app


COPY . .
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "__main__.py"]

