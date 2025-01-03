FROM python:slim

WORKDIR /app

# Install Python dependencies
RUN pip install playwright

# Run playwright install to ensure all browsers are downloaded
RUN playwright install --with-deps chromium

# Copy the Python script into the container
COPY backup.py /app

# Command to run the scraper script
CMD ["python", "backup.py"]
