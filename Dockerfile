# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json and package-lock.json first (to leverage caching)
COPY package*.json ./

# Set Node.js to production mode & Install project-specific Node.js dependencies
ENV NODE_ENV=production
RUN npm install --production

# Copy the entire application code
COPY . .

# Run Webpack to build frontend assets
RUN npm run build  # Generates `frontend/build/manifest.json`

# Ensure TailwindCSS builds correctly
RUN npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify

# Ensure static directories exist
RUN mkdir -p /app/static /app/staticfiles

# Move Webpack-generated `manifest.json` to the correct location
RUN cp /app/frontend/build/manifest.json /app/staticfiles/manifest.json

# Collect Django static files
RUN python manage.py collectstatic --noinput

# Expose Django's default port
EXPOSE 8000

# Run Gunicorn to serve the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "anansi_app.wsgi:application"]
