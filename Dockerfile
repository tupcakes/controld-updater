FROM python:alpine

WORKDIR /app
COPY update-lists.py /app/

# Install dependencies
RUN apk add \
    bash \
    python3
RUN pip install --upgrade pip
RUN pip install argparse
RUN pip install requests

# Run the application
ENTRYPOINT ["python3","/app/update-lists.py"]