FROM python:3-alpine

WORKDIR /app/polls
COPY ./requirements.txt .

# Install dependencies in Docker container
RUN pip install -r requirements.txt

COPY . .
# Migrate database
RUN python ./manage.py migrate
# Load data
RUN python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
EXPOSE 8000
# Run the server
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]