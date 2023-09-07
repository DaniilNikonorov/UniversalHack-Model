FROM python:3.8.18-alpine3.18

WORKDIR /app

# Copy all files from the current directory into the /app directory in the container
COPY ./ /app

# Install necessary build dependencies
RUN apk add --no-cache \
    g++ \
    gcc \
    make \
    gfortran \
    musl-dev \
    python3-dev \
    openblas-dev

# RUN pip install --no-cache-dir -r requirements.txt

# Define the entry point for the container
ENTRYPOINT ["python"]

# Specify the default command to run when the container starts
CMD ["prediction.py"]