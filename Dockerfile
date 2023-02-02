FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt .
COPY .env .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]

