FROM python:3.8
LABEL maintainer="amartush@uoregon.edu"

# Set the working directory in the container to /app
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . /app

# Define the command to run the app
CMD ["python", "flask_api.py"]
