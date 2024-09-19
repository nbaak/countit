FROM python:3.10.12

# Create and set the working directory
WORKDIR /app

RUN apt-get update && \
	apt-get upgrade -y

# Copy and install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the application source code
COPY ./src /app

# Create a group and user for running the application
RUN groupadd -r appuser -g 1000 && \
    useradd -u 1000 -r -g appuser -s /sbin/nologin -c "Docker image user" appuser && \
    chown -R appuser:appuser /app


# Use the python interpreter to run the application
USER appuser

# Expose the port the app runs on
EXPOSE 5000

CMD ["/app/entrypoint.sh"]