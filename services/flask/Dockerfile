FROM python:3.10.7-slim-buster
LABEL authors="Zuicie"

WORKDIR /app

# Install netcat
RUN apt update && apt install -y netcat

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY . /app

# Copy and set permissions for the entrypoint.sh script that handles migrations
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000

# Set the entrypoint of the script
ENTRYPOINT ["/entrypoint.sh"]

