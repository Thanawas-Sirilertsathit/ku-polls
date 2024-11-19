FROM python:3-alpine

WORKDIR /app/polls
COPY ./requirements.txt .

# Install dependencies in Docker container
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x ./entrypoint.sh
# Load data

# Run this command in docker terminal
# python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json

EXPOSE 8000
# Run the server
CMD [ "./entrypoint.sh" ]