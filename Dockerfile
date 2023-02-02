FROM python:3.9-alpine
WORKDIR /app
RUN mkdir -p /app/templates
COPY requirements.txt .
COPY .env .
COPY ./templates/sermons.html /app/templates/sermons.html
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]

