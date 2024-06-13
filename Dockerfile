# Specify the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY . .

# Run the app
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]