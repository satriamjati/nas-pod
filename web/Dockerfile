# Use official Python image
FROM python:alpine

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (Flask default=5000)
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
