# Pull official base Python Docker image
FROM python:3.10.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the django project
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
