# Start from the osgeo/gdal image that includes Python
FROM ghcr.io/andrii-rieznik/python-gdal:py3.12.6-gdal3.9.2

# Install Python dependencies if needed
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application files
COPY . /app
WORKDIR /app

# Set default command to run main.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
