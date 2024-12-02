# Use a lightweight Python image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the port for Jupyter Notebook
EXPOSE 8888

# Default command to first run scraping.py, then start JupyterLab
CMD ["bash", "-c", "python scraping.py && jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root"]
